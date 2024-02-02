from django.db import models

# Create your models here.

#create a class for the book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image_url = models.CharField(max_length=2083)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        unique_together = ('title', 'author')

