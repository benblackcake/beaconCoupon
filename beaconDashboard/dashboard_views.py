import json
import pymysql
from datetime import time, datetime

from django.contrib.auth.models import User

from django.shortcuts import render,render_to_response,redirect
from django.http import Http404, HttpResponse, response

# from beaconDashboard import bitly
from rest_framework.exceptions import ValidationError, PermissionDenied

from beaconDashboard.models import BeaconList, CouponList, CollectList, AuthtokenToken, UserBehavior
from beaconDashboard.serializers import CouponSerialize, UserSerializer, StaffUserAuth, \
    CollectCoupon, \
    CouponSer, Collectser, BasicUserAuth, StaffSerializer, DeviceSer, UserBehaviorSer
from rest_framework import viewsets, generics, serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth import login, logout

# from django_bitly.models import Bittle
from django.conf import settings
from beaconDashboard import bitly_api
from django.db import connection, transaction, IntegrityError
from apiCall import EncodeEddystone,CallApi
# from rest_framework.views import exception_handler
# from django.conf.urls.static import static



debug='__DEBUG__'

class BeaconHomeAPIview(APIView):
    # authentication_classes = (TokenAuthentication)
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    permission_classes = [permissions.AllowAny]
    renderer_classes =[TemplateHTMLRenderer]
    template_name='index.html'
    def get(self,request,format=None):
        now = datetime.now()
        # print(self.request.user)
        content = {
            'user': request.user,  # `django.contrib.auth.User` instance.
            'auth': request.auth,  # None
        }
        print(debug+ "User: "+str(self.request.user))
        queryset = CouponList.objects.filter(user_id=self.request.user.id).all()#Use filter to get current user beaconList
        # print(queryset)
        # return Response()
        return Response({'datas':queryset,
                         'time':now.strftime("%Y-%m-%d %H:%M:%S")})

    def post(self, request, *args, **kwargs):
        # BeaconList.objects.all()
        device=BeaconList.objects.filter(user_id=self.request.user.id,device_check=True)
        callDeviceID=device.values('device_id').get()
        callDeviceToken=device.values('access_token').get()
        print(callDeviceID['device_id'])
        reqAPI=CallApi.CallApi(callDeviceID['device_id'],callDeviceToken['access_token'])

        print(debug +request.POST.get('path_to_coupon_image_url_link'))
        orig=request.POST.get('path_to_coupon_image_url_link')
        res = EncodeEddystone.EncodeEddyston.strTohex(orig)
        jsonData=json.dumps({"en": "1",
                       "url": res
                       })
        # print(jsonData)
        reqAPI.callFunction(jsonData)
        print(debug +str(res))
        return redirect("beaconDashboard:index")

class CouponDetiallView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    renderer_classes =[TemplateHTMLRenderer]
    template_name='coupondetial.html'
    def get(self,request,id):
        queryset = CouponList.objects.get(id=id)
        print(queryset.coupon_image_url_link.url)
        return Response({'datas':queryset})

