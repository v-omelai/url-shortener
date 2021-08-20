from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from rest_framework import generics, status, views
from rest_framework.response import Response

from shortener.models import Link
from shortener.serializers import LinkSerializer


class LinkRedirectView(RedirectView):
    def get_redirect_url(*args, **kwargs):
        links = Link.objects.filter(id=kwargs.get('id'))  # noqa
        link = get_object_or_404(links)
        return link.original


class LinkCreateAPIView(generics.CreateAPIView):
    queryset = Link.objects.all()  # noqa
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        lookup_field = 'original'
        params = {
            lookup_field: request.data.get(lookup_field)
        }
        try:
            link = Link.objects.get(**params)  # noqa
        except ObjectDoesNotExist:
            return super().create(request, *args, **kwargs)
        serializer = self.get_serializer(link)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):  # noqa
        count = Link.objects.count()  # noqa
        return Response({
            'count': count
        }, status=status.HTTP_200_OK)
