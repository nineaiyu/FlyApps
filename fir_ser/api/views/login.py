from django.contrib import auth
from api.models import Token, UserInfo, UserCertificationInfo, CertificationInfo
from rest_framework.response import Response
from api.utils.serializer import UserInfoSerializer, CertificationSerializer, UserCertificationSerializer
from django.core.cache import cache
from rest_framework.views import APIView
import binascii
import os, datetime
from api.utils.utils import get_captcha, valid_captcha, is_valid_domain, is_valid_phone, \
    get_sender_sms_token, is_valid_email, is_valid_sender_code, get_sender_email_token, get_random_username, \
    check_username_exists
from api.utils.auth import ExpiringTokenAuthentication
from api.utils.response import BaseResponse
from fir_ser.settings import CACHE_KEY_TEMPLATE, SERVER_DOMAIN, REGISTER, LOGIN
from api.utils.storage.caches import login_auth_failed, set_default_app_wx_easy
import logging
from api.utils.geetest.geetest_utils import first_register, second_validate
from api.utils.throttle import VisitRegister1Throttle, VisitRegister2Throttle, GetAuthC1Throttle, GetAuthC2Throttle
from api.utils.storage.storage import Storage

logger = logging.getLogger(__name__)


def get_login_type():
    return LOGIN.get("login_type")


def get_register_type():
    return REGISTER.get("register_type")


def GetAuthenticate(target, password, act, allow_type):
    user_obj = None
    if act == 'email' and allow_type[act]:
        if is_valid_email(target):
            user_obj = UserInfo.objects.filter(email=target).values('username').first()
    elif act == 'sms' and allow_type[act]:
        if is_valid_phone(target):
            user_obj = UserInfo.objects.filter(mobile=target).values('username').first()
    elif act == 'up' and allow_type[act]:
        user_obj = auth.authenticate(username=target, password=password)

    if user_obj and act in ['email', 'sms']:
        user_obj = auth.authenticate(username=user_obj['username'], password=password)

    return user_obj


def CheckRegisterUerinfo(target, act, key):
    res = BaseResponse()
    res.data = {}
    times_key = "%s_%s_%s" % (key, act, target)

    if key == "register":
        if not get_register_type()[act]:
            res.code = 1002
            res.msg = "暂不允许该类型注册"
            return res

    if act == "sms":
        if is_valid_phone(target):
            if login_auth_failed("get", times_key):
                login_auth_failed("set", times_key)
                if UserInfo.objects.filter(mobile=target):
                    res.code = 1005
                    res.msg = "手机号已经存在"
                else:
                    token, code = get_sender_sms_token(act, target, 'register')
                    res.data["auth_token"] = token
            else:
                res.code = 1009
                res.msg = "该手机号今日使用次数已经达到上限"
        else:
            res.code = 1005
            res.msg = "手机号校验失败"

    elif act == "email":
        if is_valid_email(target):
            if login_auth_failed("get", times_key):
                login_auth_failed("set", times_key)
                if UserInfo.objects.filter(email=target):
                    res.code = 1005
                    res.msg = "邮箱已经存在"
                else:
                    token, code = get_sender_email_token(act, target, 'register')
                    res.data["auth_token"] = token
            else:
                res.code = 1009
                res.msg = "该邮箱今日注册次数已经达到上限"
        else:
            res.code = 1006
            res.msg = "邮箱校验失败"
    elif act == "up":
        if login_auth_failed("get", times_key):
            login_auth_failed("set", times_key)
            if UserInfo.objects.filter(username=target):
                res.code = 1005
                res.msg = "用户名已经存在"
            else:
                token, code = get_sender_email_token(act, target, 'register')
                res.data["auth_token"] = token
        else:
            res.code = 1009
            res.msg = "用户名已经存在"

    else:
        res.code = 1007
        res.msg = "信息发送失败"
    return res


