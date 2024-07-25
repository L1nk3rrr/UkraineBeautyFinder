import urllib.parse
from parsers.base_parser import BaseParser


class ProstorParser(BaseParser):
    BASE_URL = "https://api.multisearch.io/?id=10958&query={}&filters=true&categories=0&limit=40&lang=uk&fields=true"

    async def search_product(self, product_name: str):
        # Make the search query URL-safe
        encoded_product_name = urllib.parse.quote(product_name)
        search_url = self.BASE_URL.format(encoded_product_name)
        json_response = await self.fetch_json(search_url)
        products = self._parse_search_results(json_response)
        return self.handle_search_results(products)

    async def parse_product(self, product_url: str):
        # This can be expanded if we need to fetch more details from the product URL
        pass

    def _parse_search_results(self, json_response: dict):
        item_groups = json_response.get("results", {}).get("items", [])
        products = []

        for item in item_groups:
            product = {
                'name': item.get('name'),
                'price': item.get('price'),
                'oldprice': item.get('oldprice'),
                'url': item.get('url'),
                'image_url': item.get('picture'),
                'brand': item.get('brand'),
                'currency': item.get('currency'),
                'is_presence': item.get('is_presence'),
                'id': item.get('id'),
            }
            products.append(product)
        return products