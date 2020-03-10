from django.urls import path

from .views import PotholeCreateView

urlpatterns = [
    path('pothole/create', PotholeCreateView.as_view(), name='pothole_create'),
]
