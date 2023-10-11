from django.db import models

class File(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to="graph_1/files/")
