from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import os

def create_image_with_new_dimensions(image: InMemoryUploadedFile, new_height=None, new_width=None):
    """
    Resizes image or keeps it original but saves again so it will be dict type (the same as resized images)
    """
    img = Image.open(image)
    old_width, old_height = img.size
    
    def save_into_file(imgfile):
        imgfile.save("temp.jpg", "JPEG", optimize=True)
        buffer = BytesIO()
        imgfile.save(buffer, format='JPEG', optimize=True)
        file = ContentFile(buffer.getvalue())
        os.remove("temp.jpg")
        return file

    if new_height:
        if new_width == 0 or new_width is None:
            new_width = int(old_width / (old_height / new_height))
            
        alias = Image.ANTIALIAS if new_height < old_height else Image.BICUBIC
        new_img = img.resize((new_width, new_height), alias)
        
        file = save_into_file(new_img)
        file_name = image.name.split('.')[0] + f'_resized_h{new_height}_w{new_width}.jpg'
        
    if new_height == None and new_width == None or new_height == 0 or new_height == old_height:
        file = save_into_file(img)
        file_name = image.name.split('.')[0] + '_original.jpg'
        
    return InMemoryUploadedFile(file, None, file_name, 'image/jpeg', file.tell, None)
