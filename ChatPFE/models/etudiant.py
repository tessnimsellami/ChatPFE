from django.db import models

class Etudiant(models.Model):
    cin_etud = models.CharField(max_length=8, primary_key=True)
    password_etud = models.CharField(max_length=255)
