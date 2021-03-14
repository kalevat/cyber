from django.urls import path

from .views import homePageView, addView, normalView, changeView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('view/', normalView, name='validation'),
    path('change/', changeView, name='change')
]
