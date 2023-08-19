from .models import *
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['pk', 'header', 'text', 'post_type']