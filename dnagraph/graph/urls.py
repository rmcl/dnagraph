from django.conf.urls import patterns, include, url

urlpatterns = patterns('graph.views',
    url(r'^show/(?P<node_id>[\d]+)/repeatmasker/$', 'exec_repeatmasker', name='repeatmasker'),
    url(r'^show/(?P<node_id>[\d]+)/$', 'show', name='show_node'),
)
