from django.conf.urls import url
from . import views
urlpatterns = [
    # 用户注册
    # 使用命名空间之后，reverse(users:register) == '/register/' 就可以进行反向解析了，如果路由有改动也不会影响命名空间
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    # 获取url参数，通过正则匹配到username，然后传递给P<username>
    url(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',views.UsernameCountView.as_view()),
]