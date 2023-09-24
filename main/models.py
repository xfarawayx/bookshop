from django.db import models
from login.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Book(models.Model):
    bnum = models.CharField(max_length=20, primary_key=True)
    btype = models.CharField(max_length=10)
    bname = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    overplus = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    def __str__(self):
        return self.bnum

class Order(models.Model):
    onum = models.CharField(max_length=20, primary_key=True)
    bnum = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='bnum')
    unum = models.ForeignKey(User, on_delete=models.CASCADE, db_column='unum')
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.onum
