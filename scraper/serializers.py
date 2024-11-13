from rest_framework import serializers

class ScraperSerializer(serializers.Serializer):
    url = serializers.URLField()
    title_xpath = serializers.CharField(required=False, allow_blank=True)
    description_xpath = serializers.CharField(required=False, allow_blank=True)
    image_xpath = serializers.CharField(required=False, allow_blank=True)
