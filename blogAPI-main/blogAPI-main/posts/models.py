from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_comments', blank=True)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_votes', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    
class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    post = models.ForeignKey(Post , on_delete=models.CASCADE, related_name='post_votes')
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.SmallIntegerField(choices=((1,'Upvote'), (-1 , 'Downvote')))
    
    def __str__(self):
        return f'{self.user} {self.get_value_display()}d'
