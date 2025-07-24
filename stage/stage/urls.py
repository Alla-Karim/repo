from django.contrib import admin
from django.urls import path, include
from Maintenance import views
from Maintenance.views import CustomLoginView, admin_dashboard, export_excel

app_name = 'equipements'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    # Routes machines
    path('machines/', views.machine_list, name='machine_list'),
    path('machines/add/', views.machine_create, name='machine_create'),
    path('machines/<int:pk>/edit/', views.machine_update, name='machine_update'),
    path('machines/<int:pk>/delete/', views.machine_delete, name='machine_delete'),

    # Auth : login personnalisé (doit être avant include)
    path('accounts/login/', CustomLoginView.as_view(), name='login'),

    # Autres urls d'authentification (logout, password_change, etc)
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/register/', views.register, name='register'),

    # Dashboard admin custom
    path('admin-panel/', admin_dashboard, name='admin_dashboard'),

    # Export Excel
    path('admin-panel/export/', export_excel, name='export_excel'),

    path('saisisseurs/add/', views.saisisseur_add, name='saisisseur_add'),
    path('admin-panel/saisisseurs/<int:user_id>/delete/', views.saisisseur_delete, name='saisisseur_delete'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
