from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile
@receiver(post_save, sender=User)
def post_save_create_profile_resever(sender, instance, created, **kwargs):
     if created:
          UserProfile.objects.create(user=instance)     
          print('profile created')
     else:
          try:
               profile = UserProfile.objects.get(user=instance)
               profile.save()
          except:
               UserProfile.objects.create(user=instance)
               print('profile updated')
      
@receiver(post_save, sender=User)         
def post_save_create_profile_resever(sender, instance, **kwargs):
#     print(instance.username,"this user been saved")  
     pass
               
     
# post_save.connect(post_save_create_profile_resever, sender=User)