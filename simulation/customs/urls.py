from django.urls import path

from . import views

urlpatterns = [
    path('', views.sim, name='sim'),
    path('my-ajax-test/', views.myajaxtestview, name='ajax-test-view'),
    path('my-ajax-test/2', views.myajaxtestview2, name='ajax-test-view2'),
    path('my-ajax-test/3', views.runsim, name='runsim'),
    path('my-ajax-test/4', views.pausesim, name='pausesim'),
    path('my-ajax-test/5', views.reset, name='reset'),
    path('my-ajax-test/6', views.retriveData, name='retriveData'),
    path('my-ajax-test/7', views.passParameter, name='passParameter'),
    path('my-ajax-test/8', views.deleteTuple, name='deleteTuple'),
    path('my-ajax-test/9', views.save, name='save'),
    path('my-ajax-test/10', views.saveAs, name='saveAs'),
    path('my-ajax-test/11', views.terminate, name='terminate'),
    path('my-ajax-test/12', views.getServiceTime, name='getServiceTime'),
    path('my-ajax-test/13', views.getClientInterval, name='getClientInterval'),
    path('my-ajax-test/14', views.checkArraySize, name='checkArraySize'),
    path('my-ajax-test/15', views.adjustArray, name='adjustArray'),
]