from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'all/$', views.AllProjectsView.as_view(), name='all'),
    url(r'new/$', views.NewProjectView.as_view(), name='new'),
    url(r'detail/(?P<pk>\d+)$', views.ProjectDetailView.as_view(),
        name='detail'),
    url(r'delete/(?P<pk>\d+)$', views.DeleteProjectView.as_view(),
        name='delete'),
    url(r'edit/(?P<pk>\d+)$', views.EditProjectView.as_view(), name='edit'),
    url(r'apply/(?P<pk>\d+)$', views.ApplyView.as_view(), name='apply'),
    url(r'applications/', views.ApplicationsView.as_view(),
        name='applications'),
    url(r'accept/(?P<decision>\d+)/(?P<id>\d+)/(?P<pk>\d+)/$',
        views.ApplicationAcceptView.as_view(),
        name='accept'),
    url(r'search/$', views.SearchProjectView.as_view(), name='search'),    
    url(r'filter/(?P<pk>\d+)$', views.FilterProjectView.as_view(),
        name='filter'),
    url(r'completed/(?P<pk>\d+)$', views.CompletedProjectView.as_view(),
        name='completed'),
    url(r'add_skill/$', views.AddSkillView.as_view(),
        name='add_skill'),
]
