from django.db import models
import codecs

class NiceBoatSkill(models.Model):
	image = models.ImageField(upload_to='niceboat', blank=True)
	name = models.CharField(max_length=60, unique=True)
	level = models.IntegerField(max_length=2)

class NiceBoatMP(models.Model):
	level = models.IntegerField(max_length=3)
	mp = models.IntegerField(max_length=32)
	price = models.CharField(max_length=32)
	max = models.IntegerField(max_length=32)
	mobs = models.CharField(max_length=64)

class RandomSet(models.Model):
	randomsetid = models.IntegerField(max_length=32, unique=True, db_index=True, primary_key=True)
	itemid = models.IntegerField(max_length=32, unique=True)
	#ml = models.IntegerField(max_length=32)
	#job = models.IntegerField(max_length=32)
	#type = models.IntegerField(max_length=32)
	#slot = models.IntegerField(max_length=32)
	#weaponid = models.IntegerField(max_length=32)
	#armorid = models.IntegerField(max_length=32)
	#socketid = models.IntegerField(max_length=32)
	name = models.CharField(max_length=256)
	#nameid = models.IntegerField(max_length=32)
	desc = models.CharField(max_length=1024)
	grade = models.IntegerField(max_length=1, default=1)
	#server = models.IntegerField(max_length=32, default=511)
	#descid = models.IntegerField(max_length=32)
	icon = models.CharField(max_length=256)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name

class ItemSet(models.Model):
	randomset = models.ForeignKey(RandomSet, related_name="items")
	name = models.CharField(max_length=256)
	desc = models.CharField(max_length=1024)
	grade = models.IntegerField(max_length=1, default=1)
	#server = models.IntegerField(max_length=32, default=511)
	ratio = models.DecimalField(max_digits=10, decimal_places=7)

	class Meta:
		ordering = ['randomset', '-ratio', 'name']

	def __unicode__(self):
		return self.name
