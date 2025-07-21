from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm

# Register your models here.
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = [
        "username",
        "email",
        "is_superuser",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
