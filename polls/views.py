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
@authentication_classes([OAuth2Authentication])
def servers_severity(request,serverid):
    try:
        server1=Server.objects.get(id=serverid)
        severity = Alert.objects.filter(server=server1).values('severity').annotate(count=Count('severity'))
        severity_summary = {}
        for item in severity:
            severity_summary[item['severity']] = item['count']
        return Response(severity_summary)
    except:
         return Response({"message":"invalid serverid"},status=404)
@api_view(["GET"])
@authentication_classes([OAuth2Authentication])

def servers_all(request):
    try:
        server1=Server.objects.all().order_by('-created_at')
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
    except:
        Response({"message":"servers not added"},status=400)


@api_view(["POST"])
@authentication_classes([OAuth2Authentication])

def add_server(request):
    data = request.data
    try:
        q=Server.objects.create(name_of_server=data["name_of_server"],
                                 ip_address=data["ip_address"],
                                 location=data["location"],
                                 description=data["description"],
                                 tag=data["tag"]
                         )
    
        return Response({"message":f"server id is :{q.id}"},status=202)
    except:
        return Response({"message":"error"},status=400)
@api_view(["PUT"])
@authentication_classes([OAuth2Authentication])

def update_server(request):
    data = request.data
    try:
        q=Server.objects.get(id=data["id"])
        q.name_of_server=data["name_of_server"]

        q.ip_address=data["ip_address"]
        q.location=data["location"]
        q.description=data["description"]
        q.tag=data["tag"]
        q.save()
    
        return Response({"message":f"server id is :{q.id} is updated"},status=202)
    except:
        return Response({"message":"error"},status=400)


    
@api_view(["GET"])
@authentication_classes([OAuth2Authentication])

def server_usage(request,serverid):
    try:
        server1=Server.objects.get(id=serverid)
        resource_usage = ResourceUsage.objects.filter(server_id=server1).order_by('timestamp')[0]
        
        
        usage_data = {
            'timestamp': resource_usage.timestamp,
            'cpu_usage_percent': resource_usage.cpu_usage_percent,
            'ram_usage_percent': resource_usage.ram_usage_percent,
            'disk_usage_percent': resource_usage.disk_usage_percent,
            'app_usage_percent': resource_usage.app_usage_percent
        }
        
        return Response(usage_data,status=200)
    except:
        Response({"message":"no usage found"},status=400)

@api_view(["GET"])
@authentication_classes([OAuth2Authentication])

def server_network_traffic(request,serverid):
    try:
        server1=Server.objects.get(id=serverid)
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        network_traffic = NetworkTraffic.objects.filter(server_id=server1, timestamp__range=[start_date,end_date]).order_by('-timestamp')
        list1=[]
        for item in network_traffic:
            traffic_data = {
            'timestamp': item.timestamp,
            'incoming_traffic_mb': item.incoming_traffic_mb}
            list1.append(traffic_data)
        
        
        return Response(list1)
    except:
            Response({"message":"no network found between these days"},status=404)


@api_view(["GET"])
def usage_between_dates(request,serverid):
    try:
        server1=Server.objects.get(id=serverid)
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        resource_usages = ResourceUsage.objects.filter(server_id=server1, timestamp__range=[start_date, end_date]).order_by('-timestamp')
        
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
    except:
        return Response({"message":"no network found between these days"},status=404)