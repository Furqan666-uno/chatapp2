from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from chatapp import views as chat_views
from chatapp.views import index

urlpatterns = [
    path('', index, name='home'),  # Make chat rooms page the homepage
    path('admin/', admin.site.urls),
    path('rooms/', include('chatapp.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='chatapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', chat_views.signup_view, name='signup'),
]
