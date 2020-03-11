from django.contrib.gis.db import models as gis
from django.contrib.gis.geos import Point
from django.db import models
from users.models import CustomUser
import os

# from django.db.models import ImageField, FileField, signals

class CustomImageField():
    def __init__(self, upload_to):
        pass

class BaseModel(models.Model):
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True

def pothole_photo_directory(instance, filename):
    fn, ext = os.path.splitext(filename)
    return 'pothole_{}/original_{}{}'.format(instance.pk, instance.pk, ext)

class Pothole(BaseModel):
    DEPTH = (
        ('1','<30mm'),
        ('2','30mm-60mm'),
        ('3','>60mm')
    )

    WIDTH = (
        ('1', '<50cm'),
        ('2', '50cm-150cm'),
        ('3', '>150cm')
    )

    RESPONSE_TIME_NEEDED = (
        ('1','< A day'),
        ('2','1 day - 5 days'),
        ('3','6 days - 6 months'),
        ('4','>6 months'),
    )

    photo = models.ImageField(upload_to=pothole_photo_directory, null=False, blank=False)
    geometry = gis.PointField()
    depth = models.CharField(choices=DEPTH, blank=False, max_length=1)
    width = models.CharField(choices=WIDTH, blank=False, max_length=1)
    response_time_needed = models.CharField(choices=RESPONSE_TIME_NEEDED, blank=False, max_length=1)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_photo = self.photo
            self.photo = None
            super(Pothole, self).save(*args, **kwargs)
            self.photo = saved_photo

        super(Pothole, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} - {} - {} - {}'.format(self.id, self.depth, self.width, self.response_time_needed)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('-id',)

class PotholeRepair(BaseModel):
    TYPE = (
        ('1','Permanent'),
        ('2','Semi Permanent'),
        ('3','Permanent')
    )

    RESULT = (
        ('1', 'Bad'),
        ('2', 'Enough'),
        ('3', 'Good'),
    )

    pothole = models.ForeignKey(Pothole, on_delete=models.CASCADE, null=True, blank=False)
    # date = models.DateField(null=True, blank=False)
    type = models.CharField(choices=TYPE, null=True, blank=False, max_length=1)
    result = models.CharField(choices=RESULT, null=True, blank=False, max_length=1)
    photo = models.ImageField(upload_to=pothole_photo_directory, null=False, blank=False)

    def __unicode__(self):
        return '{}- {} - {} - {}'.format(self.id, self.date, self.type, self.result)

    class Meta:
        ordering = ('-id',)