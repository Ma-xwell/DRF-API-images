from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AccountTier(models.Model):
    name = models.CharField(max_length=30, unique=True)
    generate_expiring_links = models.BooleanField(default=False)
    original_file_link_presence = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} tier.'
    
class User(AbstractUser):
    tier_type = models.ForeignKey(AccountTier, on_delete=models.CASCADE, null=True)

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
    height = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    is_expirable = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(null=True, blank=True)
    expiration_seconds = models.PositiveIntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)], blank=True, null=True)
    
    def expired(self):
        """
        If image has expired, the method returns True. If it has not expired, then False is returned.
        """
        return self.expiration_date < timezone.now()
    
    def __str__(self):
        return f'Image {self.id} of user "{self.user}"'
    