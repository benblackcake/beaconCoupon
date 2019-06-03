# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class BeaconList(models.Model):
    beacon_id = models.CharField(max_length=40)
    beacon_image_url = models.CharField(max_length=50, blank=True, null=True)
    manager_account = models.ForeignKey(User, models.DO_NOTHING, db_column='manager_account', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beacon_list'



class BigCatlogList(models.Model):
    catlog_id = models.CharField(primary_key=True, max_length=10)
    catlog_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'big_catlog_list'


class CollectList(models.Model):
    collect_id = models.CharField(primary_key=True, max_length=10)
    collect_name = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('UserList', models.DO_NOTHING)
    coupon = models.ForeignKey('CouponList', models.DO_NOTHING, blank=True, null=True)
    event = models.ForeignKey('EventList', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collect_list'


class CouponList(models.Model):
    coupon_id = models.CharField(primary_key=True, max_length=10)
    coupon_name = models.CharField(max_length=10, blank=True, null=True)
    coupon_image_url_link = models.CharField(max_length=50, blank=True, null=True)
    coupon_content = models.CharField(max_length=60, blank=True, null=True)
    coupon_dismoney = models.IntegerField(blank=True, null=True)
    coupon_s_time = models.DateTimeField(blank=True, null=True)
    coupon_e_time = models.DateTimeField(blank=True, null=True)
    coupon_catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, db_column='coupon_catlog', blank=True, null=True)
    manager_account = models.ForeignKey('ManagetList', models.DO_NOTHING, db_column='manager_account', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupon_list'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventList(models.Model):
    event_id = models.CharField(primary_key=True, max_length=10)
    event_title = models.CharField(max_length=20, blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    event_s_time = models.DateTimeField(blank=True, null=True)
    event_e_time = models.DateTimeField(blank=True, null=True)
    event_content = models.CharField(max_length=200, blank=True, null=True)
    event_image_url = models.CharField(max_length=30, blank=True, null=True)
    event_catelog = models.CharField(max_length=4, blank=True, null=True)
    manager_account = models.ForeignKey('ManagetList', models.DO_NOTHING, db_column='manager_account', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_list'


class ManagetList(models.Model):
    manager_account = models.CharField(primary_key=True, max_length=10)
    manager_password = models.CharField(max_length=50, blank=True, null=True)
    manager_name = models.CharField(max_length=10, blank=True, null=True)
    manager_phone = models.CharField(max_length=10, blank=True, null=True)
    manager_email = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'managet_list'


class ShareList(models.Model):
    share_id = models.CharField(primary_key=True, max_length=10)
    share_name = models.CharField(max_length=30, blank=True, null=True)
    share_content = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'share_list'


class StoreList(models.Model):
    store_id = models.CharField(primary_key=True, max_length=20)
    store_name = models.CharField(max_length=50, blank=True, null=True)
    store_catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, db_column='store_catlog', blank=True, null=True)
    manager_account = models.ForeignKey(ManagetList, models.DO_NOTHING, db_column='manager_account', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_list'


class UserBehavior(models.Model):
    user = models.ForeignKey('UserList', models.DO_NOTHING, primary_key=True)
    user_click_catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, db_column='user_click_catlog', blank=True, null=True)
    user_click_catlog_times = models.CharField(max_length=50, blank=True, null=True)
    user_click_event = models.ForeignKey(EventList, models.DO_NOTHING, db_column='user_click_event', blank=True, null=True)
    user_click_event_times = models.CharField(max_length=50, blank=True, null=True)
    user_click_coupon = models.ForeignKey(CouponList, models.DO_NOTHING, db_column='user_click_coupon', blank=True, null=True)
    user_click_coupon_times = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_behavior'


class UserList(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_gender = models.CharField(max_length=10, blank=True, null=True)
    user_fb_id = models.CharField(max_length=30, blank=True, null=True)
    user_go_id = models.CharField(max_length=40, blank=True, null=True)
    user_email_id = models.CharField(max_length=30, blank=True, null=True)
    user_beacon_id = models.CharField(max_length=40, blank=True, null=True)
    share = models.ForeignKey(ShareList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_list'
