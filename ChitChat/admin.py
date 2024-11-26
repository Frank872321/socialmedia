from django.contrib import admin
from .models import Room, Message
# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'admin')
    filter_horizontal = ('members',)  # Enables a better UI for ManyToMany field