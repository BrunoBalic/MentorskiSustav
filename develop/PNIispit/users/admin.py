from django.contrib import admin

from .models import Users

class UsersAdmin(admin.ModelAdmin):
    # ovdje upisem koja polja zelim imati u admin sucelju,
    # ako zelim sva, nemoram ovo pisati, sva budu po default-u
    # ovo sam napravio da ih sortiram kako ja zelim, inace su sortirani onim redosljedom kojim su definirani u modelu...
    fields = (
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'user_role',
        'status',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        'user_permissions',
    )


# Register your models here.

# admin.site.register(Users)
admin.site.register(Users, UsersAdmin)
