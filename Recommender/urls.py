from django.conf.urls import patterns, url
from Recommender import views

urlpatterns = patterns('',
    url(r'^$', views.DataEntry, name='data_entry'),
    url(r'^successful_entry$', views.SuccessfulEntry, name='successful_entry'),
)