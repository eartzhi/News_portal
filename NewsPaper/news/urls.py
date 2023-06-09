from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import LogoutView
from .views import PostList, PostDetail, SearchPost, NewsCreate, \
    ArticlesCreate, NewsEdit, ArticlesEdit, NewsDelete, ArticlesDelete, \
    upgrade_me, Account, Subscription, subscribe, unsubscribe

urlpatterns = [
   path('', cache_page(1*60)(PostList.as_view()), name='posts_list'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('search', SearchPost.as_view(), name='search_page'),
   path('news/create', NewsCreate.as_view(), name='create_news'),
   path('articles/create', ArticlesCreate.as_view(), name='create_articles'),
   path('news/<int:pk>/edit', NewsEdit.as_view(), name='edit_news'),
   path('articles/<int:pk>/edit', ArticlesEdit.as_view(), name='edit_articles'),
   path('news/<int:pk>/delete', NewsDelete.as_view(), name='delete_news'),
   path('articles/<int:pk>/delete', ArticlesDelete.as_view(),
        name='delete_articles'),
   path('logout/',
        LogoutView.as_view(template_name='logout.html'),
        name='logout'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('user/<int:pk>', Account.as_view(success_url='/'),
        name='account'),
   path('user/subscribe', Subscription.as_view(),
         name='subscription'),
   path('<int:pk>/subscribe', subscribe,
         name='subscribe'),
   path('<int:pk>/unsubscribe', unsubscribe,
         name='unsubscribe'),
   # path('test', IndexView.as_view()),
]
