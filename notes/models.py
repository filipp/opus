import re
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        ordering = ['title']

class Note(models.Model):
    user = models.ForeignKey(User)
    shared = models.BooleanField(default=True)
    title = models.CharField(max_length=140, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def get_date(self):
        return self.version_set.all()[0].created_at

    def get_user(self):
        pass

    def content(self):
        try:
            return self.version_set.latest().content
        except Version.DoesNotExist:
            return ''

    def updated_at(self):
        return self.version_set.latest().created_at

    def get_absolute_url(self):
        return '/notes/%d/' % self.pk

    class Meta:
        ordering = ['-id']

class Version(models.Model):
    note = models.ForeignKey(Note)
    user = models.ForeignKey(User)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())

    class Meta:
        get_latest_by = 'created_at'

class Attachment(models.Model):
    content = models.FileField(upload_to='uploads')
    note = models.ForeignKey(Note)

@receiver(post_save, sender=Version)
def version_saved(sender, instance, created, **kwargs):
    
    tags = re.findall('#(\w+)', instance.content)

    for t in tags:
        tag = Tag.objects.get_or_create(title=t)[0]
        instance.note.tags.add(tag)

    instance.note.save()
