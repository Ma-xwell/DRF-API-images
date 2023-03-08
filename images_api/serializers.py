from rest_framework import serializers
from .models import Image, AccountTier, ImageDimensions

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
        width = instance.width
        expiration_date = instance.expiration_date
        if width is None or width == 0:
            width = 'auto'
        expiration_date = 'N/A' if expiration_date is None else expiration_date.strftime('%B %d, %Y - %H:%M:%S')
        data = super().to_representation(instance)
        data['width'] = width
        data['expiration_date'] = expiration_date
        return data
    
    class Meta:
        model = Image
        fields = ['image', 'height', 'width', 'is_expirable', 'expiration_date']
        
class UploadImageSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super().__init__(*args, **kwargs)
        if user.is_authenticated: 
            if user.tier_type.generate_expiring_links is True:
                self.fields['generate_expiring_links'] = serializers.BooleanField(source='tier_type.generate_expiring_links')
                self.fields['expiration_seconds_between_300_and_30000'] = serializers.IntegerField(source='expiration_seconds', required=False)
    
    class Meta:
        model = Image
        fields = ['image']
    