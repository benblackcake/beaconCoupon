from django.urls import path,include
from beaconDashboard import dashboard_views
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# from rest_framework.authtoken import views
app_name='beaconDashboard'
router = DefaultRouter()
# router.register('beaconlist', dashboard_views.BeaconListViewSet)
router.register('userlist',dashboard_views.CouponViewSerialize)
router.register('couponbasiclist',dashboard_views.CouponBasicView)
router.register('collectList',dashboard_views.UserCollectList)
router.register('userreg',dashboard_views.CreateUser)
router.register('basicuserlogin',dashboard_views.ValidateBasicUser)
router.register('staffregist',dashboard_views.CreateStaffUser)
router.register('devicelist',dashboard_views.DeviceList)
router.register('userbehavior',dashboard_views.UserBehaviorList)

# handler403 = dashboard_views.handler404s
handler403 = dashboard_views.response_error_handler
urlpatterns=[
    path('api/',include(router.urls),name='api'),
    path('api-auth',include('rest_framework.urls',namespace='rest_framework')),
    path('', dashboard_views.BeaconHomeAPIview.as_view(), name='index'),
    path('coupondetial/<id>', dashboard_views.CouponDetiallView.as_view(), name='coupondetial'),
    # path('list', dashboard_views.BeaconListAPIview.as_view(), name='list'),
    path('newbeacondata/', dashboard_views.CouponCreate.as_view(), name='newbeacondata'),
    path('datatable', dashboard_views.CouponDatatable.as_view(), name='datatable'),
    # path('testregist',dashboard_views.CreateUser.as_view(),name='testregist'),
    path('testlogin',dashboard_views.ValidateStaffUser.as_view(),name='testlogin'),
    path('testlogout',dashboard_views.ValidateStaffUserLogout.as_view(),name='testlogout'),
    path('devicelist',dashboard_views.DeviceView.as_view(),name='devicelist'),
    path('useranalysis',dashboard_views.UserBehaviorView.as_view(),name='useranalsis'),
    path('403/', dashboard_views.permission_denied_view),
    # path('newbeacondata/<pk>',dashboard_views.BeaconListDetialAPIview.as_view(),name='newbeacondataDetial'),
]