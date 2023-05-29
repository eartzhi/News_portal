from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_DEFAULT,
                                default='Неизвестен')
    nick_name = models.CharField(max_length=255, null=True, default='Автор')
    rating = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)

    def __str__(self):
        return self.nick_name

    def update_rating(self):
        post_rating = 0
        comment_rating = 0
        author_comment_rating = 0
        for rate in Post.objects.filter(author=self.pk):                 # не запросом, зато читаемо
            post_rating += rate.rating
            for comm_rate in Comment.objects.filter(post=rate):
                comment_rating += comm_rate.rating
        for auth_rate in Comment.objects.filter(user=self.user):
            author_comment_rating += auth_rate.rating
        self.rating = post_rating * 3 + comment_rating + author_comment_rating
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    ARTICLE = 'A'
    NEWS = 'N'

    POST_TYPE_CHOISE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT,
                               default='Неизвестен')
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOISE)
    creation_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.TextField()
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.header[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# заполение в файле News_portal\NewsPaper\module_D5.py
