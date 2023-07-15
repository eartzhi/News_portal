from django.contrib import admin
from .models import Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('header', 'rating', 'creation_time') # оставляем только имя и цену товара
    list_filter = ('category__category', 'creation_time', 'rating') # добавляем примитивные фильтры в нашу админку
    search_fields = ('header', 'category__category') # тут всё очень похоже на фильтры из запросов в базу


class PostCategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post', 'category') # оставляем только имя и цену товара
    list_filter = ('category',) # добавляем примитивные фильтры в нашу админку
    search_fields = ('category',) # тут всё очень похоже на фильтры из запросов в базу


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('post', 'user', 'comment_text', 'creation_time', 'rating') # оставляем только имя и цену товара
    list_filter = ('user', 'post', 'creation_time', 'rating') # добавляем примитивные фильтры в нашу админку
    search_fields = ('user',) # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)