def CheckChangeUerinfo(target, act, key, user, ftype=None):
    res = BaseResponse()
    res.data = {}

    if key == "change":
        if not get_login_type()[act]:
            res.code = 1002
            res.msg = "暂不允许该类型修改"
            return res
    times_key = "%s_%s_%s" % (user.uid, act, target)
    if act == "sms":
        if is_valid_phone(target) and str(user.mobile) != str(target):
            if login_auth_failed("get", times_key):
                login_auth_failed("set", times_key)
                if UserInfo.objects.filter(mobile=target) and ftype is None:
                    res.code = 1005
                    res.msg = "手机号已经存在"
                else:
                    token, code = get_sender_sms_token(act, target, 'change')
                    res.data["auth_token"] = token
            else:
                res.code = 1009
                res.msg = "该手机号今日注册次数已经达到上限"
        else:
            res.code = 1005
            res.msg = "手机号校验失败"

    elif act == "email":
        if is_valid_email(target) and str(user.email) != str(target):
            if login_auth_failed("get", times_key):
                login_auth_failed("set", times_key)
                if UserInfo.objects.filter(email=target):
                    res.code = 1005
                    res.msg = "邮箱已经存在"
                else:
                    token, code = get_sender_email_token(act, target, 'change')
                    res.data["auth_token"] = token
            else:
                res.code = 1009
                res.msg = "该邮箱今日注册次数已经达到上限"
        else:
            res.code = 1006
            res.msg = "邮箱校验失败"
    elif act == "up":
        if login_auth_failed("get", times_key):
            login_auth_failed("set", times_key)
            if UserInfo.objects.filter(username=target):
                res.code = 1005
                res.msg = "用户名已经存在"
            else:
                token, code = get_sender_email_token(act, target, 'change')
                res.data["auth_token"] = token
        else:
            res.code = 1009
            res.msg = "用户名已经存在"

    else:
        res.code = 1007
        res.msg = "信息发送失败"
    return res


class LoginView(APIView):
    throttle_classes = [VisitRegister1Throttle, VisitRegister2Throttle]

    def generate_key(self):
        return binascii.hexlify(os.urandom(32)).decode()

    def post(self, request):
        response = BaseResponse()
        receive = request.data
        username = receive.get("username", None)
        if LOGIN.get("captcha"):
            is_valid = valid_captcha(receive.get("cptch_key", None), receive.get("authcode", None), username)
        else:
            is_valid = True
        if is_valid:
            if LOGIN.get("geetest"):
                geetest = receive.get("geetest", None)
                if geetest and second_validate(geetest).get("result", "") == "success":
                    pass
                else:
                    response.code = 1001
                    response.msg = "geetest 验证有误"
                    return Response(response.dict)

            login_type = receive.get("login_type", None)
            if login_auth_failed("get", username):
                password = receive.get("password")
                user = GetAuthenticate(username, password, login_type, get_login_type())
                logger.info("username:%s  password:%s" % (username, password))
                if user:
                    if user.is_active:
                        login_auth_failed("del", username)
                        # update the token
                        key = self.generate_key()
                        now = datetime.datetime.now()
                        user_info = UserInfo.objects.get(pk=user.pk)

                        auth_key = "_".join([CACHE_KEY_TEMPLATE.get('user_auth_token_key'), key])
                        cache.set(auth_key, {'uid': user_info.uid, 'username': user_info.username}, 3600 * 24 * 7)
                        Token.objects.create(user=user, **{"access_token": key, "created": now})

                        serializer = UserInfoSerializer(user_info, )
                        data = serializer.data
                        response.msg = "验证成功!"
                        response.userinfo = data
                        response.token = key
                    else:
                        response.msg = "用户被禁用"
                        response.code = 1005
                else:
                    login_auth_failed("set", username)
                    #
                    # try:
                    #     UserInfo.objects.get(username=username)
                    response.msg = "密码或者账户有误"
                    response.code = 1002
                    # except UserInfo.DoesNotExist:
                    #     response.msg = "用户不存在!"
                    #     response.code = 1003
            else:
                response.code = 1006
                logger.error("username:%s failed too try , locked" % (username,))
                response.msg = "用户登录失败次数过多，已被锁定，请1小时之后再次尝试"
        else:
            response.code = 1001
            response.msg = "验证码有误"

        return Response(response.dict)

    def get(self, request):
        response = BaseResponse()
        response.data = {}
        if LOGIN.get("captcha"):
            response.data = get_captcha()
        if LOGIN.get("geetest"):
            response.data['geetest'] = True
        response.data['login_type'] = get_login_type()
        allow_f = REGISTER.get("enable")
        response.data['register_enable'] = allow_f
        return Response(response.dict)

    def put(self, request):
        import hashlib
        response = BaseResponse()
        user_id = request.data.get('user_id', None)
        if user_id:
            sha = hashlib.sha1(str(user_id).encode("utf-8"))
            response.data = first_register(sha.hexdigest(), request.META.get('REMOTE_ADDR'))
        else:
            response.code = 1002
            response.msg = '参数错误'
        return Response(response.dict)


