from django.urls import path
from .views import ListCreateUser, RetrieveUpdateDestroyUser, MyTokenObtainPairView

urlpatterns = [
    path('users/', ListCreateUser.as_view(), name='list_create_users'),
    path('users/<int:id>', RetrieveUpdateDestroyUser.as_view(), name='retrieve_update_destroy_user'),
    path('users/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    ]
