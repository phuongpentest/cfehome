from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from restaurants.models import	RestaurantLocation
from menus.models import Item
from restaurants.forms import RestaurantCreateForm, RestaurantLocationCreateForm


class RestaurantListView(LoginRequiredMixin,ListView):
		def get_queryset(self):
			return RestaurantLocation.objects.filter(owner = self.request.user).order_by('-updated')

class RestaurantDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
			return RestaurantLocation.objects.filter(owner = self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
	template_name = 'form.html'
	form_class = RestaurantLocationCreateForm
	model = RestaurantLocation

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user
		return super().form_valid(form)	# super(RestaurantCreateView,self).form_valid(form)
	
		
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'restaurants/detail_update.html'
	form_class = RestaurantLocationCreateForm
	model = RestaurantLocation
		
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		# menu_items = Item.objects.filter(restaurant=self.kwargs.get('restaurantlocation'))
		context['title'] = 'Update Restaurant'
		# context['menu_items'] = menu_items
		# print(context)
		return context
