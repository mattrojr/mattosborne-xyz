from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^campaign/(?P<campaign_id>[0-9]+)/$', views.campaign, name='campaign'),
    url(r'^area/(?P<area_id>[0-9]+)/$', views.area, name='area'),
    url(r'^new_campaign/$', views.new_campaign, name='new_campaign'),
    url(r'^new_area/(?P<campaign_id>[0-9]+)/$', views.new_area, name='new_area'),
    url(r'^edit_campaign/(?P<campaign_id>[0-9]+)/$', views.edit_campaign, name='edit_campaign'),
    url(r'^edit_area/(?P<area_id>[0-9]+)/$', views.edit_area, name='edit_area'),
    url(r'^delete_campaign/(?P<campaign_id>[0-9]+)/$', views.delete_campaign, name='delete_campaign'),
    url(r'^delete_area/(?P<area_id>[0-9]+)/$', views.delete_area, name='delete_area'),
]