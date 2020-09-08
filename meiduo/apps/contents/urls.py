from django.conf.urls import url
from . import views
urlpatterns = [
    # 首页的广告 / 根路径
    url(r'^$',views.IndexView.as_view(),name='index')
]