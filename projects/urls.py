from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^new/$', views.add_project),
    url(r'^(?P<id>[0-9]+)/tasks/$', views.add_task),
    url(r'^(?P<id>[0-9]+)/tasks/delete/(?P<t_id>[0-9]+)$', views.del_task),
    url(r'^(?P<id>[0-9]+)/tasks/edit/(?P<t_id>[0-9]+)$', views.edit_task),

    url(r'^(?P<id>[0-9]+)/order$', views.order),
    url(r'^order_task$', views.order_tasks),
]
