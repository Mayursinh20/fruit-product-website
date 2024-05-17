from django.contrib import admin
from .models import User

# Register your models here.
# admin.site.register(User)

# For the sake of beautify we are overriding the things here
# else just remove entire below code and uncomment the above code
# admin.site.register(User)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "username", "mobile_number"]
    list_filter = ["is_superuser", "is_active", "is_staff"]
    fieldsets = [
        (
            "Personal info",
            {
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "mobile_number",
                    "gender",
                    "birth_date",
                    "marital_status",
                    "address",
                    "otp",
                    "date_joined",
                    "last_login",
                    "password",
                ]
            },
        ),
        ("Permissions", {"fields": ["is_superuser", "is_active", "is_staff"]}),
    ]
    # Show fields when creating users
    add_fieldsets = [
        (
            "Required Fields",
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "mobile_number",
                    "gender",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email", "username", "mobile_number"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