class RegistView(APIView):
    throttle_classes = [VisitRegister1Throttle, VisitRegister2Throttle]

    def generate_key(self):
        return binascii.hexlify(os.urandom(32)).decode()

    def post(self, request):
        response = BaseResponse()
        receive = request.data

        username = receive.get("username", None)

        if is_valid_email(username):
            act = 'email'
        elif is_valid_phone(username):
            act = 'sms'
        else:
            response.code = 1001
            response.msg = "邮箱或手机校验有误"
            return Response(response.dict)

        if not get_register_type()[act]:
            response.code = 1002
            response.msg = "不允许该类型注册"
            return Response(response.dict)

        if REGISTER.get("geetest"):
            geetest = request.data.get("geetest", None)
            if geetest and second_validate(geetest).get("result", "") == "success":
                pass
            else:
                response.code = 1018
                response.msg = "geetest验证有误"
                return Response(response.dict)

        is_valid, target = is_valid_sender_code(act, receive.get("auth_token", None), receive.get("auth_key", None))
        if is_valid and str(target) == str(username):
            if login_auth_failed("get", username):
                password = receive.get("password")
                password2 = receive.get("password2")
                if password == password2:
                    random_username = get_random_username()
                    if is_valid_email(username):

                        user_obj = UserInfo.objects.create_user(random_username, email=username, password=password,
                                                                first_name=random_username[:8])
                    elif is_valid_phone(username):
                        user_obj = UserInfo.objects.create_user(random_username, mobile=username, password=password,
                                                                first_name=random_username[:8])
                    else:
                        user_obj = None
                        response.msg = "注册异常"
                        response.code = 1000
                    if user_obj:
                        response.msg = "注册成功"
                        response.code = 1000
                else:
                    response.code = 1001
                    response.msg = "密码不一致"
            else:
                response.code = 1006
                logger.error("username:%s failed too try , locked" % (username,))
                response.msg = "用户注册失败次数过多，已被锁定，请1小时之后再次尝试"
        else:
            response.code = 1001
            response.msg = "邮件或短信验证码有误"

        return Response(response.dict)

    def get(self, request):
        response = BaseResponse()
        response.data = {}
        allow_f = REGISTER.get("enable")
        if allow_f:
            if REGISTER.get("captcha"):
                response.data = get_captcha()
            if REGISTER.get("geetest"):
                response.data['geetest'] = True
            response.data['register_type'] = get_register_type()
        response.data['enable'] = allow_f
        return Response(response.dict)


