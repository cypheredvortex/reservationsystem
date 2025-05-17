from django.contrib import admin
from django.apps import AppConfig

def customize_admin():
    # These customizations will be applied after the admin site is properly initialized
    admin.site.site_header = 'Home Reservation Administration'
    admin.site.site_title = 'Home Reservation Admin'
    admin.site.index_title = 'Site Administration'
    admin.site.enable_nav_sidebar = True

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django.contrib.admin'
    verbose_name = 'Administration'
    default_site = 'django.contrib.admin.sites.AdminSite'

    def ready(self):
        customize_admin()