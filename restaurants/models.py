from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator
from .validators import validate_category
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class RestaurantLocationQuerySet(models.QuerySet):
	def search(self, query):	#RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
		if query:
			query = query.strip()
			return self.filter(
				Q(name__icontains=query) |
				Q(location__icontains=query) |
				Q(category__icontains=query) |
				Q(item__name__icontains=query) |
				Q(item__contents__icontains=query)
				).distinct()
		else:
			return self

class RestaurantLocationManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationQuerySet(self.model, using=self._db)
	def search(self, query):	#restaurantLocation.objects.search()
		return self.get_queryset().search(query)

class RestaurantLocation(models.Model):
	owner		= models.ForeignKey(User) # Django Models Unleached JOINCFE.com
	name		= models.CharField(max_length=120)
	location	= models.CharField(max_length=120, null=True, blank=True)
	category	= models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
	timestamp	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)
	#my_date_field = models.DateTimeField(auto_now=False, auto_now_add=False)
	slug		= models.SlugField(null=True, blank=True)

	objects = RestaurantLocationManager()		# add Model.objects.all()

	class Meta:
		ordering = ['-updated', '-timestamp']
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):		#get_absolute_url
		# return f"/restaurant/{self.slug}"
		# return reverse('restaurant')
		return reverse('restaurants:detail', kwargs={'slug': self.slug})


	@property
	def title(self):
		return self.name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
	# print('saving...')
	# print(instance.timestamp)
	instance.category = instance.category.capitalize()

	if not instance.slug:
		instance.slug = unique_slug_generator(instance)


# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
# 	print('saved...')
# 	print(instance.timestamp)
# 	if not instance.slug:
# 		instance.slug = unique_slug_generator(instance)
# 		instance.save()


pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)

TITLE_CHOICES = (
		('MR', 'Mr.'),
		('MRS', 'Mrs.'),
		('MS', 'Ms.'),
		# ('MM', 'Mm.'),
	)

class Author(models.Model):
	name = models.CharField(max_length=100)
	title = models.CharField(max_length=3, choices=TITLE_CHOICES)
	birth_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.name

class Book(models.Model):
	authors = models.ManyToManyField(Author)
	name = models.CharField(max_length=100)
