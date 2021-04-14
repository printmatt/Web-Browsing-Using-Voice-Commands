from django.db import models

# Create your models here.
class Website(models.Model):
    site_name = models.CharField(max_length=100, help_text='Website entity name', primary_key=True)
    site_address = models.URLField(max_length=100, help_text='Web address')

    def __str__(self):
        return self.site_address