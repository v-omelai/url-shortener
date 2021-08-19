from django.urls import path

from shortener.views import LinkCreateView, LinkRedirectView


app_name = 'shortener'

urlpatterns = [
    path('', LinkCreateView.as_view(), name='link-create'),
    path('<str:id>', LinkRedirectView.as_view(), name='link-redirect'),
]
