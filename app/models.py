from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    nature_score = models.IntegerField()
    adventure_score = models.IntegerField()
    culture_score = models.IntegerField()
    altitude_score = models.IntegerField()
    cluster_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.name