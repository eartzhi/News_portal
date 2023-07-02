from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User, AnonymousUser, Group, Permission
from .views import Account, NewsCreate
from .models import Author, Post, Category
from django.utils import timezone


class SimpleTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='John', email='John@com',
                                              password='password1')
        self.user2 = User.objects.create_user(username='Mike', email='Mike@com',
                                              password='password2')
        premium_group = Group.objects.create(name='authors')
        # premium_group.user_set.add(self.user1)
        Author.objects.create(nick_name=self.user1.username, user=self.user1)
        self.auth = Author.objects.get(nick_name=self.user1.username, )
        can_add_post = Permission.objects.get(name='Can add post')
        can_change_post = Permission.objects.get(name='Can change post')
        premium_group.permissions.add(can_add_post)
        premium_group.permissions.add(can_change_post)
        self.user1.groups.add(premium_group)
        Category.objects.create(category='Политика')
        # cat = Category.objects.get(category='Политика')
        # my_post = Post.objects.create(author=self.auth,
        #                              header="gbdgbdfbhsrth",
        #                              text= 'wrgehggstndrtnryndryn4eh' )
        # # my_post.category.set([cat])

    # def test_user_check(self):
    #     request1 = self.factory.get(reverse('account',
    #                                          kwargs={'pk': self.user1.id}))
    #     request1.user = self.user1
    #     response1 = Account.as_view()(request1, pk=self.user1.id)
    #     print(response1)
    #     self.assertEqual(response1.status_code, 200)
    #     request2 = self.factory.post(
    #         reverse('account', kwargs={'pk': self.user1.id}),
    #         {'username': 'John1',
    #          'first_name': 'John1',
    #          'last_name': 'John_last_name'})
    #     request2.user = self.user1
    #     response2 = Account.as_view(success_url='search')(request2, pk=self.user1.id)
    #     print(response2)
    #     self.assertEqual(response2.status_code, 302)
    #     self.user1.refresh_from_db()
    #     self.assertEqual(self.user1.username, 'John1')
    #     self.assertEqual(self.user1.first_name, 'John1')
    #     self.assertEqual(self.user1.last_name, 'John_last_name')

    def test_post_create(self):
        # auth = Author.objects.get(nick_name=self.user1.username)
        cat = Category.objects.get(category='Политика')
        request = self.factory.post('posts/news/create',
                                    {
                                        'text': 'wrgehggstndrtnsdthdrthdrthdrthdtrdhdrthrthdrthdrthdrthrthrthdrthdtrhdrthdrthftyjftyjftftyjfyjftyftyjryndryn4eh',
                                        "header": "gbdgbdftyjftyjtfyjytjtyjftyjftyfyfyfyfyftyjbhsrth",
                                        'category': 'Политика',
                                        'author': self.auth,
                                        'post_type': "N",
                                     # "header": "gbdgbdftyjftyjtfyjytjtyjftyjftyfyfyfyfyftyjbhsrth",
                                     # 'text': 'wrgehggstndrtnsdthdrthdrthdrthdtrdhdrthrthdrthdrthdrthrthrthdrthdtrhdrthdrthftyjftyjftftyjfyjftyftyjryndryn4eh',
                                     # # 'creation_time': timezone.now(),
                                     })
        # self.Post.refresh_from_db()
        request.user = self.user1
        print(request.headers)
        response = NewsCreate.as_view()(request)
        # response.render()
        print(response)
        self.assertEqual(response.status_code, 200)
        new_news = Post.objects.all()
        print(new_news)
        # self.assertEquals(new_news.count(), 1)
        # self.assertEqual(new_news.values('category__category'), cat)
        # self.assertEqual(new_news.header, 'gbdgbdfbhsrth')
        # self.assertEqual(new_news.text, 'wrgehggstndrtnryndryn4eh')

