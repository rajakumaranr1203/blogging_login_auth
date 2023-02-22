from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Vote


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('user', 'content', 'created_at')


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Vote
        fields = ('user', 'value', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    votes = VoteSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'body', 'created_at', 'updated_at', 'comments', 'votes' )
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id' , 'username' , 'email')

