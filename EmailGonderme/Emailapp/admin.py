from django.contrib import admin
from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class EmailAdmin(admin.ModelAdmin):
    class Meta:
        model = CustomUser