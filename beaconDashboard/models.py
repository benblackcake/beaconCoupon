# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class AppAnsList(models.Model):
    ans_id = models.IntegerField(primary_key=True)
    ans_topic = models.CharField(max_length=20, blank=True, null=True)
    ans_content = models.TextField(blank=True, null=True)
    ans_time = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(unique=True, blank=True, null=True)
    store_id = models.IntegerField(unique=True, blank=True, null=True)
    manager_id = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app ans_list'


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
    head_image = models.CharField(max_length=200,blank=True, null=True)
    fb_id = models.CharField(max_length=50,blank=True, null=True)
    google_id = models.CharField(max_length=50,blank=True, null=True)

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
    # id=models.IntegerField(auto_created=True)
    device_name=models.CharField(max_length=10,null=True)
    device_id = models.CharField(max_length=70)
    access_token = models.CharField(max_length=70)
    device_check = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    def checkS(self):
        return BeaconList.objects.filter(device_check=True)
    class Meta:
        managed = False
        db_table = 'beacon_list'


class BigCatlogList(models.Model):
    catlog_id = models.IntegerField(primary_key=True)
    catlog_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'big_catlog_list'


class CollectList(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    # coupon_name = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    path_to_coupon_image_url_link = models.ForeignKey('CouponList', models.DO_NOTHING, db_column='path_to_coupon_image_url_link', blank=True, null=True)
    # event = models.ForeignKey('EventList', models.DO_NOTHING, blank=True, null=True)
    # beacon_list = models.ForeignKey(BeaconList, models.DO_NOTHING, blank=True, null=True)
    # catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collect_list'


'''

'''
class CouponList(models.Model):
    # id = models.AutoField(primary_key=True)
    # coupon_image_url_link = models.CharField(unique=True, db_column='coupon_image_url_link',max_length=60)
    coupon_image_url_link=models.FileField(unique=True, db_column='coupon_image_url_link',upload_to="django_beacon_test/images", null=True, blank=True)
    path_to_coupon_image_url_link = models.CharField(db_column='path_to_coupon_image_url_link',max_length=100, blank=True, null=True)
    uuid=models.UUIDField(default=uuid.uuid4,editable=True)
    # coupon_image_url_link_file = models.CharField(max_length=100)
    # coupon_image_url_link_file = models.FileField(blank=False, null=False)
    coupon_name = models.CharField(max_length=10,db_column='coupon_name', blank=True, null=True)
    coupon_content = models.TextField(blank=True, null=True)
    coupon_dismoney = models.IntegerField(blank=True, null=True)
    # coupon_class = models.CharField(max_length=5, blank=True, null=True)
    coupon_s_time = models.DateField(blank=True, null=True)
    coupon_e_time = models.DateField(blank=True, null=True)
    store = models.ForeignKey('StoreList', models.DO_NOTHING, blank=True, null=True)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    beacon_list = models.ForeignKey(BeaconList, models.DO_NOTHING, blank=True, null=True)
    catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, blank=True, null=True)
    def __unicode__(self):
        return self.path_to_coupon_image_url_link
    def get_absolute_url(self):
        return "/%s/" % self.id
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
    event_id = models.IntegerField(primary_key=True)
    event_image_url = models.CharField(max_length=30, blank=True, null=True)
    event_title = models.CharField(max_length=20, blank=True, null=True)
    event_content = models.CharField(max_length=200, blank=True, null=True)
    # event_catelog = models.CharField(max_length=4, blank=True, null=True)
    event_s_time = models.DateTimeField(blank=True, null=True)
    event_e_time = models.DateTimeField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    store = models.ForeignKey('StoreList', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UserList', models.DO_NOTHING, blank=True, null=True)
    beacon_list = models.ForeignKey(BeaconList, models.DO_NOTHING, blank=True, null=True)
    catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event_list'


class ManagetList(models.Model):
    manager_id = models.IntegerField(unique=True, blank=True, null=True)
    manager_name = models.CharField(max_length=20, blank=True, null=True)
    manager_account = models.CharField(primary_key=True, max_length=20)
    manager_password = models.CharField(max_length=20, blank=True, null=True)
    manager_phone = models.CharField(max_length=20, blank=True, null=True)
    manager_email = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'managet_list'


class StoreList(models.Model):
    store_id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=20, blank=True, null=True)
    store_account = models.CharField(max_length=20, blank=True, null=True)
    store_password = models.CharField(max_length=20, blank=True, null=True)
    manager_account = models.ForeignKey(ManagetList, models.DO_NOTHING, db_column='manager_account', blank=True, null=True)
    catlog = models.ForeignKey(BigCatlogList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_list'

class SuggId(models.Model):
    sugg_id = models.IntegerField(primary_key=True)
    sugg_catlog = models.CharField(db_column='sugg_ catlog', max_length=5, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    sugg_number = models.CharField(max_length=20, blank=True, null=True)
    sugg_content = models.TextField(blank=True, null=True)
    sugg_date = models.CharField(max_length=20, blank=True, null=True)
    sugg_time = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('UserList', models.DO_NOTHING, blank=True, null=True)
    store = models.ForeignKey(StoreList, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sugg_id'

class UserBehavior(models.Model):
    # id=models.IntegerField(primary_key=True)
    path_to_coupon_image_url_link = models.CharField(primary_key=True, max_length=100)
    user_id = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id', blank=True, null=True)
    # path_to_coupon_image_url_link = models.ForeignKey(CouponList, models.DO_NOTHING,
    #                                                   db_column='path_to_coupon_image_url_link', blank=True,
    #                                                   null=True)
    user_click_event_time = models.IntegerField(blank=True, null=True)
    user_click_coupon_time = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'user_behavior'

#
class UserList(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    user_fb_id = models.CharField(max_length=30, blank=True, null=True)
    user_go_id = models.CharField(max_length=40, blank=True, null=True)
    user_gender = models.CharField(max_length=10, blank=True, null=True)
    user_email_id = models.CharField(max_length=30, blank=True, null=True)
    user_address = models.CharField(max_length=30, blank=True, null=True)
    user_birthday = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_list'
