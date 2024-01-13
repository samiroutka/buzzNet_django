from django.urls import path
from .views import *

urlpatterns = [
  path('login/', LoginView.as_view()),
  path('register/', RegisterView.as_view()),

  path('users/<name>', SearchUserApi.as_view()),
  path('users/', UsersApi.as_view()),

  path('user/<name>', UserApi.as_view()),
  path('user/<name>/posts', UserPosts.as_view()),
  path('user/<name>/posts/<id>', UserPost.as_view()),
  
  path('posts/<title>', PostView.as_view()),

  path('mediadowloading/images/', MediaImagesView.as_view()),
  path('mediadowloading/videos/', MediaVideosView.as_view()),
]