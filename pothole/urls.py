from django.urls import path

from .views import PotholeCreateView,PotholeDetailView

urlpatterns = [
    path('pothole/create', PotholeCreateView.as_view(), name='pothole_create'),
    path('pothole/details', PotholeDetailView.as_view(), name='pothole_detail'),
]
