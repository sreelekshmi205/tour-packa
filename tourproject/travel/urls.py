from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('book/<int:pk>/', views.book_package, name='book_package'),

    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/add/', views.add_package, name='add_package'),
    path('vendor/edit/<int:pk>/', views.edit_package, name='edit_package'),
    path('vendor/delete/<int:pk>/', views.delete_package, name='delete_package'),

    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/approve/<int:pk>/', views.approve_package, name='approve_package'),
]
