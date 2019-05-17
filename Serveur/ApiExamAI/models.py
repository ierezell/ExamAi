from django.db import models
from django.utils import timezone


class Eleve(models.Model):
    idul = models.CharField(max_length=7)
    # clee_prive_serveur = models.IntegerField(default=0)
    # clee_publique_client = models.IntegerField(default=0)
    dateCo = models.DateTimeField(auto_now_add=True,
                                  verbose_name="Date de connection")
    suspect = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=f"images/eleves/{idul}",
                              default=None,
                              blank=True,
                              null=True)

    videoSurveillance = models.ImageField(
        upload_to=f"images/surveillance/{idul}",
        default=None,
        blank=True,
        null=True)

    soundSurveillance = models.FileField(
        upload_to=f"sound/surveillance/{idul}",
        default=None,
        blank=True,
        null=True)

    class Meta:
        verbose_name = "eleve"
        ordering = ['idul']

    def __str__(self):
        return self.idul
