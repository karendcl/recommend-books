from django.db import models

# Create your models here.

#create a class for the book model
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.CharField(max_length=2083)
    topics = models.ManyToManyField('Topic')

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'author')


#create a class for the Topics model
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


