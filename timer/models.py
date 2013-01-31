from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    user = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=128)
    color = models.CharField(max_length=6, default="red")

    def get_absolute_url(self):
        return "/timer/label/%d/events/" % self.pk

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Event(models.Model):
    user = models.ForeignKey(User, editable=False)
    started_at = models.DateTimeField(default=datetime.now())
    duration = models.IntegerField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)   # in seconds
    labels = models.ManyToManyField(Label, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def hours(self):
        return self.duration/3600

    def title(self):
        if self.notes:
            return '%s: %s'  % (self.notes, self.duration())

        return self.started_at

    def as_json(self):
        return {'started_at': int(self.started_at.strftime('%s'))*1000}

    def get_absolute_url(self):
        return "/timer/events/%d/" % self.pk

    class Meta:
        ordering = ['-started_at']
