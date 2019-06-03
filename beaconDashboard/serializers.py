from rest_framework.validators import UniqueValidator


from beaconDashboard.models import BeaconList, CouponList, CollectList, UserBehavior
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,get_permission_codename
from datetime import time, datetime
from rest_framework.authtoken.models import Token
import uuid
debug='__debug__'
ifdebug=False

class CouponSerialize(serializers.ModelSerializer):
    class Meta:
        model=CouponList
        fields=('id','uuid','path_to_coupon_image_url_link','coupon_image_url_link','coupon_name','user_id','coupon_dismoney','coupon_content'
                ,'coupon_s_time'
                ,'coupon_e_time')
    # def create(self, validated_data):
    #     CouponList.objects.create(**validated_data)
    # def create(self, validated_data):
    #     return super().create(validated_data)
    #
    # # def create(self, validated_data):
    #

    def update(self, instance, validated_data):
        instance.coupon_name = validated_data.get('coupon_name', instance.coupon_name)
        instance.coupon_content=validated_data.get('coupon_content',instance.coupon_content)
        instance.coupon_dismoney = validated_data.get('coupon_dismoney', instance.coupon_dismoney)
        instance.coupon_s_time=validated_data.get('coupon_s_time',instance.coupon_s_time)
        instance.coupon_e_time=validated_data.get('coupon_e_time',instance.coupon_e_time)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance
        # instance.coupon_name = validated_data.get('coupon_name', instance.coupon_name)

class UserSerializer(serializers.ModelSerializer):
    # username=serializers.CharField(max_length=20)
    password=serializers.CharField(write_only=True)
    # email=serializers.CharField(max_length=254)
    fb_id=serializers.CharField(max_length=50,default=None)
    google_id=serializers.CharField(max_length=50,default=None)
    head_image=serializers.CharField(max_length=200,default=None)
    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            # password=validated_data['password'],
            email=validated_data['email'],
            fb_id=validated_data['fb_id'],
            google_id=validated_data['google_id'],
            head_image=validated_data['head_image'],
            date_joined=datetime.now()
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model=User
        fields=('username','password','email','fb_id','google_id','head_image','date_joined')
        # fields = ('date_joined')
        # fields=('username','password','email')
    def to_representation(self, instance):
        # li_date=[]
        # iden = super().to_representation(instance)
        timePure=instance.date_joined
        time=datetime.date(timePure)
        # li_date.append(time)
        maxDay = datetime.now().max.day
        # print(li_date)
        # for i in range(1,maxDay):
        #     if i ==time.day:
        #         li_date.append(i)
        #     else:
        #         li_date.append(0)
        return int(time.day)

class StaffSerializer(serializers.ModelSerializer):
    # username=serializers.CharField(max_length=20)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=('username','password','email')
        # fields=('username','password','email')

class StaffUserAuth(serializers.Serializer):
    username=serializers.CharField(
        max_length=30,
        required=True
    )
    password=serializers.CharField(
        max_length=30,
        required=True,
        style={
            'input_type': 'password', 'placeholder': 'Password'
        }
    )
    def validate(self, attrs):
        credentials={
            'username':attrs.get('username'),
            'password':attrs.get('password')
        }
        if all(credentials.values()):
            user=authenticate(**credentials)

            # user
            # token=Token.objects.get(user=user)
            return(user)

class BasicUserAuth(serializers.Serializer):
    username=serializers.CharField(
        max_length=30,
        required=True
    )
    password=serializers.CharField(
        max_length=30,
        required=True,
    )
    def validate(self, attrs):
        credentials={
            'username':attrs.get('username'),
            'password':attrs.get('password')
        }
        if all(credentials.values()):
            try:
                user=authenticate(**credentials)
            except User.DoesNotExist:
                return (user)
            # user
            # token=Token.objects.get(user=user)
            return(user)

class NameSerializer(serializers.Serializer):

    coupon_name= serializers.CharField(
        max_length=30,
        required=True,

    )

    coupon_content=serializers.CharField(
        max_length=100,
        required=True,
    )
    coupon_dismoney=serializers.IntegerField(
        max_value=0
    )
    coupon_image_url_link=serializers.FileField(
        use_url=True,

    )
    uuid=serializers.UUIDField(default=uuid.uuid4())


class CouponSer(serializers.ModelSerializer):

    # coupon_image_url_link = serializers.PrimaryKeyRelatedField(read_only=True)
    # coupon_image_url_link = serializers.PrimaryKeyRelatedField(queryset=CouponList.objects.all(), required=False)
    # coupon_name=serializers.StringRelatedField(many=True)
    class Meta:
        model=CouponList
        fields = ('id','path_to_coupon_image_url_link','coupon_name','coupon_content','coupon_s_time','coupon_e_time','coupon_dismoney','user_id')
        # fields=('__all__')
class CollectCoupon(serializers.ModelSerializer):
    # coupon_image_url_link = serializers.PrimaryKeyRelatedField(queryset=CouponList.objects.all().select_related('coupon_image_url_link'),required=True)
    # coupon_name=serializers.StringRelatedField(many=True)
    couponDetial=CouponSer(source='coupon_image_url_link')
    # couponDtial=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=CollectList
        fields = ('coupon_image_url_link','couponDetial')
    def update(self, instance, validated_data):
        instance.coupon_image_url_link=validated_data.get('coupon_image_url_link',instance.coupon_image_url_link)
        instance.save()
        return instance
        # instance.coupon_image_url_link = validated_data.get('coupon_image_url_link', instance.coupon)

class Collectser(serializers.ModelSerializer):
    # coupon_image_url_links = CouponImgLink(source='coupon_image_url_link')
    # def to_internal_value(self, data):
    #     return super().to_internal_value(data)

    class Meta:
        model=CollectList
        fields=('__all__')


class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model=BeaconList
        fields=('__all__')


class UserBehaviorSer(serializers.ModelSerializer):
    class Meta:
        model=UserBehavior
        fields=('__all__')

    def to_representation(self, instance):
        iden=super().to_representation(instance)

        iden['url'] = iden['path_to_coupon_image_url_link']
        return iden


'''
    def validate(self, validated_data):
        print(debug,validated_data.get('coupon_image_url_link'))
        # validated_data['coupon_image_url_link']=self.data.get('coupon_image_url_link')
        coupon_image_url_link=CouponList.objects.filter(coupon_image_url_link=validated_data.get('coupon_image_url_link')).get()
        print(debug,coupon_image_url_link)
        res={'coupon_image_url_link':validated_data.get('coupon_image_url_link')
             }

        print(debug,res)
        return res

'''




