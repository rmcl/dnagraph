from django.db import models

class Node(models.Model):
    id = models.AutoField(primary_key=True)
    length = models.IntegerField()
    parents = models.ManyToManyField('Node')
    locations = models.CharField(max_length=100)
    sequence = models.TextField()


    def __unicode__(self):
        return str(self.id)