from django.db import models

class UserInput(models.Model):
    year = models.CharField(max_length=100)
    km_driven = models.CharField(max_length=100)
    seler_type = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=100)
    transmission_type = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
            
            
            
            
            