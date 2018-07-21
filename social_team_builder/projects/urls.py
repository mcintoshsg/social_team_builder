from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'all/$', views.AllProjectsView.as_view(), name='all'),
    url(r'new/$', views.NewProjectView.as_view(), name='new'),
    url(r'detail/(?P<pk>\d+)$', views.ProjectDetailView.as_view(),
        name='detail'),
    url(r'delete/$', views.DeleteProjectView.as_view(), name='delete'),
    url(r'edit/$', views.EditProjectView.as_view(), name='edit'),
    url(r'apply/(?P<pk>\d+)$', views.ApplyView.as_view(), name='apply'),
    url(r"applications/", views.ApplicationsView.as_view(),
        name='applications'),
]
