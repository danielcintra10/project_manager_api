from django.urls import path
from .views import ListCreateUser, RetrieveUpdateDestroyUser, MyTokenObtainPairView, \
    ListDeveloperUsers, ListProjectManagerUsers

urlpatterns = [
    path('users/', ListCreateUser.as_view(), name='list_create_users'),
    path('users/<int:id>', RetrieveUpdateDestroyUser.as_view(), name='retrieve_update_destroy_user'),
    path('users/p/', ListProjectManagerUsers.as_view(), name='list_project_manager_users'),
    path('users/d/', ListDeveloperUsers.as_view(), name='list_developer_users'),
    path('users/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    ]
