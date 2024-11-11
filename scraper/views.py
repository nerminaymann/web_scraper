import requests
import pandas as pd
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ScraperSerializer


class ScraperView(APIView):
    def post(self, request):
        serializer = ScraperSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            response = requests.get(url)

            if response.status_code != 200:
                return Response({'error': 'Failed to retrieve the URL'},
                                status=status.HTTP_400_BAD_REQUEST)

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the data
            data = []
            item_data = {'url': url}
            titles = soup.find_all(['h1', 'h2', 'div','meta'],
                                   class_=lambda class_name: class_name and 'title' in class_name)
            for title in titles:
                title_text = title.get_text(strip=True)
                if title_text:
                    item_data['title'] = title_text

            descriptions = soup.find_all(['p', 'span', 'div','meta'],
                                         class_=lambda class_name: class_name and 'description' in class_name)
            for desc in descriptions:
                desc_text = desc.get_text(strip=True)
                if desc_text:
                    item_data['description'] = desc_text

            prices = soup.find_all(class_=lambda class_name: class_name and 'price' in class_name)
            for price in prices:
                price_text = price.get_text(strip=True)
                if price_text:
                    item_data['price'] = price_text

            images = soup.find_all('img', src=True)
            for img in images:
                img_src = img['src']
                if img_src:
                    item_data['image'] = img_src

            data.append(item_data)

            # Convert the data into a DataFrame and export to CSV or Excel
            df = pd.DataFrame(data)

            # Save to CSV
            csv_path = 'scraped_data.csv'
            df.to_csv(csv_path, index=False)

            # Save to Excel
            excel_path = 'scraped_data.xlsx'
            df.to_excel(excel_path, index=False)

            return Response({
                'csv_file': csv_path,
                'excel_file': excel_path
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
