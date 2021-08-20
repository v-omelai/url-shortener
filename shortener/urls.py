from django.urls import path

from shortener.views import LinkCreateAPIView, LinkRedirectView, LinkAPIView

app_name = 'shortener'

urlpatterns = [
    path('', LinkCreateAPIView.as_view(), name='link-create'),
    path('features/', LinkAPIView.as_view(), name='link-features'),
    path('<str:id>/', LinkRedirectView.as_view(), name='link-redirect'),
]
