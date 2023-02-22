from django.shortcuts import render , get_object_or_404
from rest_framework import generics , status
from rest_framework.response import Response
from .permissions import IsAuthorOrReadonly 
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAdminUser
from django.urls import reverse
from django.contrib.auth import get_user_model


from .models import Post , Comment ,Vote
from .serializers import PostSerializer , CommentSerializer , VoteSerializer , UserSerializer
# Create your views here.

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadonly ,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    
    
  

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadonly ,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer 
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get comments and votes for the post
        comments = Comment.objects.filter(post=instance)
        comment_serializer = CommentSerializer(comments, many=True , read_only=True )

        votes = Vote.objects.filter(post=instance)
        vote_serializer = VoteSerializer(votes, many=True, read_only=True )

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['comments'] = comment_serializer.data
        data['votes'] = vote_serializer.data
        return Response(data)

    
    
class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadonly ,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
    
class CommentCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly ,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        serializer = PostSerializer(post)
        return Response(serializer.data)


    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = VoteSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                vote = Vote.objects.get(user=self.request.user, post=post)
                vote.value = serializer.validated_data['value']
                vote.save()
            except Vote.DoesNotExist:
                serializer.save(user=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
