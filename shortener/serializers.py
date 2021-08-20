from rest_framework import serializers

from shortener.models import Link


class LinkSerializer(serializers.ModelSerializer):
    shortened = serializers.ReadOnlyField()

    class Meta:
        model = Link
        fields = '__all__'
