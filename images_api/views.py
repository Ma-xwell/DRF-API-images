from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.files.images import get_image_dimensions
import datetime

from .models import User, Image, AccountTier
from .serializers import ImageSerializer, UploadImageSerializer, AccountTierSerializer, ImageDimensionsSerializer
from .functions import create_image_with_new_dimensions

class ImageView(generics.ListCreateAPIView):
    
    def get_serializer_class(self):
        """
        When GET, show user the image links and their attributes. When POST, show only the ability to upload the image.
        """
        if self.request.method == 'POST':    
            return UploadImageSerializer
        
        return ImageSerializer
        
    def get_queryset(self):
        """
        Lists all of the logged user's images
        """
        user = self.request.user
        
        if user.is_authenticated:
            images = Image.objects.filter(user=user)
            
            for image in images:
                if image.is_expirable:
                    if image.expired():
                        image.delete()
            
            return images
        
        return Image.objects.none()
    
    def perform_create(self, serializer):
        """
        Lets logged user upload a new image
        """
        current_time = datetime.datetime.now()
        user = self.request.user
        image = self.request.data['image']
        is_expirable = bool(self.request.data.get('generate_expiring_links', False))
        
        if is_expirable:
            expiration_seconds = serializer.validated_data.get('expiration_seconds', None)

            if expiration_seconds is not None:
                expiration_seconds = int(expiration_seconds)
                print(expiration_seconds)
            if expiration_seconds is None:
                is_expirable = False
        
        account_tier = User.objects.get(id=user.id).tier_type
        account_tier_serializer = AccountTierSerializer(account_tier)
        tier_possible_dimensions = account_tier_serializer['dimensions'].value
        
        new_images_list = []
        
        for dimension in tier_possible_dimensions:
            image.seek(0)
            width = dimension['width'] if not dimension['width'] == 0 else None
            height = dimension['height']
            new_image = create_image_with_new_dimensions(image, height, width)
            new_image_dict = {'image': new_image, 'height': height, 'width': width, 'is_expirable': is_expirable}
            
            if is_expirable:
                new_image_dict['expiration_seconds_between_300_and_30000'] = expiration_seconds, 
                new_image_dict['expiration_date'] = current_time+datetime.timedelta(seconds=expiration_seconds)
            
            new_images_list.append(new_image_dict)
        
        if account_tier_serializer['original_file_link_presence'].value:
            converted_image = create_image_with_new_dimensions(image)
            converted_width, converted_height = get_image_dimensions(converted_image)
            new_image_dict = {'image': converted_image, 'height': converted_height, 'width': converted_width, 'is_expirable': is_expirable}
            
            if is_expirable:
                new_image_dict['expiration_seconds_between_300_and_30000'] = expiration_seconds
                new_image_dict['expiration_date'] = current_time+datetime.timedelta(seconds=expiration_seconds)
            
            new_images_list.append(new_image_dict)
            
        serializer = ImageSerializer(data=new_images_list, many=True)
        #if str(image).lower().endswith(('.jpg', '.png')) and 
        if user.is_authenticated and serializer.is_valid():    
            return serializer.save(user=user)
        
        return serializer
    
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