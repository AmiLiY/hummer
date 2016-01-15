from django.conf.urls import include, url
from rest_framework import routers
from restapi.views import (UserViewSet, ProjectViewSet, ImageViewSet,
    ApplicationViewSet, PortViewSet, ResourceLimitViewSet, VolumeViewSet,
    is_authenticated)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet, base_name='project')
router.register(r'projects/(?P<pid>[0-9]+)/images', ImageViewSet,
    base_name='image')
router.register(r'projects/(?P<pid>[0-9]+)/applications', ApplicationViewSet,
    base_name='application')
router.register(r'projects/(?P<pid>[0-9]+)/volumes', VolumeViewSet,
    base_name='volume')
router.register(r'resourcelimits', ResourceLimitViewSet,
    base_name='resourcelimit')

set_password = UserViewSet.as_view({
    'post': 'set_password'
})

port_list = PortViewSet.as_view({
    'get': 'list'
})
port_detail = PortViewSet.as_view({
    'get': 'retrieve'
})

volume_download = VolumeViewSet.as_view({
    'get': 'download'
})
volume_upload = VolumeViewSet.as_view({
    'post': 'upload'
})
pod_list = ApplicationViewSet.as_view({
    'get': 'pod_lists'
})

urlpatterns = [
    # Examples:
    # url(r'^$', 'hummer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include(router.urls)),

    # user
    url(r'users/(?P<pk>[0-9]+)/set_password/$', set_password,
        name='set-password'),
    url(r'auth/is_authenticated/$', is_authenticated, name='is_authenticated'),

    # pod
    url(r'projects/(?P<pid>[0-9]+)/applications/(?P<pk>[0-9]+)/pods/$',
        pod_list, name='pod-list'),

    # port
    url(r'projects/(?P<pid>[0-9]+)/applications/(?P<aid>[0-9]+)/ports/$',
        port_list, name='port-list'),
    url(r'projects/(?P<pid>[0-9]+)/applications/(?P<aid>[0-9]+)/ports/\
(?P<pk>[0-9]+)/$',
        port_detail, name='port-detail'),

    # volume
    url(r'projects/(?P<pid>[0-9]+)/volumes/(?P<pk>[0-9]+)/download/$',
        volume_download, name='volume-download'),
    url(r'projects/(?P<pid>[0-9]+)/volumes/(?P<pk>[0-9]+)/upload/$',
        volume_upload, name='volume-upload'),

    # auth
    url(r'auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]
