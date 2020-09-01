from django.urls import path
from . import views


# for TEMPLATE relative urls
app_name = 'first_app'

urlpatterns = [
    path('', views.index, name='index'),
    # path('form/', views.form_name_view),
    path('form/', views.form_topic_view, name='form_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
