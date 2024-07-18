from django.db import models


class Category(models.Model):
 category_name = models.CharField(max_length=200, null=True, unique=True)
 def __str__(self):
     return self.category_name
 

class Product(models.Model):
    product_name= models.CharField(max_length=200, unique=True)
    product_price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.FileField(upload_to= 'static/uploads', null=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    #ondelete le chai category delete garda product ma dekhine category pani hatnu parxa so 
    #null=true hareko choti class banaisake paxi paxi kei attributes thapnu paro vane tesma rakhnu parx always
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name
    # return str(self.product_price) yo chai product ko price ko adhar ma admin ma list out garna ko lagi


