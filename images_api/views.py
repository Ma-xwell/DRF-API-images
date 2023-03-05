from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Image, AccountTier
from .serializers import ImageSerializer, AccountTierSerializer, ImageDimensionsSerializer

# Create your views here.

class ImageApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        List all images of the user
        """
        
        images = Image.objects.filter(user=request.user.id)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Upload the image
        """
        data = {
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AccountTierApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Lists all the account tiers
        """
        tiers = AccountTier.objects.all()
        serializer = AccountTierSerializer(tiers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Allows to add new tiers
        """
        data_account_tier = {
            'name': request.data.get('name'),
            'generate_expiring_links': request.data.get('generate_expiring_links'),
            'original_file_link_presence': request.data.get('original_file_link_presence'),
            'description': request.data.get('description')
        }
        serializer_account_tier=AccountTierSerializer(data=data_account_tier)
        
        if serializer_account_tier.is_valid():
            account_tier = serializer_account_tier.save()
            
            data_image_dimensions = {
                'height': request.data.get('height'),
                'width': request.data.get('width'),
                'tier_type': account_tier.id
            }
            serializer_image_dimensions = ImageDimensionsSerializer(data=data_image_dimensions)
            if serializer_image_dimensions.is_valid():
                serializer_image_dimensions.save()
                return Response(serializer_image_dimensions.data, status=status.HTTP_201_CREATED)
            return Response(serializer_image_dimensions.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_account_tier.errors, status=status.HTTP_400_BAD_REQUEST)