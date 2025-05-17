from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from maison import views as maison_views
from reservation import views as reservation_views
from paiement import views as paiement_views

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    path('admin/users/', user_views.manage_users, name='manage_users'),
    path('admin/users/<int:user_id>/delete/', user_views.delete_user, name='delete_user'),
    path('admin/reservations/', user_views.all_reservations, name='all_reservations'),
    
    # Authentication URLs
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout_view'),
    path('profile/', user_views.profile_view, name='profile_view'),
    
    # House URLs
    path('', maison_views.home, name='home'),  # Changed this line
    path('houses/', maison_views.house_list, name='house_list'),
    path('houses/<int:house_id>/', maison_views.house_detail, name='house_detail'),
    path('houses/add/', maison_views.add_house, name='add_house'),
    path('houses/<int:house_id>/edit/', maison_views.edit_house, name='edit_house'),
    path('houses/<int:house_id>/delete/', maison_views.delete_house, name='delete_house'),
    path('my-houses/', maison_views.my_houses, name='my_houses'),
    
    # Reservation URLs
    path('reservations/create/<int:house_id>/', reservation_views.create_reservation, name='create_reservation'),
    path('my-reservations/', reservation_views.my_reservations, name='my_reservations'),
    path('reservations/<int:reservation_id>/cancel/', reservation_views.cancel_reservation, name='cancel_reservation'),
    path('received-reservations/', maison_views.received_reservations, name='received_reservations'),
    
    # Payment URLs
    path('payments/process/<int:reservation_id>/', paiement_views.process_payment, name='process_payment'),
    path('payments/history/', paiement_views.payment_history, name='payment_history'),
    path('payments/confirmation/<int:payment_id>/', paiement_views.payment_confirmation, name='payment_confirmation'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
