from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100000)
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000000)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        unique_together = ('title', 'author')

