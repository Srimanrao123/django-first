from django.urls import path

from . import views

urlpatterns = [
    
    path("dummy_view/v1/",views.dummy_view),
    path("server/<int:serverid>",views.servers_severity),
    path("servers",views.servers_all),
    path("server/<int:serverid>/usage",views.server_usage),
    path("server/<int:serverid>/network",views.server_network_traffic),
    path("server/<int:serverid>/usage_between_dates",views.usage_between_dates),
    path("add_server",views.add_server),
    path("update_server",views.update_server),

    
]