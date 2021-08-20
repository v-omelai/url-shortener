from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from ipware import get_client_ip
from rest_framework import generics, status
from rest_framework.response import Response

from shortener.models import Link, Client
from shortener.serializers import LinkSerializer


class LinkRedirectView(RedirectView):
    def get_redirect_url(*args, **kwargs):
        links = Link.objects.filter(id=kwargs.get('id'))  # noqa
        link = get_object_or_404(links)
        return link.original


class LinkGenericAPIView(generics.GenericAPIView):
    queryset = Link.objects.all()  # noqa
    serializer_class = LinkSerializer
    lookup_field = 'original'

    def post(self, request, *args, **kwargs):
        # Get or Create Link
        try:
            link = Link.objects.get(**{  # noqa
                self.lookup_field: request.data.get(self.lookup_field)
            })
            serializer = self.get_serializer(link)
            status_ = status.HTTP_200_OK
        except ObjectDoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            link = serializer.save()
            status_ = status.HTTP_201_CREATED
        # Get or Create Client + Add Link 2 Client
        address, is_routable = get_client_ip(request)
        if address is not None:
            client, _ = Client.objects.get_or_create(address=address)  # noqa
            client.links.add(link)
        return Response(serializer.data, status=status_)

    def get(self, request, *args, **kwargs):  # noqa
        count = Link.objects.count()  # noqa
        popular = Link.objects.annotate(count=Count('client')).order_by('-count')[:10]  # noqa
        serializer = self.get_serializer(popular, many=True)
        return Response({
            'count': count,
            'popular': serializer.data,
        }, status=status.HTTP_200_OK)
