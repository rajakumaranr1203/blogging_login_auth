from  django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['email','username','name','is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields': ('name',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields':('name',)}),
    )
    
    
    
admin.site.register(CustomUser,CustomUserAdmin)
