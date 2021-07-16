from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=90)
    description = models.TextField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
