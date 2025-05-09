"""
URL configuration for djcrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from leads.views import landing_page,LandingPageView,SignupView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/",include("django_browser_reload.urls")),
    path('', LandingPageView.as_view() ,name="landing-page"),
    path('leads/',include('leads.urls',namespace="leads")),
    path('agents/',include('agents.urls',namespace="agents")),
    path('signup/',SignupView.as_view(),name="signup"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(
        next_page=reverse_lazy('landing-page'),
        template_name='registration/logout.html'
        ),name="logout"),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)