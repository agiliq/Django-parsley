from django.db import models

# Create your models here.

class Profile(models.Model):
	name=models.CharField(max_length=15)
	dob = models.DateField(blank=True,null=True)
	summary=  models.TextField()
	phone=models.IntegerField(max_length=15, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=10)
	S_CHOICES = (
        ('Male', 'Male'),        
        ('Female', 'Female'),
    )
	sex=models.CharField(max_length=10,choices=S_CHOICES)