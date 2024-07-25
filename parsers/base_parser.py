import logging

from abc import ABC, abstractmethod
import aiohttp
from utils.random_utils import Randomizer

randomizer = Randomizer()


class BaseParser(ABC):

    async def fetch(self, url: str):
        headers = {'User-Agent': randomizer.user_agent}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.text()

    async def fetch_json(self, url: str):
        headers = {'User-Agent': randomizer.user_agent}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.json()

    def handle_search_results(self, products):
        logging.info(f"Got products - {len(products)} ")
        if len(products) == 0:
            return {"status": "not_found", "message": "No products found for this search term."}
        elif len(products) > 15:
            return {"status": "too_many_results", "message": "Too many results. Please provide a more specific search term."}
        else:
            return {"status": "ok", "products": products}

    @abstractmethod
    async def search_product(self, product_name: str):
        """Search for products on the site and return a list of results."""
        pass

    @abstractmethod
    async def parse_product(self, product_url: str):
        """Parse a specific product page and return product details."""
        pass
