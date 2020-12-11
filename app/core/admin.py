from django.contrib import admin

from core import models

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    read_only_fields =('id',)

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Transaction)
