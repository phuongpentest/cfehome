from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView

from .forms import ItemForm
from .models import Item

class HomeView(View):
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, 'home.html',{})

		user = request.user
		is_following_user_ids = [x.user.id for x in user.is_following.all()]
		qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by('-updated')

		return render(request, 'menus/home-feed.html', {'object_list': qs})

class ItemListView(ListView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

class ItemDetailView(DetailView):
	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
	template_name = 'form.html'
	form_class = ItemForm
	model = Item
	
	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		return super().form_valid(form)	# super(RestaurantCreateView,self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		# kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
		return kwargs

	# def get_queryset(self):
	# 	model = Item
	# 	return super().get_queryset()
	# 	return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Add Item'
		return context

class ItemUpdateView(LoginRequiredMixin, UpdateView):
	template_name = 'menus/detail_update.html'
	form_class = ItemForm
	model = Item
	# def get_queryset(self):
	# 	return super().get_queryset()
		# return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'
		return context

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs