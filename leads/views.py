from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse
from .models import Lead,Agent
from .forms import LeadForm 
from .forms import LeadModelForm,CustomUserCreationForm
from django.views import generic
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from customers.models import Customer
from agents.mixins import OrganisorAndLoginRequiredMixin


def lead_table(request):
	leads = Lead.objects.all()
	context={
		'leads': leads
	}
	return render(request, "leads/lead_table.html", context)

class SignupView(generic.CreateView):
	template_name = "registration/signup.html"
	form_class= CustomUserCreationForm

	def get_success_url(self):
		return reverse("login")


class LandingPageView(generic.TemplateView):
	template_name = "landing.html"


def landing_page(request):
	return render(request, "landing.html")

class LeadListView(LoginRequiredMixin,generic.ListView):
	template_name = "leads/lead_list.html"
	context_object_name = "leads"

	def get_queryset(self):
		queryset = Lead.objects.all()
		if self.request.user.is_agent:
			queryset = queryset.filter(agent__user=self.request.user)
		return queryset	



def lead_list(request):
	leads =Lead.objects.all()
	context={
		'leads': leads
	}
	return render(request, "leads/lead_list.html", context)


class LeadDetailView(LoginRequiredMixin,generic.DetailView):
	template_name = "leads/lead_detail.html"
	queryset = Lead.objects.all()
	context_object_name = "lead"


def lead_details(request,pk):
	lead = Lead.objects.get(id=pk)
	context={
        'lead': lead
    }
	return render(request, "leads/lead_detail.html",context)


class LeadCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
	template_name = "leads/lead_create.html"
	form_class= LeadModelForm
	
	def get_success_url(self):
		return reverse("leads:lead-list")

	def form_valid(self, form):
		#todo send email notification
		send_mail(
			subject="A lead has been created",
			message="Go to the site to see the new lead",
			from_email="test@example.com",
			recipient_list=["test2@example.com"]
		)
		return super(LeadCreateView,self).form_valid(form)



def lead_create(request):
	form= LeadModelForm()
	if request.method == "POST":
		form = LeadModelForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("/leads")

	else:
		form = LeadModelForm()		
	
	context ={
		"form":form
		}
	return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
	template_name = "leads/lead_update.html"
	queryset = Lead.objects.all()
	form_class= LeadModelForm
	
	def get_success_url(self):
		return reverse("leads:lead-list")

def lead_update(request,pk):
	lead = get_object_or_404(Lead, pk=pk) 
	
	if request.method == "POST":
		form = LeadModelForm(request.POST,instance=lead)
		if form.is_valid():
			form.save()
			return redirect("/leads")
	else:
		form = LeadModelForm(instance=lead)		
	
	context = {
		'lead': lead,
		'form': form
	}
	return render(request, "leads/lead_update.html", context)

class LeadDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
	template_name = "leads/lead_delete.html"
	queryset = Lead.objects.all()
	
	
	def get_success_url(self):
		return reverse("leads:lead-list")
def lead_delete(request,pk):
	lead=Lead.objects.get(id=pk)
	lead.delete()
	return redirect("/leads")

from django.shortcuts import redirect, get_object_or_404
from .models import Lead
from customers.models import Customer

def convert_to_customer(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        # Create a customer from lead data
        Customer.objects.create(
            name=f"{lead.first_name} {lead.last_name}",
            email="example@example.com",  # Replace or fetch if available
            phone="0000000000"            # Replace or fetch if available
        )
        #lead.delete()  # Optional: remove lead after conversion
        return redirect('leads:lead-list')  # Or wherever your lead page is