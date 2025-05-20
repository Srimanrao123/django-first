from django.contrib import admin

# Register your models here.


from .models import NetworkTraffic, ResourceUsage, Alert, Server


admin.site.register(NetworkTraffic)
admin.site.register(ResourceUsage)
admin.site.register(Alert)
admin.site.register(Server)

