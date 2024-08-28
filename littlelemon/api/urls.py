from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('users', views.Users.as_view(), name='api-users'),
    path('users/me', views.UsersMe.as_view(), name='api-users-me'),
    path('token', obtain_auth_token, name='api-token'),

    path('menu', views.MenuAPI.as_view(), name='api-menu'),
    path('menu/<int:id>', views.MenuItemAPI.as_view(), name='api-singlemenu'),

    path('book', views.BookingAPI.as_view(), name='api-book'),
    path('book/<int:id>', views.SingleBookingAPI.as_view(), name='api-singlebook')
    
]