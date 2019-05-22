from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from .views import current_user, user_signup


urlpatterns = [
    path('login', obtain_jwt_token, name='login'),
    path('signup', user_signup, name='signup'),
    path('current_user', current_user, name='current_user'),
]
