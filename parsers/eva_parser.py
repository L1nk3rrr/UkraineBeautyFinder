import urllib
from parsers.base_parser import BaseParser
from utils.random_utils import Randomizer

randomizer = Randomizer()


class EvaParser(BaseParser):
    BASE_URL = "https://api.multisearch.io/?id=10779&query={}&filters=true&categories=0&limit=40&lang=uk&fields=true"

    async def search_product(self, product_name: str):
        encoded_product_name = urllib.parse.quote(product_name)
        search_url = self.BASE_URL.format(encoded_product_name)
        json_response = await self.fetch_json(search_url)
        products = self._parse_search_results(json_response)
        return self.handle_search_results(products)

    async def parse_product(self, product_url: str):
        # Since the product details are already available in the search results, this might not be necessary.
        pass

    def _parse_search_results(self, json_response: dict):
        items = json_response.get("results", {}).get("items", [])
        products = []
        for item in items:
            product = {
                'name': item.get('name'),
                'price': item.get('price'),
                'oldprice': item.get('oldprice'),
                'url': item.get('url'),
                'image_url': item.get('picture'),
                'brand': item.get('brand'),
                'label': item.get('label'),
                'currency': item.get('currency'),
                'discountPercent': item.get('params_data', {}).get('discountPercent'),
                'stars': item.get('params_data', {}).get('Stars'),
                'reviews': item.get('params_data', {}).get('Відгуки'),
                'sku': item.get('params_data', {}).get('sku'),
                'id': item.get('id'),
            }
            products.append(product)
        return products
