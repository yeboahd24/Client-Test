from django.contrib import admin
from .models import Developer,ProjectManager,User,Ticket

# Register your models here.
admin.site.register(Developer)
admin.site.register(ProjectManager)
admin.site.register(User)
admin.site.register(Ticket)