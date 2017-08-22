from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from restaurants.models import	RestaurantLocation, Author, Book
from restaurants.forms import RestaurantCreateForm, RestaurantLocationCreateForm, AuthorForm

def restaurant_listview(request):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, template_name, context)	

# def restaurant_createview(request):
# 	template_name = 'restaurants/restaurants_create.html'
# 	if request.method == "POST":
# 		# print(request.POST)
# 		name = request.POST.get('name')
# 		location = request.POST.get('location')
# 		category = request.POST.get('category')
# 		obj = RestaurantLocation.objects.create(name=name, location=location, category=category)
# 		return redirect('/restaurant')
# 	elif request.method == "GET":
# 		print("Get data")
# 	context = {}	
# 	return render(request, template_name, context)	
@login_required(login_url='/login/')
def restaurant_createview(request):
	template_name = 'restaurants/restaurants_create.html'
	form = RestaurantLocationCreateForm(request.POST or None)
	errors = None
	
	if form.is_valid():
		# Customize
		# like a pre save
		user = request.user
		if user.is_authenticated():
			instance = form.save(commit=False)
			instance.owner = user
			instance.save()
			# like a post save
			return redirect('/restaurant')
		else:
			return redirect('/login')
	if form.errors:
		errors = form.errors

	context = {'form': form, 'errors': errors}	
	return render(request, template_name, context)	

class RestaurantListView(ListView):

	def get_queryset(self):
		#print(self.kwargs)
		slug = self.kwargs.get('slug')
		if slug:
			queryset = RestaurantLocation.objects.filter(
				Q(category__iexact=slug) |
				Q(category__icontains=slug)
			)
		else: 
			queryset = RestaurantLocation.objects.all().order_by('-timestamp')
		return queryset

class RestaurantDetailView(DetailView):
	queryset = RestaurantLocation.objects.all()
	#template_name = 'restaurants/restaurantlocation_detail.html'

	# def get_context_data(self, *args, **kwargs):
	# 	print(self.kwargs)
	# 	context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
	# 	print(context)
	# 	return context
	
	# def get_object(self, *args, **kwargs):
	# 	rest_id = self.kwargs.get('rest_id')
	# 	obj = get_object_or_404(RestaurantLocation, id=rest_id)
	# 	return obj


class AuthorListView(ListView):
	queryset = Author.objects.all()

def author_createview(request):
	template_name = 'restaurants/author_create.html'
	form = AuthorForm(request.POST or None)
	errors = None
	
	if form.is_valid():
		form.save()
		return redirect('/author')
	if form.errors:
		errors = form.errors

	context = {'form': form, 'errors': errors}	
	return render(request, template_name, context)	

class RestaurantCreateView(LoginRequiredMixin, CreateView):
	template_name = 'form.html'
	form_class = RestaurantLocationCreateForm
	# success_url = '/restaurant'
	# login_url = '/login/'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user
		return super().form_valid(form)	# super(RestaurantCreateView,self).form_valid(form)
	
		
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context