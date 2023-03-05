from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.

class AccountTier(models.Model):
    name = models.CharField(max_length=30, unique=True)
    generate_expiring_links = models.BooleanField(default=False)
    original_file_link_presence = models.BooleanField(default=False)
    description = models.TextField()
    
    def __str__(self):
        return f'{self.name} tier.'
    
class User(AbstractUser):
    tier_type = models.ForeignKey(AccountTier, on_delete=models.CASCADE, null=True)
    
    def change_tier(self, new_type_name):
        """
        Changes tier type of the user if the given type exists.
        """
        try:
            new_type = AccountTier.objects.get(name=new_type_name)
        except AccountTier.DoesNotExist:
            raise ValueError('Such tier does not exist.')
        
        self.tier_type = new_type
        self.save()
        
    def __str__(self):
        return f'User: {self.id}. Tier: {self.tier_type}.'

class ImageDimensions(models.Model):
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField(null=True)
    tier_type = models.ForeignKey(AccountTier, on_delete=models.CASCADE, related_name='dimensions')
    
    def __str__(self):
        width_str = "auto" if self.width is None else str(self.width)
        return f'Height: {self.height}; width: {width_str}; tier: {self.tier_type}.'

class Image(models.Model):
    image = models.ImageField(upload_to='images_api/media/images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_images')
    expiration = models.DateTimeField(null=True, blank=True)
    dimensions = models.ForeignKey(ImageDimensions, on_delete=models.PROTECT, related_name='images', null=True)
    
    def expired(self):
        """
        If image has expired, the method returns True. If it has not expired, then False is returned.
        """
        return self.expiration < datetime.datetime.now()
    
    def __str__(self):
        return f'Image {self.id} of user "{self.user}"'
    