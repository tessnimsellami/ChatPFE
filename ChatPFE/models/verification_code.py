from django.db import models

class Verification_Code(models.Model):
    cin_verification = models.CharField(max_length=8, primary_key=True)
    code = models.CharField(max_length=6)
