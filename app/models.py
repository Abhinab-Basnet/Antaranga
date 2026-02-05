from django.db import models
from django.contrib.auth.models import User

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



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cluster_id = models.IntegerField(null=True, blank=True)
    nature_score = models.FloatField(default=0)
    adventure_score = models.FloatField(default=0)
    culture_score = models.FloatField(default=0)
    altitude_score = models.FloatField(default=0)
    top_match_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class UnlockedCluster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_clusters')
    cluster_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cluster_id')

class ClusterHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cluster_history')
    cluster_id = models.IntegerField()
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        
        unique_together = ('user', 'cluster_id') 

    def __str__(self):
        return f"{self.user.username} - Cluster {self.cluster_id}"