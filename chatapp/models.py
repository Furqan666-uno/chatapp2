from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class ChatRoom(models.Model):
    name= models.CharField(max_length=200)
    slug= models.SlugField(unique=True) # creates unique vlues for each room
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name 
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room= models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content= models.TextField()
    date= models.DateTimeField(auto_now=True)

    class Meta:
        ordering= ('date',) # to arrange msg in date order

    def __str__(self):
        return f"{self.user.username} in {self.room.name}: {self.message_content[:30]}"