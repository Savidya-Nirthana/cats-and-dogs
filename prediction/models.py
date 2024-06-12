from django.db import models

class ImageUpload(models.Model):
    image=models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title