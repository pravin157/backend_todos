from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, RegisterView, LoginView, LogoutView, CurrentUserView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
    path('', include(router.urls)),
]
