# Generated by Django 3.0.3 on 2021-05-27 13:55

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='用户名')),
                ('email',
                 models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('uid', models.CharField(db_index=True, max_length=64, unique=True)),
                ('mobile', models.BigIntegerField(help_text='用于手机验证码登录', null=True, unique=True, verbose_name='手机')),
                ('qq', models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='QQ')),
                ('is_active', models.BooleanField(default=True, verbose_name='账户状态，默认启用')),
                ('storage_active', models.BooleanField(default=False, verbose_name='配置存储，默认关闭')),
                ('supersign_active', models.BooleanField(default=False, verbose_name='配置超级签，默认关闭')),
                ('job', models.TextField(blank=True, max_length=128, null=True, verbose_name='职位')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('gender',
                 models.SmallIntegerField(choices=[(0, '保密'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('head_img', models.CharField(default='head_img.jpeg', max_length=256, verbose_name='个人头像')),
                ('role', models.SmallIntegerField(choices=[(0, '普通会员'), (1, 'VIP'), (2, 'SVIP'), (3, '管理员')], default=0,
                                                  verbose_name='角色')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('download_times', models.PositiveIntegerField(default=0, verbose_name='可用下载次数,需要用户充值')),
                ('all_download_times', models.BigIntegerField(default=0, verbose_name='总共下载次数')),
                ('history_release_limit',
                 models.IntegerField(blank=True, default=10, null=True, verbose_name='app 历史记录版本')),
                ('api_token', models.CharField(default='', max_length=256, verbose_name='api访问密钥')),
            ],
            options={
                'verbose_name': '账户信息',
                'verbose_name_plural': '账户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppIOSDeveloperInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issuer_id', models.CharField(max_length=64, verbose_name='标识创建认证令牌的发放者')),
                ('private_key_id', models.CharField(max_length=64, verbose_name='密钥 ID')),
                ('p8key', models.TextField(max_length=512, verbose_name='p8key')),
                ('is_actived', models.BooleanField(default=False, verbose_name='是否已经激活')),
                ('certid', models.CharField(blank=True, max_length=64, null=True, verbose_name='超级签名自动创建证书ID')),
                ('usable_number', models.IntegerField(default=100, verbose_name='可使用设备数')),
                ('use_number', models.IntegerField(default=0, verbose_name='已消耗设备数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('cert_expire_time', models.DateTimeField(blank=True, null=True, verbose_name='证书过期时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('auth_type', models.SmallIntegerField(choices=[(0, 'p8key认证')], default=0, verbose_name='认证类型')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '苹果开发者账户',
                'verbose_name_plural': '苹果开发者账户',
            },
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('type', models.SmallIntegerField(choices=[(0, 'android'), (1, 'ios')], default=0, verbose_name='类型')),
                ('status',
                 models.SmallIntegerField(choices=[(0, '封禁'), (1, '正常'), (2, '违规')], default=1, verbose_name='应用状态')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='应用名称')),
                ('short', models.CharField(db_index=True, max_length=16, unique=True, verbose_name='短链接')),
                ('bundle_id', models.CharField(blank=True, max_length=64, verbose_name='bundle id')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('count_hits', models.BigIntegerField(default=0, verbose_name='下载次数')),
                ('password', models.CharField(blank=True, help_text='默认 没有密码', max_length=32, verbose_name='访问密码')),
                ('isshow', models.BooleanField(default=True, verbose_name='下载页可见')),
                ('issupersign', models.BooleanField(default=False, verbose_name='是否超级签名包')),
                ('supersign_type', models.SmallIntegerField(
                    choices=[(0, '普通权限'), (1, '推送权限，请上传adhoc包'), (2, 'network、vpn、推送权限，请上传adhoc包'), (3, '特殊权限')],
                    default=1, verbose_name='签名类型')),
                ('new_bundle_id', models.CharField(blank=True, help_text='用于超级签某些因素下需要修改包名', max_length=64, null=True,
                                                   verbose_name='new_bundle_id')),
                ('supersign_limit_number', models.IntegerField(default=0, verbose_name='签名使用限额')),
                ('wxredirect', models.BooleanField(default=True, verbose_name='微信内第三方链接自动跳转')),
                ('wxeasytype', models.BooleanField(default=True, verbose_name='微信内简易模式，避免微信封停')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='描述')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('has_combo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                   related_name='combo_app_info', to='api.Apps', verbose_name='关联应用')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '应用信息',
                'verbose_name_plural': '应用信息',
            },
        ),
        migrations.CreateModel(
            name='DomainCnameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_record', models.CharField(max_length=128, unique=True, verbose_name='记录值')),
                ('ip_address', models.CharField(max_length=128, verbose_name='域名解析地址')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用该解析')),
                ('is_system', models.BooleanField(default=False, verbose_name='是否是系统自带解析')),
                ('is_https', models.BooleanField(default=False, verbose_name='是否支持HTTPS')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '系统分发域名配置',
                'verbose_name_plural': '系统分发域名配置',
            },
        ),
        migrations.CreateModel(
            name='VerifyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32, verbose_name='真实姓名')),
                ('id_card', models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证号或护照号')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='联系地址')),
                ('mobile', models.BigIntegerField(blank=True, null=True, verbose_name='联系电话')),
                ('date_verify', models.DateTimeField(auto_now_add=True, verbose_name='认证时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verify_info',
                                              to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '实名认证',
                'verbose_name_plural': '实名认证',
            },
        ),
        migrations.CreateModel(
            name='UserDomainInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(db_index=True, max_length=64, verbose_name='下载页面域名')),
                ('is_enable', models.BooleanField(default=False, verbose_name='绑定成功')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Apps',
                                   verbose_name='APP专属域名')),
                ('cname_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DomainCnameInfo',
                                               verbose_name='cname解析ID')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '用户分发域名绑定',
                'verbose_name_plural': '用户分发域名绑定',
            },
        ),
        migrations.CreateModel(
            name='UserCertificationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='真实姓名')),
                ('card', models.CharField(max_length=128, unique=True, verbose_name='身份证号码')),
                ('addr', models.CharField(max_length=128, verbose_name='居住地址')),
                ('mobile', models.BigIntegerField(blank=True, null=True, verbose_name='手机号码')),
                ('status',
                 models.SmallIntegerField(choices=[(-1, '待认证'), (0, '认证中'), (1, '认证成功'), (2, '认证失败')], default=0,
                                          verbose_name='认证状态')),
                ('msg', models.CharField(blank=True, max_length=512, null=True, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('reviewed_time', models.DateTimeField(auto_now=True, verbose_name='审核时间')),
                ('user_id',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certification',
                                      to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '用户认证信息',
                'verbose_name_plural': '用户认证信息',
            },
        ),
        migrations.CreateModel(
            name='UDIDsyncDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udid', models.CharField(db_index=True, max_length=64, verbose_name='udid唯一标识')),
                ('product', models.CharField(blank=True, max_length=64, null=True, verbose_name='产品')),
                ('serial', models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号')),
                ('version', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('platform', models.SmallIntegerField(choices=[(0, 'fly分发'), (1, 'app developer')], default=0,
                                                      verbose_name='udid所在平台')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
            ],
            options={
                'verbose_name': 'iOS开发平台同步设备信息',
                'verbose_name_plural': 'iOS开发平台同步设备信息',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=64, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token',
                                           to=settings.AUTH_USER_MODEL, verbose_name='关联用户')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='下载包唯一名称')),
                ('title', models.CharField(max_length=128, verbose_name='下载包名称')),
                ('description', models.CharField(max_length=128, verbose_name='下载包描述')),
                ('price', models.BigIntegerField(verbose_name='下载包价格，单位分')),
                ('package_size', models.BigIntegerField(verbose_name='下载包次数')),
                ('download_count_gift', models.IntegerField(default=0, verbose_name='赠送下载次数')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用该价格')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '价格列表',
                'verbose_name_plural': '价格列表',
                'unique_together': {('price', 'package_size')},
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.SmallIntegerField(choices=[(0, '微信'), (1, '支付宝'), (2, '优惠码'), (4, '银联')])),
                ('payment_number', models.CharField(blank=True, max_length=128, null=True, verbose_name='支付第3方订单号')),
                ('payment_name', models.CharField(blank=True, max_length=128, null=True, verbose_name='支付商家名称')),
                ('order_number', models.CharField(max_length=128, unique=True, verbose_name='订单号')),
                ('actual_amount', models.BigIntegerField(verbose_name='实付金额,单位分')),
                ('actual_download_times', models.BigIntegerField(default=0, verbose_name='实际购买的数量')),
                ('actual_download_gift_times', models.BigIntegerField(default=0, verbose_name='实际赠送的数量')),
                ('status', models.SmallIntegerField(
                    choices=[(0, '交易成功'), (1, '待支付'), (2, '订单已创建'), (3, '退费申请中'), (4, '已退费'), (5, '主动取消'), (6, '超时取消')],
                    verbose_name='状态')),
                ('order_type',
                 models.SmallIntegerField(choices=[(0, '用户下单'), (1, '后台充值')], default=0, verbose_name='订单类型')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='付款时间')),
                ('cancel_time', models.DateTimeField(blank=True, null=True, verbose_name='订单取消时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                (
                    'user_id',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeveloperDevicesID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did', models.CharField(max_length=64)),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
                ('udid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.UDIDsyncDeveloper',
                                           verbose_name='所消耗的udid')),
            ],
            options={
                'verbose_name': '超级签Devices id',
                'verbose_name_plural': '超级签Devices id',
            },
        ),
        migrations.CreateModel(
            name='DeveloperAppID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.CharField(max_length=64)),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
            ],
            options={
                'verbose_name': '超级签APP id',
                'verbose_name_plural': '超级签APP id',
            },
        ),
        migrations.CreateModel(
            name='CertificationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification_url', models.CharField(blank=True, max_length=128, verbose_name='认证URL')),
                ('type',
                 models.SmallIntegerField(choices=[(0, '未知'), (1, '国徽面照片'), (2, '人像面照片'), (3, '手持身份证照片')], default=0,
                                          verbose_name='图像类型')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '身份证截图',
                'verbose_name_plural': '身份证截图',
            },
        ),
        migrations.CreateModel(
            name='AppUDID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udid', models.CharField(db_index=True, max_length=64, verbose_name='udid唯一标识')),
                ('product', models.CharField(blank=True, max_length=64, null=True, verbose_name='产品')),
                ('serial', models.CharField(blank=True, max_length=64, null=True, verbose_name='序列号')),
                ('version', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('imei', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('iccid', models.CharField(blank=True, max_length=64, null=True, verbose_name='型号')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_signed', models.BooleanField(default=False, verbose_name='是否完成签名打包')),
                ('binary_file', models.CharField(blank=True, max_length=128, null=True, verbose_name='签名包名称')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '设备详情',
                'verbose_name_plural': '设备详情',
            },
        ),
        migrations.CreateModel(
            name='APPToDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binary_file',
                 models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='签名包名称')),
                ('release_file', models.CharField(blank=True, max_length=128, null=True, verbose_name='源包名称')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
            ],
            options={
                'verbose_name': '应用开发者绑定',
                'verbose_name_plural': '应用开发者绑定',
            },
        ),
        migrations.CreateModel(
            name='APPSuperSignUsedInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
                ('developerid',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppIOSDeveloperInfo',
                                   verbose_name='所使用苹果开发者账户')),
                ('udid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AppUDID',
                                           verbose_name='所消耗的udid')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '设备使用统计',
                'verbose_name_plural': '设备使用统计',
            },
        ),
        migrations.CreateModel(
            name='AppStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='存储名字')),
                ('storage_type',
                 models.SmallIntegerField(choices=[(0, '本地存储'), (1, '七牛云存储'), (2, '阿里云存储'), (3, '默认存储')], default=3,
                                          verbose_name='存储类型')),
                ('access_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问key')),
                ('secret_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='存储访问secret')),
                (
                    'bucket_name',
                    models.CharField(blank=True, max_length=128, null=True, verbose_name='存储空间bucket_name')),
                ('domain_name',
                 models.CharField(blank=True, help_text='fly-storage.dvcloud.xin,可以自定义端口', max_length=128, null=True,
                                  verbose_name='下载域名')),
                ('is_https', models.BooleanField(default=True, verbose_name='是否支持https')),
                ('sts_role_arn',
                 models.CharField(blank=True, max_length=128, null=True, verbose_name='阿里云sts_role_arn')),
                ('endpoint', models.CharField(blank=True, max_length=128, null=True, verbose_name='阿里云endpoint')),
                ('download_auth_type', models.SmallIntegerField(
                    choices=[(1, 'OSS模式： 需要把OSS权限开启私有模式'), (2, 'CDN模式： 请先配置好阿里云CDN，开启阿里云OSS私有Bucket回源，将使用鉴权A方式')],
                    default=1, verbose_name='阿里云下载授权方式')),
                ('cnd_auth_key',
                 models.CharField(blank=True, max_length=128, null=True, verbose_name='阿里云cnd_auth_key')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('description', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                              verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '存储配置',
                'verbose_name_plural': '存储配置',
            },
        ),
        migrations.CreateModel(
            name='AppScreenShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot_url', models.CharField(blank=True, max_length=128, verbose_name='应用截图URL')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '应用截图',
                'verbose_name_plural': '应用截图',
            },
        ),
        migrations.CreateModel(
            name='AppReleaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_master', models.BooleanField(default=True, verbose_name='是否master版本')),
                (
                    'release_id',
                    models.CharField(db_index=True, max_length=64, unique=True, verbose_name='release 版本id')),
                ('build_version', models.CharField(blank=True, max_length=16, verbose_name='build版本')),
                ('app_version', models.CharField(blank=True, max_length=16, verbose_name='app版本')),
                ('release_type',
                 models.SmallIntegerField(choices=[(0, 'android'), (1, 'adhoc'), (2, 'Inhouse'), (3, 'unknown')],
                                          default=0, verbose_name='版本类型')),
                ('minimum_os_version', models.CharField(max_length=64, verbose_name='应用可安装的最低系统版本')),
                ('binary_size', models.BigIntegerField(verbose_name='应用大小')),
                ('binary_url', models.CharField(blank=True, max_length=128, verbose_name='第三方下载URL')),
                ('icon_url', models.CharField(blank=True, max_length=128, verbose_name='图标url')),
                ('changelog', models.TextField(blank=True, default=None, null=True, verbose_name='更新日志')),
                ('udid', models.TextField(blank=True, default='', null=True, verbose_name='ios内测版 udid')),
                ('distribution_name',
                 models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='企业签名')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '应用详情',
                'verbose_name_plural': '应用详情',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='default_domain_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DomainCnameInfo',
                                    verbose_name='默认下载页域名'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True,
                                         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                         related_name='user_set', related_query_name='user', to='auth.Group',
                                         verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='storage',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                       related_name='app_storage', to='api.AppStorage', verbose_name='存储'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                         related_name='user_set', related_query_name='user', to='auth.Permission',
                                         verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='usercertificationinfo',
            index=models.Index(fields=['card'], name='api_usercer_card_246743_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='udidsyncdeveloper',
            unique_together={('udid', 'developerid')},
        ),
        migrations.AlterUniqueTogether(
            name='developerdevicesid',
            unique_together={('did', 'developerid', 'app_id')},
        ),
        migrations.AlterUniqueTogether(
            name='developerappid',
            unique_together={('aid', 'developerid', 'app_id')},
        ),
        migrations.AlterUniqueTogether(
            name='appudid',
            unique_together={('app_id', 'udid')},
        ),
        migrations.AddIndex(
            model_name='appscreenshot',
            index=models.Index(fields=['app_id'], name='api_appscre_app_id__b65655_idx'),
        ),
        migrations.AddIndex(
            model_name='apps',
            index=models.Index(fields=['app_id'], name='api_apps_app_id_4c0254_idx'),
        ),
        migrations.AddIndex(
            model_name='apps',
            index=models.Index(fields=['id', 'user_id', 'type'], name='api_apps_id_226a6b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='appiosdeveloperinfo',
            unique_together={('user_id', 'issuer_id')},
        ),
    ]
