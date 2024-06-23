from django.db import models


class Responsable(models.Model):
    ROLE_CHOICES = (
        ('responsable_administratif', 'Responsable Administratif'),
        ('responsable', 'Responsable'),
    )
    
    cin = models.CharField(max_length=8, primary_key=True)
    password = models.CharField(max_length=255)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES)


