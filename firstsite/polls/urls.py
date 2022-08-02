from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offical', views.officaltutor, name='tutor'),
    path('error', views.test_error, name='error'),
]
