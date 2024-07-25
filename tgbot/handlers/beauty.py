import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list

from tgbot.keyboards.inline import beauty_menu_keyboard
from parsers.eva_parser import EvaParser
from parsers.prostor_parser import ProstorParser

beauty_router = Router()
eva_parser = EvaParser()
prostor_parser = ProstorParser()

# In-memory storage for search results (could be replaced with a more persistent storage)
SEARCH_RESULTS = {}


@beauty_router.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Choose an option:", reply_markup=beauty_menu_keyboard())


@beauty_router.callback_query(lambda c: c.data == "search_product")
async def search_product(query: CallbackQuery):
    await query.message.answer("Please enter the product name:")
    await query.answer()


@beauty_router.message(F.text)
async def handle_search(message: Message):
    product_name = message.text
    eva_results = await eva_parser.search_product(product_name)
    prostor_results = await prostor_parser.search_product(product_name)

    if eva_results["status"] == "not_found":
        await message.answer(f"Eva: {eva_results['message']}")

    if prostor_results["status"] == "not_found":
        await message.answer(f"Prostor: {eva_results['message']}")

    if eva_results["status"] == "too_many_results":
        await message.answer(eva_results["message"] + " for Eva")

    if prostor_results["status"] == "too_many_results":
        await message.answer(prostor_results["message"] + " for Prostor")

    eva_products = eva_results.get("products", [])
    prostor_products = prostor_results.get("products", [])


    for product in eva_products:
        SEARCH_RESULTS[f"eva_{product['id']}"] = product

    for product in prostor_products:
        SEARCH_RESULTS[f"prostor_{product['id']}"] = product


    if len(eva_products) > 1:
        keyboard_eva = InlineKeyboardBuilder()
        for eva_product in eva_products:
            keyboard_eva.button(text=eva_product['name'], callback_data=f"eva_{eva_product['id']}")
        keyboard_eva.adjust(1)
        await message.answer("Multiple products found on EVA. Please select one:",
                             reply_markup=keyboard_eva.as_markup())
    elif len(eva_products) == 1:
        eva_product = eva_products[0]
        await message.answer(
            f"<b>Eva:</b> found one product:\n"
            f"Name: {eva_product['name']}\n"
            f"Price: {eva_product['price']} {eva_product['currency']}\n"
            f"URL: {eva_product['url']}"
        )

    if len(prostor_products) > 1:
        keyboard_prostor = InlineKeyboardBuilder()
        for prostor_product in prostor_products:
            keyboard_prostor.button(text=prostor_product['name'], callback_data=f"prostor_{prostor_product['id']}")
        keyboard_prostor.adjust(1)
        await message.answer("Multiple products found on Prostor. Please select one:",
                             reply_markup=keyboard_prostor.as_markup())
    elif len(prostor_products) == 1:
        prostor_product = prostor_products[0]
        await message.answer(
            f"<b>Prostor:</b> found one product:\n"
            f"Name: {prostor_product['name']}\n"
            f"Price: {prostor_product['price']} {prostor_product['currency']}\n"
            f"URL: {prostor_product['url']}"
        )


@beauty_router.callback_query(F.data.startswith("eva_") | F.data.startswith("prostor_"))
async def show_product_details(query: CallbackQuery):
    product_id = query.data
    print(product_id)
    label = "Eva" if product_id.startswith("eva_") else "Prostor"

    # Retrieve the product details from the global dictionary
    product = SEARCH_RESULTS.get(product_id)

    if product:
        text = (
            f"<b>{label}:</b>\n"
            f"Name: {product['name']}\n"
            f"Price: {product['price']} {product['currency']}\n"
            f"Brand: {product.get('brand', 'N/A')}\n"
            f"URL: {product['url']}"
        )
        await query.message.answer(text, parse_mode=ParseMode.HTML)
    else:
        await query.message.answer("Product not found.")

    await query.answer()