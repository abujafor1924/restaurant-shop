from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
     ext=os.path.splitext(value.name)[1] # [0] returns path+filename
     valid_extensions=['.png','.jpg','.jpeg']
     if not ext.lower() in valid_extensions:
          raise ValidationError('unsupported file extension, allowed extensions are '+str(valid_extensions))         