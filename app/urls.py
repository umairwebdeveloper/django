from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('works/', views.works, name='works'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('auth/', views.login, name='auth'),
    path('trust/', views.trust, name='trust'),
    path('auth_id/<str:transaction_id>/', views.register, name='transaction_auth'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.add_or_update_profile, name='add_or_update_profile'),
    path('update_phone_number/', views.update_phone_number, name='update_phone_number'),
    path("verify/<str:transaction_id>/", views.verify_transaction, name="verify_transaction"),
    path("details/<str:transaction_id>/", views.vehicle_details, name="vehicle_details"),
    path('transaction/cancel/<str:transaction_id>/', views.cancel_transaction, name='cancel_transaction'),
]
