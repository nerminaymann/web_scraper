from rest_framework import serializers

class ScraperSerializer(serializers.Serializer):
    url = serializers.URLField()
