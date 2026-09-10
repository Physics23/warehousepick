from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, LogoutView, StationViewSet, ItemViewSet,
    ToteViewSet, PickSessionViewSet, PickTaskViewSet,
    CurrentTaskView, StationStatsView, CreateItemWithImageView
)

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'items', ItemViewSet)
router.register(r'totes', ToteViewSet)
router.register(r'sessions', PickSessionViewSet)
router.register(r'tasks', PickTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('items/upload/', CreateItemWithImageView.as_view(), name='create-item-with-image'),
    path('stations/<str:station_id>/current-task/', CurrentTaskView.as_view(), name='current-task'),
    path('stations/<str:station_id>/stats/', StationStatsView.as_view(), name='station-stats'),
]