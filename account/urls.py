from django.urls import path, include

from .views import register_view, login_view, auth_users_view, login_api, register_api, logout_api

app_name = 'account'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('', auth_users_view, ),
    path('login', login_api, name='login_api'),
    path('register', register_api, name='register_api'),
    path('logged_out/', logout_api, name='logout_api'),

]
