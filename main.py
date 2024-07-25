import asyncio
from parsers.eva_parser import EvaParser
from parsers.prostor_parser import ProstorParser
from pprint import pprint
# from parsers.watsons_parser import WatsonsParser


async def main():
    product_name = "Vichy Mineral 89"
    eva_parser = EvaParser()
    prostor_parser = ProstorParser()
    # watsons_parser = WatsonsParser()

    product_name = "Lash Sensational"
    eva_results = await eva_parser.search_product(product_name)
    prostor_results = await prostor_parser.search_product(product_name)

    if eva_results["status"] == "not_found":
        print(eva_results["message"])
    elif eva_results["status"] == "too_many_results":
        print(eva_results["message"])
    else:
        print("Eva Results:", eva_results["products"])

    if prostor_results["status"] == "not_found":
        print(prostor_results["message"])
    elif prostor_results["status"] == "too_many_results":
        print(prostor_results["message"])
    else:
        print("Prostor Results:", prostor_results["products"])

if __name__ == "__main__":
    asyncio.run(main())