'''
API: dashboard/newbeacondata
New coupon 
'''
class CouponCreate(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    renderer_classes =[TemplateHTMLRenderer]
    template_name='NewBeaconData.html'

    def permission_denied(self, request, message=None):
        print('1111')
        super().permission_denied(request, message)
        # return redirect()

    # username={}
    # parser_classes = (MultiPartParser, FormParser)

    def get(self,request):
        # raise PermissionDenied({"message":"You don't have permission to access"})

        return Response()

    #
    def post(self, request,*args,**kwargs):

        domin=request.build_absolute_uri('/')
        print(domin)

        serializer=CouponSerialize(data=request.data,
                                        context={'request': request})

        url=request.FILES['coupon_image_url_link']
        url.name=str(datetime.now().timestamp())+url.name
        filr=domin+'media/django_beacon_test/images/'+str(url.name)
        print(debug+filr)
        bitly=bitly_api.Connection(settings.BITLY_LOGIN,settings.BITLY_API_KEY)
        res=bitly.shorten(filr)
        print(res['url'])
        # print(settings)
        # print()
        if serializer.is_valid():
        #     print(self.request.user)
            serializer.save(user_id=self.request.user,
                            coupon_image_url_link=request.FILES['coupon_image_url_link'],
                            path_to_coupon_image_url_link=res['url']
                            )
            return redirect("beaconDashboard:datatable")
            # return Response(self.get_authenticate_header(request))
        return redirect("beaconDashboard:datatable")
        # return  self.get_authenticate_header(request)
            # return Response("list")
            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return redirect("list")
'''
API: dashboard/datatable
List down all coupon
'''
class CouponDatatable(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    renderer_classes =[TemplateHTMLRenderer]
    template_name='datatable.html'

    def get(self,request):
        print(debug+str(request.method))
        return Response()
    def post(self,request):
        print(debug)

'''
API dashboard/testregist
Regist new basic user
'''
class CreateUser(viewsets.ModelViewSet):
    # renderer_classes =[TemplateHTMLRenderer]
    template_name='basicUserReg.html'
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class=UserSerializer

    # def list(self, request, *args, **kwargs):
    #     serializer = UserSerializer
    #     return Response({'serializer': serializer})
    #
    def create(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            print(debug + "username"+request.data['username'])
            print(debug + "password"+request.data['password'])
            print(debug + "email"+request.data['email'])
            serializer.save()
            return HttpResponse({'Success'})
            # return Response({'data':serializer.data})
        return HttpResponse({'Unsuccess'})

    def list(self, request, *args, **kwargs):
        today=datetime.today()
        start_date = datetime(today.year, today.month, 1)
        # start_date=datetime.date(datetime.now())
        self.user=User.objects.filter(is_staff=0,date_joined__range=(start_date , datetime.now()))
        # self.user = User.objects.all()
        self.datelabel=[]
        serializer=self.get_serializer(self.user,many=True)
        print(serializer)
        # for i in datetime.month(datetime.now().date()):
        maxDay=datetime.now().max.day
        print(str(serializer.data))
        # print(datetime.now().month)
        # print(maxDay)
        li_ser=serializer.data
        li_date=[]
        for i in range(0,maxDay):
            li_date.append(0)
            self.datelabel.append(str(datetime.today().month)+"/"+str(i+1))

        for i in range(0,len(li_ser)):
            li_date[li_ser[i]-1]=li_date[li_ser[i]-1]+1

        print(li_date)
        print(len(li_date))
        print(self.datelabel)
        # print(datem)
        return Response({'data':li_date,
                         'labels':self.datelabel})
        # def get(self,request):
        #     serializer = UserSerializer
        #     return Response({'serializer': serializer})
    # def post(self,request,format=None):
    #     serializer=UserSerializer(data=request.data)
    #
    #     if serializer.is_valid():
    #         print(debug + "username"+request.data['username'])
    #         print(debug + "password"+request.data['password'])
    #         print(debug + "email"+request.data['email'])
    #         serializer.save()
    #         return HttpResponse({'Success'})
    #         # return Response({'data':serializer.data})
    #     return HttpResponse({'Unsuccess'})

class CreateStaffUser(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = StaffSerializer
    queryset = User.objects.all()
    def create(self, request, *args, **kwargs):
        try:
            user=User.objects.create(
                username=self.request.POST.get('username'),
                # password=validated_data['password'],
                email=self.request.POST.get('email'),
            )
            user.set_password(self.request.POST.get('password'))
            user.is_staff=True
            user.save()
        except IntegrityError:
            return HttpResponse({'unsuccess'})
        return HttpResponse({'success'})

'''
API: dashboard/testlogin
validate stuff user login
'''
class ValidateStaffUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='TestLogin.html'
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        serializer=StaffUserAuth
        return Response({'serializer': serializer})

    def post(self, request, format=None):
        try:
            serializer=StaffUserAuth(data=request.data)
            if serializer.is_valid():
                user=serializer.validate(request.data)
                # uer=AuthtokenToken.objects.filter(user_id=user).values('key')
                if user.is_staff:
                    print(user)
                    login(request,user)
                    return HttpResponse({'success'})
        except AssertionError:
            return HttpResponse({'unsuccess'})
        # logout(request.user)
        # return redirect("beaconDashboard:testlogin")

'''
API: dashboard/testlogout
'''
class ValidateStaffUserLogout(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name='logout.html'
    permission_classes = [permissions.AllowAny]

    def get(self,request,format=None):
        logout(request)
        return redirect("beaconDashboard:index")

'''
API :api/basicuserlogin
validata normal user
'''
class ValidateBasicUser(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = BasicUserAuth
    queryset = User.objects.all()#object.none()

    def create(self, request, *args, **kwargs):
        print(debug+ str(request.data))
        serializer=BasicUserAuth(data=request.data)
        try:
            if serializer.is_valid():
                user=serializer.validate(request.data)
                print(debug+"Login Success: "+str(user))
                # login(request,user)
                return HttpResponse({"Success"})
        except AssertionError:
            print('username or password error')
        return HttpResponse({"Unsuccess"})


'''
API :api/userlist
CRUD current IsAuthenticated user
'''
class CouponViewSerialize(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAdminUser,IsAuthenticated,)
    serializer_class = CouponSerialize
    queryset = CouponList.objects.all()

    def list(self, request, *args, **kwargs):

        user = self.request.user
        self.object_list=CouponList.objects.filter(user_id=user)
        serializer=self.get_serializer(self.object_list,many=True)
        # test=settings.MEDIA_URL+'django_beacon_test/images/kv.png'
        # print(test)
        return Response ({'data':serializer.data})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # user = serializer.validated_data[self.request.user]
            # token, create = Token.objects.get_or_create()
            print(self.request.user)
            serializer.save(user_id=self.request.user)
            return Response({'data': serializer.data})
        return Response({'data': serializer.data})
    # def update(self, request, *args, **kwargs):

    # def get_queryset(self):
    #     user=self.request.user
    #     return BeaconList.objects.filter(manager_account=user)

class CouponBasicView(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CouponSerialize
    queryset = CouponList.objects.all()
    def list(self, request, *args, **kwargs):
        self.object_list=CouponList.objects.all()
        serializer=self.get_serializer(self.object_list,many=True)
        return Response({'data': serializer.data})
    def create(self, request, *args, **kwargs):
        path_to_coupon_image_url_link = request.data['path_to_coupon_image_url_link']
        obj = CouponList.objects.filter(path_to_coupon_image_url_link=path_to_coupon_image_url_link)
        serializers=self.serializer_class(obj,many=True)
        return Response({'data':serializers.data})


'''
API: api/collectList
GET POST DELETE collectlist
'''
class UserCollectList(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = Collectser
    queryset = CollectList.objects.all()

    def rawSQLList(self,**kwargs):
        userID=kwargs.get('user_id')
        url=kwargs.get('path_to_coupon_image_url_link')

        result=CouponList.objects.raw('SELECT  t.id,t.path_to_coupon_image_url_link, '
                                      's.user_id,s.coupon_name, s.coupon_content,s.coupon_dismoney,s.coupon_s_time,s.coupon_e_time'
                                      ' FROM beacno_test.collect_list t '
                                      'INNER JOIN beacno_test.coupon_list s ON ( t.path_to_coupon_image_url_link = s.path_to_coupon_image_url_link )'
                                      'WHERE t.user_id=%s AND  CURDATE() >=coupon_s_time AND CURDATE()<=coupon_e_time ;',[userID])
        return result

    def create(self, request, *args, **kwargs):
        cursor = connection.cursor()
        raw='''
            INSERT INTO beacno_test.collect_list ( user_id, path_to_coupon_image_url_link) VALUES (%s,%s)
            ON DUPLICATE KEY UPDATE path_to_coupon_image_url_link=path_to_coupon_image_url_link;
            '''

        rawInsertBehavior = '''
                    INSERT INTO beacno_test.user_behavior 
                     ( user_id, path_to_coupon_image_url_link,user_click_coupon_time) VALUES (%s,%s,%s)
                     ON DUPLICATE KEY UPDATE user_click_coupon_time=user_click_coupon_time+1;
                     
                    '''
        #INSERT a new collected coupon
        user_id = self.request.user.id
        path_to_coupon_image_url_link = request.data['path_to_coupon_image_url_link']
        queryset=[user_id,path_to_coupon_image_url_link]
        cursor.execute(raw,queryset)
        transaction.commit()
        #UserBehavior click + 1
        obj = CouponList.objects.filter(path_to_coupon_image_url_link=path_to_coupon_image_url_link)
        u_id=User.objects.get(id=obj.values('user_id').get()['user_id'])

        querysetBehavior = [u_id.id, path_to_coupon_image_url_link, 1]
        cursor.execute(rawInsertBehavior, querysetBehavior)
        transaction.commit()
        # if times==0:
        #     querysetBehavior=[u_id.id,path_to_coupon_image_url_link,1]
        #     cursor.execute(rawInsertBehavior,querysetBehavior)
        #     transaction.commit()
        # else:
        #     querysetBehavior=[u_id.id,path_to_coupon_image_url_link,times+1]
        #     cursor.execute(rawInsertBehavior,querysetBehavior)
        #     transaction.commit()

        print(debug+"USER: "+str(request.user.username+" INSERT..."))
        print(debug+raw+str(queryset))
        #Return list of coupon who collect that
        ret=self.rawSQLList(user_id= self.request.user.id)
        print(ret)
        seret=CouponSer(ret,many=True)

        return Response({'data': seret.data})


    def list(self, request, *args, **kwargs):
        user = self.request.user
        print(debug+"User: "+str(user.username)+" SELECT....")
        data=self.rawSQLList(user_id= self.request.user.id)
        # url=CollectList.objects.filter(user_id=self.request.user).values('path_to_coupon_image_url_link')
        # print(url)
        print(debug+str(data))
        serializer = CouponSer(data,many=True)
        return Response({'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({"unsuccess"})
            pass
        # print(debug+kwargs.get('id'))
        return Response({"success"})

class DeviceList(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSer
    queryset = BeaconList.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # user = serializer.validated_data[self.request.user]
            # token, create = Token.objects.get_or_create()
            print(self.request.user)
            serializer.save(user_id=self.request.user)
            return Response({'data': serializer.data})
        return Response({'data': serializer.data})
    def list(self, request, *args, **kwargs):
        user = self.request.user
        self.object_list=BeaconList.objects.filter(user_id=user)
        serializer=self.get_serializer(self.object_list,many=True)
        # test=settings.MEDIA_URL+'django_beacon_test/images/kv.png'
        # print(test)
        return Response ({'data':serializer.data})

class DeviceView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes =[TemplateHTMLRenderer]
    template_name='devicelist.html'
    def get(self,request):
        return Response()

class UserBehaviorList(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBehaviorSer
    queryset = UserBehavior.objects.all()
    def list(self, request, *args, **kwargs):
        self.object_list=UserBehavior.objects.all()
        dit=dict()
        labels=[]
        dataset=[]
        for item in self.object_list.filter(user_id=self.request.user):
            dataset.append(item.user_click_coupon_time)

        for x in self.object_list.filter(user_id=self.request.user).values('path_to_coupon_image_url_link'):
            try:
                obj=CouponList.objects.filter(path_to_coupon_image_url_link=x['path_to_coupon_image_url_link'])
                # print(obj.values('coupon_name').get()['coupon_name'])
                labels.append(obj.values('coupon_name').get()['coupon_name'])
            except CouponList.DoesNotExist:
                pass

        print(labels)
        print(dataset)
        dit={
            'data':dataset,
            'labels':labels
        }
        # serializers=self.get_serializer(self.object_list,many=True)
        # print(self.get_serializer(self.object_list,many=True))
        # s={
        #     'data':serializers.data
        # }
        # print(s)
        return Response(dit)

class UserBehaviorView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes =[TemplateHTMLRenderer]
    template_name='useranalysis.html'
    def get(self,request):
        return Response()

def response_error_handler(request, exception=None):
    return HttpResponse('Error handler content', status=403)
def permission_denied_view(request):
    redirect('beaconDashboard:index')


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        print(response)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

''' 

'''