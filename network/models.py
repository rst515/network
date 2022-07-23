from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from colorful.fields import RGBColorField

class User(AbstractUser):
    userColour = RGBColorField(default='#FF9000')

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    subject = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey("Like", null=True, blank=True, on_delete=models.CASCADE, related_name="likedBy")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "subject": self.subject,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
            # "likes": self.select_related('likes').annotate(num_Likes=Count('likedPost')) 
            # #self.likes.user            
        }    
    
    def __str__(self):
        return f"{self.id} {self.user} {self.subject}"

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likesPosts")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_query_name="likedPost")
    def serialize(self):
        return {
        "id": self.id,
        "user": self.user.username,
        "post": self.post.id
        }  

    def __str__(self):
        return f"{self.id} {self.user} likes '{self.post.subject}' by {self.post.user.username}"

class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    follows = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followedBy")
    
    def __str__(self):
        return f"{self.id} {self.user} follows {self.follows.username}"
