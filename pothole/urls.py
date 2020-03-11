from django.urls import path

from .views import PotholeCreateView,PotholeDetailView,PotholeListView

urlpatterns = [
    path('pothole/create', PotholeCreateView.as_view(), name='pothole_create'),
    path('pothole/details', PotholeDetailView.as_view(), name='pothole_detail'),
    path('pothole/list', PotholeListView.as_view(), name='pothole_list'),
]
