from django.urls import path
from .views import *


urlpatterns = [
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('register/', registerPage, name='register'),

    path('', HomeListView.as_view(), name='home'),
    path('profile/<str:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('room/<str:pk>/', RoomDetailView.as_view(), name='room'),
    path('create-room/', RoomCreateView.as_view(), name='create-room'),
    path('room/<str:pk>/edit/', RoomUpdateView.as_view(), name='edit-room'),
    path('room/<str:pk>/delete/', RoomDeleteView.as_view(), name='delete-room'),
    path('delete-message/<str:pk>/', MessageDeleteView.as_view(), name='delete-message'),


]


