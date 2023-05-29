from django.urls import path
from .views import PostList, PostDetail, SearchPost


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view()),
   path('search', SearchPost.as_view()),
]
