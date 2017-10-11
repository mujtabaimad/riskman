from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^new/$', views.add_case),
    url(r'^(?P<id>[0-9]+)/risks/$', views.add_risk),
    url(r'^(?P<id>[0-9]+)/risks/delete/(?P<t_id>[0-9]+)$', views.del_risk),
    url(r'^(?P<id>[0-9]+)/risks/edit/(?P<t_id>[0-9]+)$', views.edit_risk),
    #
    # url(r'^(?P<id>[0-9]+)/order$', views.order),
    # url(r'^order_task$', views.order_tasks),
]
