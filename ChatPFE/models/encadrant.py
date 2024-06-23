from django.db import models

class Encadrant(models.Model):
    cin_enca = models.CharField(max_length=8, primary_key=True)
    password_enca = models.CharField(max_length=255)
