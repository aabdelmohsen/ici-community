from django.urls import path, re_path
from . import views
from sport.views import PlayerList, Daily_ScanList


urlpatterns = [
    path('', views.home, name='sport-home'),
    path('scanner', views.scanner, name='security-scanner'),
    path('player_list/', PlayerList.as_view(), name='player_list'),
    path('getqrcode/<int:id>/', views.getqrcode, name='getqrcode'),
    path('scanmenow/<int:id>/', views.scanmenow, name='scanmenow'),
    path('daily_scan/', Daily_ScanList.as_view(), name='daily_scan'),
]
