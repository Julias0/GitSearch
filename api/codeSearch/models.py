from django.db import models

# Create your models here.
class SearchResults(models.Model):
    searchTerm = models.CharField(max_length=30)
    fileUrl = models.CharField(max_length=500)

    def __str__(self):
        return self.searchTerm