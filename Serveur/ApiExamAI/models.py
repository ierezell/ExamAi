from django.db import models
from django.utils import timezone


class Surveillance(models.Model):
    suspect = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="photos/", default=None)

    class Meta:
        verbose_name = "surveillance"
        ordering = ['suspect']

    def __str__(self):
        return self.suspect


class Eleve(models.Model):
    idul = models.CharField(max_length=7)
    clee = models.IntegerField()
    dateCo = models.DateTimeField(auto_now_add=True,
                                  verbose_name="Date de connection")
    # default=timezone.now,
    #surveille = models.OneToOneField(Surveillance, on_delete=models.PROTECT, null=True)
    # PROTECT ou CASCADE ou SET_NULL

    class Meta:
        verbose_name = "eleve"
        ordering = ['idul']

    def __str__(self):
        return self.idul


"""
>> > article = Article(titre="Bonjour", auteur="Maxime")
>> > for article in Article.objects.filter(auteur="Maxime"):
>> > Article.objects.filter(titre__contains="crêpe")
>> > Article.objects.filter(date__lt=timezone.now())
"""
