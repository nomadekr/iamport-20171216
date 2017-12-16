from django.conf.urls import url
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^login/$', login, name='login', kwargs={
        'template_name': 'accounts/login.html'
    }),
]

