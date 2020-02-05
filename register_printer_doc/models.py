from django.db import models

class RegisterPrinterDoc(models.Model):
    rp_doc_id = models.AutoField(
        primary_key=True)
    name = models.CharField(
        max_length=255)
    doc = models.TextField()
    
