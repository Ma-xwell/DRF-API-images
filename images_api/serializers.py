from rest_framework import serializers
from .models import Image, AccountTier, ImageDimensions
from django.utils import timezone


class ImageDimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDimensions
        fields = ['height', 'width']
        
        
class AccountTierSerializer(serializers.ModelSerializer):
    dimensions = ImageDimensionsSerializer(many=True)
    
    class Meta:
        model = AccountTier
        fields = '__all__'
        
        
class ImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """
        Show width as "auto" if it was not fixed (automatically calculated based on height preserving the image ratio)
        """
        width = instance.width
        expiration_date = instance.expiration_date
        
        if width is None or width == 0:
            width = 'auto'
            
        expiration_date = 'N/A' if expiration_date is None else timezone.localtime(expiration_date).strftime('%B %d, %Y - %H:%M:%S')
        
        data = super().to_representation(instance)
        data['width'] = width
        data['expiration_date'] = expiration_date
        
        return data
    
    class Meta:
        model = Image
        fields = ['image', 'height', 'width', 'is_expirable', 'expiration_date']
        
        
class UploadImageSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        Override __init__ to check if expiring links checkbox and expiration seconds field should be visible
        """
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        
        if user.is_authenticated and user.tier_type is not None: 
            if user.tier_type.generate_expiring_links is True:
                self.fields['generate_expiring_links'] = serializers.BooleanField(source='user.tier_type.generate_expiring_links')
                self.fields['expiration_seconds_between_300_and_30000'] = serializers.IntegerField(source='expiration_seconds', required=False)
    
    def validate(self, data):
        """
        Validators for expiring links checkbox and expiration seconds field
        """
        user = self.context.get('request').user
        if user.is_authenticated and user.tier_type.original_file_link_presence and user.tier_type.generate_expiring_links:
            expiration_seconds = data.get('expiration_seconds')
            is_expiring = data.get('user').get('tier_type').get('generate_expiring_links')
            
            if not is_expiring and expiration_seconds:
                raise serializers.ValidationError('Check the box "Generate expiring links" first.')
            if is_expiring and (expiration_seconds is None or not 300 <= expiration_seconds <= 30000):
                raise serializers.ValidationError('Please provide correct number of seconds in range of 300 to 30000 seconds.')
            
        return data

    class Meta:
        model = Image
        fields = ['image']
    