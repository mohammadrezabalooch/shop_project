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
        "is_author",
        "is_special_user",
    ]
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[2][1]["fields"] = UserAdmin.fieldsets[2][1]["fields"] + (
        "is_author",
        "special_user",
    )
    fieldsets = tuple(fieldsets)


admin.site.register(CustomUser, CustomUserAdmin)