class UserInfoView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get(self, request):
        res = BaseResponse()
        serializer = UserInfoSerializer(request.user)
        res.data = serializer.data

        return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        data = request.data
        logger.info("user:%s update old data:%s" % (request.user, request.user.__dict__))
        logger.info("user:%s update new data:%s" % (request.user, data))

        oldpassword = data.get("oldpassword", None)
        surepassword = data.get("surepassword", None)

        mobile = data.get("mobile", None)
        email = data.get("email", None)
        if mobile or email:
            is_valid = valid_captcha(data.get("cptch_key", None), data.get("authcode", None), request)
            if not is_valid:
                res.code = 1008
                res.msg = "图片验证码异常"
                return Response(res.dict)

        if oldpassword and surepassword:
            user = auth.authenticate(username=request.user.username, password=oldpassword)
            if user is not None:
                user.set_password(surepassword)
                user.save()
                res.msg = "密码修改成功"
                logger.info("user:%s change password success,old %s new %s" % (request.user, oldpassword, surepassword))

                auth_token = request.auth
                for token_obj in Token.objects.filter(user=user):
                    if token_obj.access_token != auth_token:
                        cache.delete(token_obj.access_token)
                        token_obj.delete()

                return Response(res.dict)
            else:
                res.code = 1004
                res.msg = "老密码校验失败"
        else:
            # 修改个人资料
            domain_name = data.get("domain_name", None)
            if domain_name:
                domain_name_list = domain_name.strip(' ').replace("http://", "").replace("https://", "").split("/")
                if len(domain_name_list) > 0:
                    domain_name = domain_name_list[0]
                    if len(domain_name) > 3 and is_valid_domain(domain_name):
                        if domain_name == SERVER_DOMAIN.get("REDIRECT_UDID_DOMAIN").split("//")[1]:
                            user_admin_obj = UserInfo.objects.filter(is_superuser=True, uid=request.user.uid).order_by(
                                'pk').first()
                            if user_admin_obj:
                                request.user.domain_name = domain_name
                                set_default_app_wx_easy(request.user, True)
                            else:
                                serializer = UserInfoSerializer(request.user)
                                res.data = serializer.data
                                res.code = 1004
                                res.msg = "域名设置失败，请更换其他域名"
                                return Response(res.dict)
                        else:
                            request.user.domain_name = domain_name
                            set_default_app_wx_easy(request.user, True)
                    else:
                        serializer = UserInfoSerializer(request.user)
                        res.data = serializer.data
                        res.code = 1004
                        res.msg = "域名校验失败"
                        return Response(res.dict)

            if domain_name == '':
                request.user.domain_name = None
                set_default_app_wx_easy(request.user)

            username = data.get("username", None)
            if username and username != request.user.username:
                if check_username_exists(username):
                    res.msg = "用户名已经存在"
                    res.code = 1005
                    logger.error("User %s info save failed. Excepiton:%s" % (request.user, 'username already exists'))
                    return Response(res.dict)
                if len(username) < 6:
                    res.msg = "用户名至少6位"
                    res.code = 1006
                    return Response(res.dict)

            request.user.job = data.get("job", request.user.job)
            request.user.first_name = data.get("first_name", request.user.first_name)
            request.user.username = data.get("username", request.user.username)

            sms_token = data.get("auth_token", None)
            if sms_token:
                act = data.get("act", None)
                status, target = is_valid_sender_code(act, data.get("auth_token", None), data.get("auth_key", None))
                if status:

                    if act == 'sms' and mobile:
                        if str(target) == str(mobile):
                            if is_valid_phone(mobile):
                                request.user.mobile = data.get("mobile", request.user.mobile)
                        else:
                            res.code = 1005
                            res.msg = "手机号异常"
                    elif act == 'email' and email:
                        if str(target) == str(email):
                            if is_valid_email(email):
                                request.user.email = data.get("email", request.user.email)
                        else:
                            res.code = 1005
                            res.msg = "邮箱异常"
                    if res.code != 1000:
                        return Response(res.dict)
                else:
                    res.code = 1005
                    res.msg = "验证码校验失败"
                    return Response(res.dict)

            try:
                request.user.save()
            except Exception as e:
                serializer = UserInfoSerializer(request.user)
                res.data = serializer.data
                res.code = 1004
                res.msg = "信息保存失败"
                logger.error("User %s info save failed. Excepiton:%s" % (request.user, e))
                return Response(res.dict)
            serializer = UserInfoSerializer(request.user)
            res.data = serializer.data
            return Response(res.dict)

        return Response(res.dict)


class AuthorizationView(APIView):
    throttle_classes = [GetAuthC1Throttle, GetAuthC2Throttle]

    def post(self, request):
        res = BaseResponse()
        res.data = {}
        act = request.data.get("act", None)
        target = request.data.get("target", None)
        ext = request.data.get("ext", None)
        register_type = get_register_type()
        if ext and register_type.get('code', None) and ext.get('icode', None):
            if ext.get('icode') == '689888666':
                pass
            else:
                res.code = 1008
                res.msg = "邀请码已失效"
                return Response(res.dict)

        if REGISTER.get("captcha"):
            is_valid = valid_captcha(ext.get("cptch_key", None), ext.get("authcode", None), target)
            if ext and is_valid:
                pass
            else:
                res.code = 1018
                res.msg = "图片验证码有误"
                return Response(res.dict)

        if REGISTER.get("geetest"):
            geetest = request.data.get("geetest", None)
            if geetest and second_validate(geetest).get("result", "") == "success":
                pass
            else:
                res.code = 1018
                res.msg = "geetest验证有误"
                return Response(res.dict)

        res = CheckRegisterUerinfo(target, act, 'register')

        return Response(res.dict)


