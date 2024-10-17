from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
