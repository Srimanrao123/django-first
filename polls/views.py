from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.db import models
from django.db.models import Count
from oauth2_provider.decorators import protected_resource
import json

from polls.models import NetworkTraffic, ResourceUsage, Alert, Server



@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
@protected_resource(['superuser'])
def dummy_view(request):
    print("Call to dummy_view")
    return Response({"message": "Authenticated access granted!"})

@api_view(["GET"])
def servers_severity(request,serverid):
    server1=Server.objects.get(id=serverid)
    severity = Alert.objects.filter(server=server1).values('severity').annotate(count=Count('severity'))
    severity_summary = {}
    for item in severity:
        severity_summary[item['severity']] = item['count']
    return Response(severity_summary)
@api_view(["GET"])
def servers_all(request):
    server1=Server.objects.all()
    server_list = []
    for server in server1:
        server_data = {
            'id': server.id,
            'name_of_server': server.name_of_server,
            'ip_address': server.ip_address,
            'location': server.location,
            'description': server.description,
            'tag': server.tag,
            'created_at': server.created_at,
            'is_active': server.is_active
        }
        server_list.append(server_data)
    return Response(server_list)
@api_view(["GET"])
def server_usage(request,serverid):
    server1=Server.objects.get(id=serverid)
    resource_usage = ResourceUsage.objects.get(server_id=server1)
    
    usage_data = {
        'timestamp': resource_usage.timestamp,
        'cpu_usage_percent': resource_usage.cpu_usage_percent,
        'ram_usage_percent': resource_usage.ram_usage_percent,
        'disk_usage_percent': resource_usage.disk_usage_percent,
        'app_usage_percent': resource_usage.app_usage_percent
    }
    
    return Response(usage_data)

@api_view(["GET"])
def server_network_traffic(request,serverid):
    server1=Server.objects.get(id=serverid)
    network_traffic = NetworkTraffic.objects.get(server_id=server1)
    
    traffic_data = {
        'timestamp': network_traffic.timestamp,
        'incoming_traffic_mb': network_traffic.incoming_traffic_mb
    }
    
    return Response(traffic_data)
@api_view(["GET"])
def usage_between_dates(request,serverid):
    server1=Server.objects.get(id=serverid)
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    resource_usages = ResourceUsage.objects.filter(server_id=server1, timestamp__range=[start_date, end_date])
    
    usage_data = []
    for resource_usage in resource_usages:
        data = {
            'timestamp': resource_usage.timestamp,
            'cpu_usage_percent': resource_usage.cpu_usage_percent,
            'ram_usage_percent': resource_usage.ram_usage_percent,
            'disk_usage_percent': resource_usage.disk_usage_percent,
            'app_usage_percent': resource_usage.app_usage_percent
        }
        usage_data.append(data)
    
    return Response(usage_data)