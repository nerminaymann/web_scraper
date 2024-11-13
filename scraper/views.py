import requests
import pandas as pd
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ScraperSerializer
from .services.scraper_service import ContentParser


class ScraperView(APIView):

    def post(self, request):
        serializer = ScraperSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            title_xpath = serializer.validated_data['title_xpath']
            description_xpath = serializer.validated_data['description_xpath']
            image_xpath = serializer.validated_data['image_xpath']

            scraper = ContentParser(url)

            try:
                # Scrape all items and get them as structured data
                data = scraper.scrape_items(title_xpath, description_xpath, image_xpath)

                # Save to CSV and Excel
                csv_file = scraper.save_to_csv(data)
                excel_file = scraper.save_to_excel(data)

                # Return paths to the saved files
                return Response({
                    'csv_file': csv_file,
                    'excel_file': excel_file
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
