from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
from django.core.urlresolvers import reverse
from restaurants.models import RestaurantLocation
from menus.models import Item
from .models import Profile
from .forms import RegistrationForm

User = get_user_model()

def activate_user_view(request, code=None, *args, **kwargs):
	if code:
		qs = Profile.objects.filter(activation_key=code)
		if qs.exists() and qs.count() == 1:
			profile = qs.first()
			if not profile.activated:
				user_ = profile.user
				user_.is_active = True
				user_.save()
				profile.activated = True
				profile.activation_key = None
				profile.save()
				return redirect('/login') #reverse('login')
	#invalid code
	return redirect('/login')   #reverse('login')

class RegistrationView(CreateView):
	form_class = RegistrationForm
	template_name = 'registration/registration.html'
	success_url = '/'

	def dispatch(self, *args, **kwargs):
		# if self.request.user.is_authenticated:
		# 	return redirect('/logout')
		return super().dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		user_to_toggle = request.POST.get('username').strip()
		# print(request.POST)
		# print(user_to_toggle)
		# profile_ = Profile.objects.get(user__username__iexact=user_to_toggle)
		# user = request.user
		# if user in profile_.followers.all():
		# 	profile_.followers.remove(user)
		# else:
		# 	profile_.followers.add(user)			
		profile_, is_following = Profile.objects.toggle_follow(request.user, user_to_toggle)
		# print(is_following)
		return redirect('/profiles/abc/')
		# return redirect(f"/profiles/{profile_.user.username}/")


class ProfileDetailView(DetailView):
	# queryset = User.objects.filter(is_active=True)
	template_name = 'profiles/user.html'
	model = User

	def get_object(self):
		username = self.kwargs.get('username')
		if username is None:
			raise Http404('User name is None')
		return get_object_or_404(User, username__iexact=username, is_active=True)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		# print(context)
		# user = self.get_object()
		user = context['user']
		is_following = False
		if user.profile in self.request.user.is_following.all():
			is_following = True
		context['is_following'] = is_following
		query = self.request.GET.get('q')
		# print(query)
		items_exists = Item.objects.filter(user=user).exists()
		qs = RestaurantLocation.objects.filter(owner=user).search(query)
		# if query:
		# 	qs = qs.search(query)
			# qs = RestaurantLocation.objects.search(query=query)
		if items_exists and qs.exists():
			context['locations'] = qs
		return context

