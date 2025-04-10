from django.db import models
from accounts.models import User

# Create your models here.
class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     fooditem = models.ForeignKey('menu.FoodItem', on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField()     
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)
     
     def __unicode__(self):
          return self.user