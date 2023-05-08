from django.urls import path
from . import views

 # RestAPI用
from rest_framework import routers
from .views import TestView ,anime2sketch_View, cv_img_trans_View
from .views import openaiCLIP_View, openaiCLIP_acync_View#, myAPI_asyncView

#defaultRouter = routers.DefaultRouter()
#defaultRouter.register('userInfo',UserInfoViewSet)

app_name = 'myapi'
urlpatterns = [
    #path('<int:id>', views.index_page, name='index_page'),
    path('test/', TestView.as_view(), name='test'),
    path('anime2sketch/', anime2sketch_View.as_view(), name='anime2sketch'),
    path('cv_img_trans/', cv_img_trans_View.as_view(), name='cv_img_trans'),
    path('openaiCLIP/', openaiCLIP_View.as_view(), name='openaiCLIP'),
    path('openaiCLIP_acync_View/', openaiCLIP_acync_View.as_view(), name='openaiCLIP_acync_View'),
    #path('myAPI_asyncView/', myAPI_asyncView.as_view(), name='myAPI_asyncView'),
    #path('category/', CategoryView.as_view(), name='category'),
]
