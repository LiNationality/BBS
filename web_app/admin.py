from django.contrib import admin

# Register your models here.
from web_app import models

class u_serInfo(admin.ModelAdmin):
    list_display = (
        'user_id','name','nickname','email','avatar'
    )
    list_per_page = 10
    search_fields = ('username',)
    list_display_links = ['user_id']
    list_editable = ['name']
    list_filter = ['user_id']
admin.site.register(models.User)
admin.site.register(models.UserInfo,u_serInfo)
admin.site.register(models.Topic)
admin.site.register(models.Announcement)
admin.site.register(models.Kind)
admin.site.register(models.Reply)

