from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect 

class OrganisorAndLoginRequiredMixin(AccessMixin):
	"""Verify that the user is logged in and is an organizer."""
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not request.user.is_organisor:
			return redirect("leads:lead-list")
		return super().dispatch(request, *args, **kwargs)