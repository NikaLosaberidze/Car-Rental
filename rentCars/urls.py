from django.urls import path
from django.contrib.auth.views import LogoutView

from rentCars import views  

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': 'home'}, name='logout'),
    path('user/', views.user_profile, name='user_profile'),
    path('add_car/', views.add_car, name='add_car'),
    path('like/<int:car_id>/', views.like_car, name='like_car'),
    path('view_car/<int:car_id>/', views.view_car, name='view_car'),
    path('update_car/<int:car_id>/', views.update_car, name='update_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('rent_car/<int:car_id>/', views.rent_car, name='rent_car'),
]

