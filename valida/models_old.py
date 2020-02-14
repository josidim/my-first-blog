# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models
from django.utils import timezone


class t_face_cnefe(models.Model):
	COD_SETOR    = models.IntegerField(primary_key=True)                             
	NUM_QUADRA   = models.IntegerField()
	NUM_FACE     = models.IntegerField()                           
	class Meta:
         db_table = '"CNEFEUNIV"."T_FACE_CNEFE"'