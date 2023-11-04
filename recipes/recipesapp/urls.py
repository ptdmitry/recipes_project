from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_recipes, name='search_recipes'),
    path('recipe/<int:recipe_id>', views.get_recipe, name='recipe'),
    path('recipe/<slug:recipe_name>', views.get_recipe_by_name, name='recipe_by_name'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/', views.get_recipes, name='get_recipes'),
    path('recipes/<str:user>/', views.get_recipes, name='get_recipes_by_user'),
]