class ChangeAuthorizationView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]
    throttle_classes = [GetAuthC1Throttle, GetAuthC2Throttle]

    def post(self, request):
        res = BaseResponse()
        res.data = {}
        act = request.data.get("act", None)
        target = request.data.get("target", None)
        ext = request.data.get("ext", None)
        ftype = request.data.get("ftype", None)
        if REGISTER.get("captcha"):
            if ext and valid_captcha(ext.get("cptch_key", None), ext.get("authcode", None), target):
                pass
            else:
                res.code = 1009
                res.msg = "图片验证码有误"
                return Response(res.dict)

        if REGISTER.get("geetest"):
            geetest = request.data.get("geetest", None)
            if geetest and second_validate(geetest).get("result", "") == "success":
                pass
            else:
                res.code = 1018
                res.msg = "geetest验证有误"
                return Response(res.dict)

        res = CheckChangeUerinfo(target, act, 'change', request.user, ftype)
        return Response(res.dict)


class UserApiTokenView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get(self, request):
        res = BaseResponse()
        res.data = {
            'token': request.user.api_token
        }
        return Response(res.dict)

    def put(self, request):
        res = BaseResponse()
        data = request.data

        oldtoken = data.get("token", None)
        if oldtoken == request.user.api_token:
            request.user.api_token = 'reset'
        try:
            request.user.save()
        except Exception as e:
            logger.error("User %s api_token save failed. Excepiton:%s" % (request.user, e))
            res.code = 1002
            res.msg = "token 生成失败"
            return Response(res.dict)
        return self.get(request)


class CertificationView(APIView):
    authentication_classes = [ExpiringTokenAuthentication, ]

    def get(self, request):
        res = BaseResponse()
        res.data = {}
        act = request.query_params.get("act", "")
        user_certification_obj = UserCertificationInfo.objects.filter(user_id=request.user).first()
        if user_certification_obj and user_certification_obj.status == 1 or act == "usercert":
            card = user_certification_obj.card
            res.data["usercert"] = {
                'name': user_certification_obj.name,
                'addr': user_certification_obj.addr,
                'card': "%s%s%s" % (card[:4], '*' * (len(card) - 8), card[-4:]),
                'mobile': user_certification_obj.mobile,
                'status': user_certification_obj.status,
                'msg': user_certification_obj.msg,
            }
            return Response(res.dict)

        if 'certinfo' in act:
            if user_certification_obj:
                user_certification_serializer = UserCertificationSerializer(user_certification_obj)
                res.data["user_certification"] = user_certification_serializer.data
        if 'certpic' in act:
            certification_obj = CertificationInfo.objects.filter(user_id=request.user).all()
            if certification_obj:
                storage = Storage(request.user)
                certification_serializer = CertificationSerializer(certification_obj, many=True,
                                                                   context={"storage": storage})
                res.data["certification"] = certification_serializer.data
        return Response(res.dict)

    def post(self, request):
        res = BaseResponse()
        data = request.data

        user_certification_obj = UserCertificationInfo.objects.filter(user_id=request.user).first()
        if user_certification_obj and user_certification_obj.status == 1:
            return Response(res.dict)

        try:
            if REGISTER.get("captcha"):
                if data and valid_captcha(data.get("cptch_key", None), data.get("authcode", None), data.get("mobile")):
                    pass
                else:
                    res.code = 1009
                    res.msg = "图片验证码有误"
                    return Response(res.dict)

            is_valid, target = is_valid_sender_code('sms', data.get("auth_token", None), data.get("auth_key", None))
            if is_valid and str(target) == str(data.get("mobile")):
                if login_auth_failed("get", data.get("mobile")):
                    del data["cptch_key"]
                    del data["authcode"]
                    del data["auth_key"]
                    del data["auth_token"]
                    UserCertificationInfo.objects.update_or_create(user_id=request.user, status=0, defaults=data)
                    return self.get(request)

                else:
                    res.code = 1006
                    logger.error("username:%s failed too try , locked" % (request.user,))
                    res.msg = "用户注册失败次数过多，已被锁定，请1小时之后再次尝试"
            else:
                res.code = 1001
                res.msg = "短信验证码有误"

        except Exception as e:
            logger.error("%s UserCertificationInfo save %s failed Exception: %s" % (request.user, data, e))
            res.msg = "数据异常，请检查"
            res.code = 1002
        return Response(res.dict)
