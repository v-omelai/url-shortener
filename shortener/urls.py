from django.urls import path

from shortener.views import LinkRedirectView, LinkGenericAPIView

app_name = 'shortener'

urlpatterns = [
    path('', LinkGenericAPIView.as_view(), name='link-create-plus-features'),
    path('<str:id>/', LinkRedirectView.as_view(), name='link-redirect'),
]
