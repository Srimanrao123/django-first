from django.db import models


from datetime import date

class Server(models.Model):
    name_of_server=models.CharField(max_length=100,null=False)
    ip_address=models.CharField(null=False,max_length=20)
    location=models.CharField(max_length=50)
    description=models.TextField()
    tag=models.CharField(max_length=50)
    created_at=models.DateField(default=date.today)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name_of_server
    
class Alert(models.Model):
    server=models.ForeignKey(Server,on_delete=models.CASCADE)
    hh={
        "low":"low",
        "medium":"medium",
        "critical":"critical"
    }
    severity=models.CharField(choices=hh,max_length=10)
    messege_alert=models.TextField()
    created_at=models.DateField(date.today)
    def __str__(self):
        return self.severity


class ResourceUsage(models.Model):
    server_id=models.ForeignKey(Server,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(null=False)
    cpu_usage_percent=models.FloatField()
    ram_usage_percent=models.FloatField()
    disk_usage_percent=models.FloatField()
    app_usage_percent=models.FloatField()
    def __str__(self):
        return str(self.server_id)


class NetworkTraffic(models.Model):
    server_id=models.ForeignKey(Server,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(null=False)
    incoming_traffic_mb=models.FloatField()
    def __str__(self):
        return str(self.server_id)

