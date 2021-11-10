from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
import os, uuid

def directory_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return f'{instance.id}{extension}'

class Group(models.Model):
    group = models.CharField("Groupe", max_length=225)
  
    def __str__(self):
        return f"{self.group}"
  
    class Meta:
        verbose_name = 'Catégorie'
    
class Location(models.Model):
    location = models.CharField("Localisation", max_length=225)
    
    def __str__(self):
        return f"{self.location}"
    
    class Meta:
        verbose_name = 'Lieu'
        verbose_name_plural = 'Lieux'
    
class State(models.Model):
    state = models.CharField("État", max_length=225)

    def __str__(self):
        return f"{self.state}"

    class Meta:
        verbose_name = 'État'

class Object(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField("Description", max_length=225)
    nb = models.IntegerField("Nb", default=1)
    group = models.ForeignKey(Group, blank=False, verbose_name="Catégorie", on_delete=models.RESTRICT)
    location = models.ForeignKey(Location, blank=False, verbose_name="Lieu", on_delete=models.RESTRICT)
    state = models.ForeignKey(State, blank=True, null=True, verbose_name="État", on_delete=models.RESTRICT)
    photo = models.ImageField(upload_to=directory_path, blank=True)
    comment = models.TextField("Commentaire", blank=True, max_length=1024)
    supplier = models.CharField("Fournisseur", blank=True, max_length=225)
    price = models.DecimalField("Prix d'achat", blank=True, null=True, max_digits=6, decimal_places=2)
    buy_at = models.DateField("Date d'achat", blank=True, null=True)
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name="Créateur", related_name="user_create", on_delete=models.RESTRICT)
    updated_at = models.DateTimeField("Date de mise à jour", auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name="Modificateur", related_name="user_modify", on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"{self.description}"
    
    @property
    def photo_display(self):
        if self.photo:
            return format_html('<a href="{0}"><img src="{0}" style="max-height:400px;max-width:800px;" /></a>', self.photo.url)
    photo_display.fget.short_description = "Photo"
    
    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return "static/question-mark.png"
    photo_display.fget.short_description = "Photo"


    class Meta:
        verbose_name = 'Objet'
    

