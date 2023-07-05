from django.test import TestCase, RequestFactory
from django.urls import reverse, reverse_lazy
from django.test import Client
from django.contrib.auth.models import User, AnonymousUser, Group, Permission
from .views import Account, NewsCreate, ArticlesCreate, PostList, PostDetail
from .models import Author, Post, Category
from .forms import PostsForm
from django.utils import timezone


class SimpleTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user1 = User.objects.create_user(username='John',
                                                   email='John@com',
                                                   password='password1')
        self.test_user2 = User.objects.create_user(username='Mike',
                                                   email='Mike@com',
                                                   password='password2')
        premium_group = Group.objects.create(name='authors')
        Author.objects.create(nick_name=self.test_user1.username,
                              user=self.test_user1)
        self.auth = Author.objects.get(nick_name=self.test_user1.username, )
        can_add_post = Permission.objects.get(name='Can add post')
        can_change_post = Permission.objects.get(name='Can change post')
        premium_group.permissions.add(can_add_post)
        premium_group.permissions.add(can_change_post)
        self.test_user1.groups.add(premium_group)
        self.cat = Category.objects.create(category='Политика')
        self.my_post = Post.objects.create(author=self.auth,
                                     header="gbdgbdfhglkgbhsrth",
                                     text= 'wrgehggsfukfyuktndrtnryndryn4eh' )
        self.my_post.category.set([self.cat])

    def test_user_check(self):
        request1 = self.factory.get(reverse('account',
                                            kwargs={'pk': self.test_user1.id}))
        request1.user = self.test_user1
        response1 = Account.as_view()(request1, pk=self.test_user1.id)
        self.assertEqual(response1.status_code, 200)
        request2 = self.factory.post(
            reverse('account', kwargs={'pk': self.test_user1.id}),
            {'username': 'John1',
             'first_name': 'John1',
             'last_name': 'John_last_name'})
        request2.user = self.test_user1
        response2 = Account.as_view(success_url='search')(request2,
                                                          pk=self.test_user1.id)
        self.assertEqual(response2.status_code, 302)
        self.test_user1.refresh_from_db()
        self.assertEqual(self.test_user1.username, 'John1')
        self.assertEqual(self.test_user1.first_name, 'John1')
        self.assertEqual(self.test_user1.last_name, 'John_last_name')

    def test_form(self):
        self.form_data = {
                    'text': 'wrgehggstndrtnsdthdrthdrtftyjfyjftyftyjryndryn4eh',
                    "header": "gbdgbdftyjftyjtfyjytjjftyjftyfyfyfyfyftyjbhsrth",
                    'author': self.auth,
                    'category': self.my_post.category.all(),
                    'post_type': "N",
                     }
        form = PostsForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_news_create(self):
        request = self.factory.post(reverse('create_news'),
                                    data={
                                    'author': 1,
                                    'category': 1,
                                    "header": "gbdgbdftyjftyjtfyjytjjftyjfty",
                                    'text': 'wrgehggstndrtnsdthdrthdrtftyjfy',
                                     })
        request.user = self.test_user1
        response = NewsCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        new_news = Post.objects.last()
        self.assertEquals(Post.objects.count(), 2)
        self.assertEqual(new_news.header, 'gbdgbdftyjftyjtfyjytjjftyjfty')
        self.assertEqual(new_news.text, 'wrgehggstndrtnsdthdrthdrtftyjfy')
        self.assertEqual(new_news.post_type, 'N')

    def test_article_create(self):
        request = self.factory.post(reverse('create_articles'),
                                    data={
                                    'author': 1,
                                    'category': 1,
                                    "header": "gbdgbdftyjftyjtfyjytjjftyjfty",
                                    'text': 'wrgehggstndrtnsdthdrthdrtftyjfy',
                                     })
        request.user = self.test_user1
        response = ArticlesCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        new_news = Post.objects.last()
        self.assertEquals(Post.objects.count(), 2)
        self.assertEqual(new_news.header, 'gbdgbdftyjftyjtfyjytjjftyjfty')
        self.assertEqual(new_news.text, 'wrgehggstndrtnsdthdrthdrtftyjfy')
        self.assertEqual(new_news.post_type, 'A')

    def test_post_list(self):
        request = self.factory.get(reverse('posts_list'))
        request.user = self.test_user2
        response = PostList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context_data['page_obj']), '<Page 1 of 1>')
        self.assertTrue(response.context_data['paginator'])
        self.assertTrue(response.context_data['object_list'])

    def test_post_detail(self):
        request = self.factory.get(reverse('post',
                                           kwargs={'pk': self.my_post.id}))
        request.user = self.test_user2
        response = PostDetail.as_view()(request, pk=self.my_post.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object'].header,
                         'gbdgbdfhglkgbhsrth')
        self.assertEqual(response.context_data['object'].text,
                         'wrgehggsfukfyuktndrtnryndryn4eh')
