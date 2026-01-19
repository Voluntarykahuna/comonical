from django.db import models
from django.conf import settings # Best way to reference the User model

class Item(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/')
    founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   


class Item(models.Model):
    CATEGORY_CHOICES = [
    ('electronics', 'Electronics'), # 'electronics' is the VALUE, 'Electronics' is the LABEL
    ('documents', 'Documents/IDs'),
    ('personal', 'Personal Items'),
    ('other', 'Other'),
]
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='item_photos/')
    location_found = models.CharField(max_length=255)
    date_found = models.DateField()
    
    # Links to the CustomUser in accounts app
    founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_recovered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title