from rest_framework import serializers
from .models import Image, AccountTier, ImageDimensions

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'user']
        
class ImageDimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDimensions
        fields = ['height', 'width']
        
class AccountTierSerializer(serializers.ModelSerializer):
    dimensions = ImageDimensionsSerializer(many=True)
    
    class Meta:
        model = AccountTier
        fields = '__all__'