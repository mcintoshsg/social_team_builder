from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'signout/$', views.SignOutView.as_view(), name='signout'),
    url(r'signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'profile/(?P<pk>\d+)/$', views.ProfileView.as_view(),
        name='profile'),
    url(r'edit/(?P<pk>\d+)/$', views.EditProfileView.as_view(),
        name='edit'),
]
