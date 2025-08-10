from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('user_type', 'profile_picture', 'address_line1', 'city', 'state', 'pincode')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)



from .models import Category, BlogPost
admin.site.register(Category)
admin.site.register(BlogPost)
