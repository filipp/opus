from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opus2.views.home', name='home'),
    # url(r'^opus2/', include('opus2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^timer/$', 'timer.views.labels'),
    url(r'^timer/events/(\d+)/$', 'timer.views.view_event'),
    url(r'^timer/events/(\d+)/delete/$', 'timer.views.delete_event'),
    url(r'^timer/label/(\d+)/events/$', 'timer.views.events'),
    url(r'^timer/labels/$', 'timer.views.labels'),
    url(r'^timer/labels/new/$', 'timer.views.edit_label'),

    url(r'^alarm/$', 'timer.views.alarm'),

    url(r'^notes/$', 'notes.views.index'),
    url(r'^notes/tag/(\d+)/$', 'notes.views.index'),
    
    url(r'^notes/(\d+)/$', 'notes.views.view'),
    url(r'^notes/new/$', 'notes.views.edit'),
    url(r'^notes/(\d+)/edit/$', 'notes.views.edit'),
)
