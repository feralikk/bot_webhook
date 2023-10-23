import logging
import json
import re

from django.http import HttpResponse
from django.views import View
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Avg, Min
from django.db.models import Q
from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters, Dispatcher
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from wood_informant.models import Profile, Message, Statuses, Products, Cities, Regions, Countries, Types, \
    WoodTypes, Wets, Actual, Previous, SubTypes, WoodSubTypes

logging.basicConfig(filename="bot.log", level=logging.ERROR,
       format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger()

bot = Bot(token=settings.TOKEN)
dispatcher = Dispatcher(bot, update_queue=None, workers=4, use_context=True)

buy_flag = False
sell_flag = False

# Общие
CALLBACK_BUTTON_BACKTOREALITY = "callback_button_backtoreality"
CALLBACK_BUTTON1_PRODUCT = "callback_button1_product"
CALLBACK_BUTTON2_PRODUCT = "callback_button2_product"
CALLBACK_BUTTON3_PRODUCT = "callback_button3_product"
CALLBACK_BUTTON1_COUNTRY = "callback_button1_country"
CALLBACK_BUTTON2_COUNTRY = "callback_button2_country"
CALLBACK_BUTTON3_COUNTRY = "callback_button3_country"
CALLBACK_BUTTON4_COUNTRY = "callback_button4_country"
CALLBACK_BUTTON5_COUNTRY = "callback_button5_country"
CALLBACK_BUTTON6_COUNTRY = "callback_button6_country"
CALLBACK_BUTTON7_COUNTRY = "callback_button7_country"
CALLBACK_BUTTON8_COUNTRY = "callback_button8_country"
CALLBACK_REGION_BUTTON_BACK = "CALLBACK_REGION_BUTTON_BACK"
CALLBACK_REGION_BUTTON1_BACK = "CALLBACK_REGION_BUTTON1_BACK"
CALLBACK_REGION_BUTTON2_BACK = "CALLBACK_REGION_BUTTON2_BACK"
CALLBACK_REGION_BUTTON3_BACK = "CALLBACK_REGION_BUTTON3_BACK"
CALLBACK_REGION_BUTTON4_BACK = "CALLBACK_REGION_BUTTON4_BACK"
CALLBACK_REGION_BUTTON5_BACK = "CALLBACK_REGION_BUTTON5_BACK"
CALLBACK_REGION_BUTTON_MORE = "CALLBACK_REGION_BUTTON_MORE"
CALLBACK_REGION_BUTTON1_MORE = "CALLBACK_REGION_BUTTON1_MORE"
CALLBACK_REGION_BUTTON2_MORE = "CALLBACK_REGION_BUTTON2_MORE"
CALLBACK_REGION_BUTTON3_MORE = "CALLBACK_REGION_BUTTON3_MORE"
CALLBACK_REGION_BUTTON4_MORE = "CALLBACK_REGION_BUTTON4_MORE"
CALLBACK_REGION_BUTTON5_MORE = "CALLBACK_REGION_BUTTON5_MORE"
CALLBACK_REGION_BUTTON_SKIP = "CALLBACK_REGION_BUTTON_SKIP"
# CALLBACK_BUTTON9_COUNTRY = "callback_button9_country"
# CALLBACK_BUTTON10_COUNTRY = "callback_button10_country"
# CALLBACK_BUTTON11_COUNTRY = "callback_button11_country"
# CALLBACK_BUTTON12_COUNTRY = "callback_button12_country"
# CALLBACK_BUTTON13_COUNTRY = "callback_button13_country"
# CALLBACK_BUTTON14_COUNTRY = "callback_button14_country"
# CALLBACK_BUTTON15_COUNTRY = "callback_button15_country"
# CALLBACK_BUTTON16_COUNTRY = "callback_button16_country"
# CALLBACK_BUTTON17_COUNTRY = "callback_button17_country"
# CALLBACK_BUTTON18_COUNTRY = "callback_button18_country"
# CALLBACK_BUTTON19_COUNTRY = "callback_button19_country"
CALLBACK_BUTTON1_REGION = "callback_button1_region"
CALLBACK_BUTTON2_REGION = "callback_button2_region"
CALLBACK_BUTTON3_REGION = "callback_button3_region"
CALLBACK_BUTTON4_REGION = "callback_button4_region"
CALLBACK_BUTTON5_REGION = "callback_button5_region"
CALLBACK_BUTTON6_REGION = "callback_button6_region"
CALLBACK_BUTTON7_REGION = "callback_button7_region"
CALLBACK_BUTTON8_REGION = "callback_button8_region"
CALLBACK_BUTTON9_REGION = "callback_button9_region"
CALLBACK_BUTTON10_REGION = "callback_button10_region"
CALLBACK_BUTTON11_REGION = "callback_button11_region"
CALLBACK_BUTTON12_REGION = "callback_button12_region"
CALLBACK_BUTTON13_REGION = "callback_button13_region"
CALLBACK_BUTTON14_REGION = "callback_button14_region"
CALLBACK_BUTTON15_REGION = "callback_button15_region"
CALLBACK_BUTTON16_REGION = "callback_button16_region"
CALLBACK_BUTTON17_REGION = "callback_button17_region"
CALLBACK_BUTTON18_REGION = "callback_button18_region"
CALLBACK_BUTTON19_REGION = "callback_button19_region"
CALLBACK_BUTTON20_REGION = "callback_button20_region"
CALLBACK_BUTTON21_REGION = "callback_button21_region"
CALLBACK_BUTTON22_REGION = "callback_button22_region"
CALLBACK_BUTTON23_REGION = "callback_button23_region"
CALLBACK_BUTTON24_REGION = "callback_button24_region"
CALLBACK_BUTTON25_REGION = "callback_button25_region"
CALLBACK_BUTTON26_REGION = "callback_button26_region"
CALLBACK_BUTTON27_REGION = "callback_button27_region"
CALLBACK_BUTTON28_REGION = "callback_button28_region"
CALLBACK_BUTTON29_REGION = "callback_button29_region"
CALLBACK_BUTTON30_REGION = "callback_button30_region"
CALLBACK_BUTTON31_REGION = "callback_button31_region"
CALLBACK_BUTTON32_REGION = "callback_button32_region"
CALLBACK_BUTTON33_REGION = "callback_button33_region"
CALLBACK_BUTTON34_REGION = "callback_button34_region"
CALLBACK_BUTTON35_REGION = "callback_button35_region"
CALLBACK_BUTTON36_REGION = "callback_button36_region"
CALLBACK_BUTTON37_REGION = "callback_button37_region"
CALLBACK_BUTTON38_REGION = "callback_button38_region"
CALLBACK_BUTTON39_REGION = "callback_button39_region"
CALLBACK_BUTTON40_REGION = "callback_button40_region"
CALLBACK_BUTTON41_REGION = "callback_button41_region"
CALLBACK_BUTTON42_REGION = "callback_button42_region"
CALLBACK_BUTTON43_REGION = "callback_button43_region"
CALLBACK_BUTTON44_REGION = "callback_button44_region"
CALLBACK_BUTTON45_REGION = "callback_button45_region"
CALLBACK_BUTTON46_REGION = "callback_button46_region"
CALLBACK_BUTTON47_REGION = "callback_button47_region"
CALLBACK_BUTTON48_REGION = "callback_button48_region"
CALLBACK_BUTTON49_REGION = "callback_button49_region"
CALLBACK_BUTTON50_REGION = "callback_button50_region"
CALLBACK_BUTTON51_REGION = "callback_button51_region"
CALLBACK_BUTTON52_REGION = "callback_button52_region"
CALLBACK_BUTTON53_REGION = "callback_button53_region"
CALLBACK_BUTTON54_REGION = "callback_button54_region"
CALLBACK_BUTTON55_REGION = "callback_button55_region"
CALLBACK_BUTTON56_REGION = "callback_button56_region"
CALLBACK_BUTTON57_REGION = "callback_button57_region"
CALLBACK_BUTTON58_REGION = "callback_button58_region"
CALLBACK_BUTTON59_REGION = "callback_button59_region"
CALLBACK_BUTTON60_REGION = "callback_button60_region"
CALLBACK_BUTTON61_REGION = "callback_button61_region"
CALLBACK_BUTTON62_REGION = "callback_button62_region"
CALLBACK_BUTTON63_REGION = "callback_button63_region"
CALLBACK_BUTTON64_REGION = "callback_button64_region"
CALLBACK_BUTTON65_REGION = "callback_button65_region"
CALLBACK_BUTTON66_REGION = "callback_button66_region"
CALLBACK_BUTTON67_REGION = "callback_button67_region"
CALLBACK_BUTTON68_REGION = "callback_button68_region"
CALLBACK_BUTTON69_REGION = "callback_button69_region"
CALLBACK_BUTTON70_REGION = "callback_button70_region"
CALLBACK_BUTTON71_REGION = "callback_button71_region"
CALLBACK_BUTTON72_REGION = "callback_button72_region"
CALLBACK_BUTTON73_REGION = "callback_button73_region"
CALLBACK_BUTTON74_REGION = "callback_button74_region"
CALLBACK_BUTTON75_REGION = "callback_button75_region"
CALLBACK_BUTTON76_REGION = "callback_button76_region"
CALLBACK_BUTTON77_REGION = "callback_button77_region"
CALLBACK_BUTTON78_REGION = "callback_button78_region"
CALLBACK_BUTTON79_REGION = "callback_button79_region"
CALLBACK_BUTTON80_REGION = "callback_button80_region"
CALLBACK_BUTTON81_REGION = "callback_button81_region"
CALLBACK_BUTTON82_REGION = "callback_button82_region"
CALLBACK_BUTTON83_REGION = "callback_button83_region"
# Пиломатералы
CALLBACK_LUMBER_BUTTON1_BACK = "callback_lumber_button1_back"
CALLBACK_LUMBER_BUTTON2_BACK = "callback_lumber_button2_back"
CALLBACK_LUMBER_BUTTON3_BACK = "callback_lumber_button3_back"
CALLBACK_LUMBER_BUTTON4_BACK = "callback_lumber_button4_back"
CALLBACK_LUMBER_BUTTON5_BACK = "callback_lumber_button5_back"
CALLBACK_LUMBER_BUTTON1_TYPE = "callback_lumber_button1_type"
CALLBACK_LUMBER_BUTTON2_TYPE = "callback_lumber_button2_type"
CALLBACK_LUMBER_BUTTON3_TYPE = "callback_lumber_button3_type"
CALLBACK_LUMBER_BUTTON4_TYPE = "callback_lumber_button4_type"
CALLBACK_LUMBER_BUTTON5_TYPE = "callback_lumber_button5_type"
CALLBACK_LUMBER_BUTTON6_TYPE = "callback_lumber_button6_type"
CALLBACK_LUMBER_BUTTON7_TYPE = "callback_lumber_button7_type"
CALLBACK_LUMBER_BUTTON8_TYPE = "callback_lumber_button8_type"
CALLBACK_LUMBER_BUTTON9_TYPE = "callback_lumber_button9_type"
CALLBACK_LUMBER_BUTTON10_TYPE = "callback_lumber_button10_type"
CALLBACK_LUMBER_BUTTON11_TYPE = "callback_lumber_button11_type"
CALLBACK_LUMBER_BUTTON1_MORE = "callback_lumber_button1_more"
CALLBACK_LUMBER_BUTTON2_MORE = "callback_lumber_button2_more"
CALLBACK_LUMBER_BUTTON3_MORE = "callback_lumber_button3_more"
CALLBACK_LUMBER_BUTTON4_MORE = "callback_lumber_button4_more"
CALLBACK_LUMBER_BUTTON5_MORE = "callback_lumber_button5_more"
CALLBACK_LUMBER_BUTTON10_MORE = "callback_lumber_button10_more"
CALLBACK_LUMBER_BUTTON11_MORE = "callback_lumber_button11_more"
CALLBACK_LUMBER_BUTTON12_MORE = "callback_lumber_button12_more"
CALLBACK_LUMBER_BUTTON13_MORE = "callback_lumber_button13_more"
CALLBACK_LUMBER_BUTTON1_WOOD = "callback_lumber_button1_wood"
CALLBACK_LUMBER_BUTTON2_WOOD = "callback_lumber_button2_wood"
CALLBACK_LUMBER_BUTTON3_WOOD = "callback_lumber_button3_wood"
CALLBACK_LUMBER_BUTTON4_WOOD = "callback_lumber_button4_wood"
CALLBACK_LUMBER_BUTTON5_WOOD = "callback_lumber_button5_wood"
CALLBACK_LUMBER_BUTTON6_WOOD = "callback_lumber_button6_wood"
CALLBACK_LUMBER_BUTTON7_WOOD = "callback_lumber_button7_wood"
CALLBACK_LUMBER_BUTTON8_WOOD = "callback_lumber_button8_wood"
CALLBACK_LUMBER_BUTTON9_WOOD = "callback_lumber_button9_wood"
CALLBACK_LUMBER_BUTTON10_WOOD = "callback_lumber_button10_wood"
CALLBACK_LUMBER_BUTTON11_WOOD = "callback_lumber_button11_wood"
CALLBACK_LUMBER_BUTTON12_WOOD = "callback_lumber_button12_wood"
CALLBACK_LUMBER_BUTTON13_WOOD = "callback_lumber_button13_wood"
CALLBACK_LUMBER_BUTTON14_WOOD = "callback_lumber_button14_wood"
CALLBACK_LUMBER_BUTTON15_WOOD = "callback_lumber_button15_wood"
CALLBACK_LUMBER_BUTTON16_WOOD = "callback_lumber_button16_wood"
CALLBACK_LUMBER_BUTTON17_WOOD = "callback_lumber_button17_wood"
CALLBACK_LUMBER_BUTTON18_WOOD = "callback_lumber_button18_wood"
CALLBACK_LUMBER_BUTTON19_WOOD = "callback_lumber_button19_wood"
CALLBACK_LUMBER_BUTTON20_WOOD = "callback_lumber_button20_wood"
CALLBACK_BUTTON1_PRICE = "callback_button1_price"
CALLBACK_BUTTON2_PRICE = "callback_button2_price"
CALLBACK_BUTTON3_PRICE = "callback_button3_price"
CALLBACK_BUTTON4_PRICE = "callback_button4_price"
CALLBACK_BUTTON5_PRICE = "callback_button5_price"
CALLBACK_BUTTON6_PRICE = "callback_button6_price"
CALLBACK_LUMBER_BUTTON_YES = "callback_lumber_button_yes"
CALLBACK_LUMBER_BUTTON_NO = "callback_lumber_button_no"
CALLBACK_LUMBER_BUTTON1_WET = "CALLBACK_LUMBER_BUTTON1_WET"
CALLBACK_LUMBER_BUTTON2_WET = "CALLBACK_LUMBER_BUTTON2_WET"
CALLBACK_LUMBER_BUTTON1_SKIP = "callback_lumber_button1_skip"
CALLBACK_LUMBER_BUTTON2_SKIP = "callback_lumber_button2_skip"
CALLBACK_LUMBER_BUTTON3_SKIP = "callback_lumber_button3_skip"
CALLBACK_LUMBER_BUTTON4_SKIP = "callback_lumber_button4_skip"
CALLBACK_LUMBER_BUTTON_LENGTH = "callback_lumber_button_length"
CALLBACK_LUMBER_BUTTON_WIDTH = "callback_lumber_button3_width"
CALLBACK_LUMBER_BUTTON_THICK = "callback_lumber_button3_thick"
# Погонаж
CALLBACK_PAGONAGE_BUTTON1_TYPE = "callback_pagonage_button1_type"
CALLBACK_PAGONAGE_BUTTON2_TYPE = "callback_pagonage_button2_type"
CALLBACK_PAGONAGE_BUTTON3_TYPE = "callback_pagonage_button3_type"
CALLBACK_PAGONAGE_BUTTON4_TYPE = "callback_pagonage_button4_type"
CALLBACK_PAGONAGE_BUTTON5_TYPE = "callback_pagonage_button5_type"
CALLBACK_PAGONAGE_BUTTON6_TYPE = "callback_pagonage_button6_type"
CALLBACK_PAGONAGE_BUTTON7_TYPE = "callback_pagonage_button7_type"
CALLBACK_PAGONAGE_BUTTON8_TYPE = "callback_pagonage_button8_type"
CALLBACK_PAGONAGE_BUTTON9_TYPE = "callback_pagonage_button9_type"
CALLBACK_PAGONAGE_BUTTON10_TYPE = "callback_pagonage_button10_type"
CALLBACK_PAGONAGE_BUTTON11_TYPE = "callback_pagonage_button11_type"
CALLBACK_PAGONAGE_BUTTON12_TYPE = "callback_pagonage_button12_type"
CALLBACK_PAGONAGE_BUTTON13_TYPE = "callback_pagonage_button13_type"
CALLBACK_PAGONAGE_BUTTON14_TYPE = "callback_pagonage_button14_type"
CALLBACK_PAGONAGE_BUTTON15_TYPE = "callback_pagonage_button15_type"
CALLBACK_PAGONAGE_BUTTON16_TYPE = "callback_pagonage_button16_type"
CALLBACK_PAGONAGE_BUTTON17_TYPE = "callback_pagonage_button17_type"
CALLBACK_PAGONAGE_BUTTON1_WOOD = "callback_pagonage_button1_wood"
CALLBACK_PAGONAGE_BUTTON2_WOOD = "callback_pagonage_button2_wood"
CALLBACK_PAGONAGE_BUTTON3_WOOD = "callback_pagonage_button3_wood"
CALLBACK_PAGONAGE_BUTTON4_WOOD = "callback_pagonage_button4_wood"
CALLBACK_PAGONAGE_BUTTON5_WOOD = "callback_pagonage_button5_wood"
CALLBACK_PAGONAGE_BUTTON6_WOOD = "callback_pagonage_button6_wood"
CALLBACK_PAGONAGE_BUTTON7_WOOD = "callback_pagonage_button7_wood"
CALLBACK_PAGONAGE_BUTTON8_WOOD = "callback_pagonage_button8_wood"
CALLBACK_PAGONAGE_BUTTON9_WOOD = "callback_pagonage_button9_wood"
CALLBACK_PAGONAGE_BUTTON10_WOOD = "callback_pagonage_button10_wood"
CALLBACK_PAGONAGE_BUTTON11_WOOD = "callback_pagonage_button11_wood"
CALLBACK_PAGONAGE_BUTTON12_WOOD = "callback_pagonage_button12_wood"
CALLBACK_PAGONAGE_BUTTON1_WET = "CALLBACK_PAGONAGE_BUTTON1_WET"
CALLBACK_PAGONAGE_BUTTON2_WET = "CALLBACK_PAGONAGE_BUTTON2_WET"
CALLBACK_PAGONAGE_BUTTON3_WET = "CALLBACK_PAGONAGE_BUTTON3_WET"
CALLBACK_PAGONAGE_BUTTON1_BACK = "callback_pagonage_button1_back"
CALLBACK_PAGONAGE_BUTTON2_BACK = "callback_pagonage_button2_back"
CALLBACK_PAGONAGE_BUTTON3_BACK = "callback_pagonage_button3_back"
CALLBACK_PAGONAGE_BUTTON1_MORE = "callback_pagonage_button1_more"
CALLBACK_PAGONAGE_BUTTON2_MORE = "callback_pagonage_button2_more"
CALLBACK_PAGONAGE_BUTTON3_MORE = "callback_pagonage_button3_more"
CALLBACK_PAGONAGE_BUTTON1_SKIP = "callback_pagonage_button1_skip"
CALLBACK_PAGONAGE_BUTTON2_SKIP = "callback_pagonage_button2_skip"
CALLBACK_PAGONAGE_BUTTON3_SKIP = "callback_pagonage_button3_skip"
# Пеллеты
CALLBACK_PELLETS_BUTTON1_TYPE = "callback_pellets_button1_type"
CALLBACK_PELLETS_BUTTON2_TYPE = "callback_pellets_button2_type"
CALLBACK_PELLETS_BUTTON3_TYPE = "callback_pellets_button3_type"
CALLBACK_PELLETS_BUTTON4_TYPE = "callback_pellets_button4_type"
CALLBACK_PELLETS_BUTTON5_TYPE = "callback_pellets_button5_type"
CALLBACK_PELLETS_BUTTON6_TYPE = "callback_pellets_button6_type"
CALLBACK_PELLETS_BUTTON1_BACK = "callback_pellets_button1_back"
CALLBACK_PELLETS_BUTTON1_MORE = "callback_pellets_button1_more"
CALLBACK_PELLETS_BUTTON2_MORE = "callback_pellets_button2_more"
CALLBACK_PELLETS_BUTTON3_MORE = "callback_pellets_button3_more"
CALLBACK_PELLETS_BUTTON1_SKIP = "CALLBACK_PELLETS_BUTTON1_SKIP"

TITLES = {
    CALLBACK_BUTTON_BACKTOREALITY: "Вернуться к выбору параметров",
    CALLBACK_REGION_BUTTON_BACK: "Выбрать продукцию ⬅️",
    CALLBACK_REGION_BUTTON1_BACK: "Назад ⬅️",
    CALLBACK_REGION_BUTTON2_BACK: "Назад ⬅️",
    CALLBACK_REGION_BUTTON3_BACK: "Назад ⬅️",
    CALLBACK_REGION_BUTTON4_BACK: "Назад ⬅️",
    CALLBACK_REGION_BUTTON5_BACK: "Назад ⬅️",
    CALLBACK_REGION_BUTTON_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON1_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON2_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON3_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON4_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON5_MORE: "Ещё ➡️",
    CALLBACK_REGION_BUTTON_SKIP: "Выбрать всё",
    CALLBACK_BUTTON1_PRODUCT: "Пиломатериалы",
    CALLBACK_BUTTON2_PRODUCT: "Погонаж",
    CALLBACK_BUTTON3_PRODUCT: "Пеллеты",
    CALLBACK_BUTTON1_COUNTRY: "Россия",
    CALLBACK_BUTTON2_COUNTRY: "Белоруссия",
    CALLBACK_BUTTON3_COUNTRY: "Австрия",
    CALLBACK_BUTTON4_COUNTRY: "Китай",
    CALLBACK_BUTTON5_COUNTRY: "Эстония",
    CALLBACK_BUTTON6_COUNTRY: "Латвия",
    CALLBACK_BUTTON7_COUNTRY: "Литва",
    CALLBACK_BUTTON8_COUNTRY: "Польша",
    # CALLBACK_BUTTON9_COUNTRY: "Южная Корея",
    # CALLBACK_BUTTON10_COUNTRY: "Франция",
    # CALLBACK_BUTTON11_COUNTRY: "Грузия",
    # CALLBACK_BUTTON12_COUNTRY: "Германия",
    # CALLBACK_BUTTON13_COUNTRY: "Великобритания",
    # CALLBACK_BUTTON14_COUNTRY: "Венгрия",
    # CALLBACK_BUTTON15_COUNTRY: "Италия",
    # CALLBACK_BUTTON16_COUNTRY: "Казахстан",
    # CALLBACK_BUTTON17_COUNTRY: "Киргизия",
    # CALLBACK_BUTTON18_COUNTRY: "Коста-Рика",
    # CALLBACK_BUTTON19_COUNTRY: "Чехия",
    # CALLBACK_BUTTON20_COUNTRY: "Малайзия",
    # CALLBACK_BUTTON21_COUNTRY: "Молдавия",
    # CALLBACK_BUTTON22_COUNTRY: "Нидерланды",
    # CALLBACK_BUTTON23_COUNTRY: "Норвегия",
    # CALLBACK_BUTTON24_COUNTRY: "Египет",
    # CALLBACK_BUTTON25_COUNTRY: "Румыния",
    # CALLBACK_BUTTON26_COUNTRY: "Словения",
    # CALLBACK_BUTTON27_COUNTRY: "Испания",
    # CALLBACK_BUTTON28_COUNTRY: "Швеция",
    # CALLBACK_BUTTON29_COUNTRY: "Швейцария",
    # CALLBACK_BUTTON30_COUNTRY: "Судан",
    # CALLBACK_BUTTON31_COUNTRY: "Турция",
    # CALLBACK_BUTTON32_COUNTRY: "Туркменистан",
    # CALLBACK_BUTTON33_COUNTRY: "Украина",
    # CALLBACK_BUTTON34_COUNTRY: "ОАЭ",
    # CALLBACK_BUTTON35_COUNTRY: "Узбекистан",
    # CALLBACK_BUTTON36_COUNTRY: "Вьетнам",
    # CALLBACK_BUTTON37_COUNTRY: "Болгария",
    # CALLBACK_BUTTON38_COUNTRY: "Ирак",
    # CALLBACK_BUTTON39_COUNTRY: "Иордания",
    # CALLBACK_BUTTON40_COUNTRY: "Канада",
    # CALLBACK_BUTTON41_COUNTRY: "США",
    # CALLBACK_BUTTON42_COUNTRY: "Саудовская Аравия",
    # CALLBACK_BUTTON43_COUNTRY: "Иран",
    # CALLBACK_BUTTON44_COUNTRY: "Словакия",
    # CALLBACK_BUTTON45_COUNTRY: "Финляндия",
}
    # Пиломатериалы
LUMBER_TITLES1 = {
    CALLBACK_LUMBER_BUTTON11_MORE: "Необрезные ➡️",
    CALLBACK_LUMBER_BUTTON12_MORE: "Лиственные ➡️",
    CALLBACK_LUMBER_BUTTON5_BACK: "Хвойные ⬅️",
}
LUMBER_TITLES = {
    CALLBACK_LUMBER_BUTTON1_BACK: "Выбрать регион ⬅️",
    CALLBACK_LUMBER_BUTTON2_BACK: "Выбрать тип ⬅️",
    CALLBACK_LUMBER_BUTTON3_BACK: "Выбрать древесину ⬅️",
    CALLBACK_LUMBER_BUTTON4_BACK: "Назад ⬅️",
    CALLBACK_LUMBER_BUTTON1_MORE: "Ещё 5 ⚡️",
    CALLBACK_LUMBER_BUTTON2_MORE: "Ещё 5 ⚡️",
    CALLBACK_LUMBER_BUTTON3_MORE: "Ещё 10 ⚡️",
    CALLBACK_LUMBER_BUTTON4_MORE: "Ещё 5 ⚡️",
    CALLBACK_LUMBER_BUTTON5_MORE: "Ещё 5 ⚡️",
    CALLBACK_LUMBER_BUTTON10_MORE: "Ещё ➡️",
    CALLBACK_LUMBER_BUTTON13_MORE: "Ещё ➡️",
    CALLBACK_LUMBER_BUTTON1_TYPE: "Обрезные:Все",
    CALLBACK_LUMBER_BUTTON2_TYPE: "Обрезные:Доска",
    CALLBACK_LUMBER_BUTTON3_TYPE: "Обрезные:Брус",
    CALLBACK_LUMBER_BUTTON4_TYPE: "Обрезные:Брусок",
    CALLBACK_LUMBER_BUTTON5_TYPE: "Необрезные:Все",
    CALLBACK_LUMBER_BUTTON6_TYPE: "Необрезные:Доска",
    CALLBACK_LUMBER_BUTTON7_TYPE: "Необрезные:Лафет",
    CALLBACK_LUMBER_BUTTON8_TYPE: "Строганые:Все",
    CALLBACK_LUMBER_BUTTON9_TYPE: "Строганые:Доска",
    CALLBACK_LUMBER_BUTTON10_TYPE: "Строганые:Брус",
    CALLBACK_LUMBER_BUTTON11_TYPE: "Строганые:Брусок",
    CALLBACK_LUMBER_BUTTON1_WET: "Естественная",
    CALLBACK_LUMBER_BUTTON2_WET: "Сухой лес",
    CALLBACK_LUMBER_BUTTON1_WOOD: "Хвойные:все",
    CALLBACK_LUMBER_BUTTON2_WOOD: "Хвойные:сосна",
    CALLBACK_LUMBER_BUTTON3_WOOD: "Хвойные:пихта",
    CALLBACK_LUMBER_BUTTON4_WOOD: "Хвойные:ель",
    CALLBACK_LUMBER_BUTTON5_WOOD: "Хвойные:кедр",
    CALLBACK_LUMBER_BUTTON6_WOOD: "Хвойные:лиственница",
    CALLBACK_LUMBER_BUTTON7_WOOD: "Лиственные:все",
    CALLBACK_LUMBER_BUTTON8_WOOD: "Лиственные:берёза",
    CALLBACK_LUMBER_BUTTON9_WOOD: "Лиственные:осина",
    CALLBACK_LUMBER_BUTTON10_WOOD: "Лиственные:дуб",
    CALLBACK_LUMBER_BUTTON11_WOOD: "Лиственные:бук",
    CALLBACK_LUMBER_BUTTON12_WOOD: "Лиственные:липа",
    CALLBACK_LUMBER_BUTTON13_WOOD: "Лиственные:клён",
    CALLBACK_LUMBER_BUTTON14_WOOD: "Лиственные:каштан",
    CALLBACK_LUMBER_BUTTON15_WOOD: "Лиственные:карагач",
    CALLBACK_LUMBER_BUTTON16_WOOD: "Лиственные:ольха",
    CALLBACK_LUMBER_BUTTON17_WOOD: "Лиственные:ясень",
    CALLBACK_LUMBER_BUTTON18_WOOD: "Лиственные:бальса",
    CALLBACK_LUMBER_BUTTON19_WOOD: "Лиственные:тополь",
    CALLBACK_LUMBER_BUTTON20_WOOD: "Лиственные:ива",
    CALLBACK_LUMBER_BUTTON_YES: "Да",
    CALLBACK_LUMBER_BUTTON_NO: "Нет",
    CALLBACK_LUMBER_BUTTON1_SKIP: "Выбрать всё",
    CALLBACK_LUMBER_BUTTON2_SKIP: "Выбрать всё",
    CALLBACK_LUMBER_BUTTON3_SKIP: "Выбрать всё",
    CALLBACK_LUMBER_BUTTON4_SKIP: "Выбрать всё",
    CALLBACK_LUMBER_BUTTON_LENGTH: "Пропустить",
    CALLBACK_LUMBER_BUTTON_WIDTH: "Пропустить",
    CALLBACK_LUMBER_BUTTON_THICK: "Пропустить",
    }

PAGONAGE_TITLES = {
    # Погонаж
    CALLBACK_PAGONAGE_BUTTON1_TYPE: "Вагонка",
    CALLBACK_PAGONAGE_BUTTON2_TYPE: "Плинтус",
    CALLBACK_PAGONAGE_BUTTON3_TYPE: "Полок",
    CALLBACK_PAGONAGE_BUTTON4_TYPE: "Половая доска",
    CALLBACK_PAGONAGE_BUTTON5_TYPE: "Террасная доска",
    CALLBACK_PAGONAGE_BUTTON6_TYPE: "Террасная доска из ДПК (Декинг)",
    CALLBACK_PAGONAGE_BUTTON7_TYPE: "Палубная доска",
    CALLBACK_PAGONAGE_BUTTON8_TYPE: "Рейка",
    CALLBACK_PAGONAGE_BUTTON9_TYPE: "Имитация бруса",
    CALLBACK_PAGONAGE_BUTTON10_TYPE: "Блок-хаус",
    CALLBACK_PAGONAGE_BUTTON11_TYPE: "Планкен",
    CALLBACK_PAGONAGE_BUTTON12_TYPE: "Наличник",
    CALLBACK_PAGONAGE_BUTTON13_TYPE: "Брусок строганный",
    CALLBACK_PAGONAGE_BUTTON14_TYPE: "Брусок сращенный строганный",
    CALLBACK_PAGONAGE_BUTTON15_TYPE: "Деревянные обои",
    CALLBACK_PAGONAGE_BUTTON16_TYPE: "Деревянная мозаика",
    CALLBACK_PAGONAGE_BUTTON17_TYPE: "Лунный паз",
    CALLBACK_PAGONAGE_BUTTON1_WOOD: "Лиственные:все",
    CALLBACK_PAGONAGE_BUTTON2_WOOD: "Лиственные:берёза",
    CALLBACK_PAGONAGE_BUTTON3_WOOD: "Лиственные:осина",
    CALLBACK_PAGONAGE_BUTTON4_WOOD: "Лиственные:дуб",
    CALLBACK_PAGONAGE_BUTTON5_WOOD: "Лиственные:липа",
    CALLBACK_PAGONAGE_BUTTON6_WOOD: "Лиственные:ясень",
    CALLBACK_PAGONAGE_BUTTON7_WOOD: "Хвойные:все",
    CALLBACK_PAGONAGE_BUTTON8_WOOD: "Хвойные:сосна",
    CALLBACK_PAGONAGE_BUTTON9_WOOD: "Хвойные:пихта",
    CALLBACK_PAGONAGE_BUTTON10_WOOD: "Хвойные:ель",
    CALLBACK_PAGONAGE_BUTTON11_WOOD: "Хвойные:кедр",
    CALLBACK_PAGONAGE_BUTTON12_WOOD: "Хвойные:лиственница",
    CALLBACK_PAGONAGE_BUTTON1_WET: "Естественная",
    CALLBACK_PAGONAGE_BUTTON2_WET: "Сухой лес",
    CALLBACK_PAGONAGE_BUTTON3_WET: "Термо модифицированная древесина",
    CALLBACK_PAGONAGE_BUTTON1_BACK: "Выбрать регион ⬅️",
    CALLBACK_PAGONAGE_BUTTON2_BACK: "Выбрать вид ⬅️",
    CALLBACK_PAGONAGE_BUTTON3_BACK: "Выбрать породу древесины ⬅️",
    CALLBACK_PAGONAGE_BUTTON1_MORE: "Ещё 5 ⚡️",
    CALLBACK_PAGONAGE_BUTTON2_MORE: "Ещё 5 ⚡️",
    CALLBACK_PAGONAGE_BUTTON3_MORE: "Ещё 10 ⚡️",
    CALLBACK_PAGONAGE_BUTTON1_SKIP: "Выбрать всё",
    CALLBACK_PAGONAGE_BUTTON2_SKIP: "Выбрать всё",
    CALLBACK_PAGONAGE_BUTTON3_SKIP: "Выбрать всё",
    }
PELLETS_TITLES = {
    # Пеллеты
    CALLBACK_PELLETS_BUTTON1_TYPE: "Пеллеты",
    CALLBACK_PELLETS_BUTTON2_TYPE: "Брикеты",
    CALLBACK_PELLETS_BUTTON3_TYPE: "Щепа",
    CALLBACK_PELLETS_BUTTON4_TYPE: "Опилки",
    CALLBACK_PELLETS_BUTTON5_TYPE: "Деревянная стружка",
    CALLBACK_PELLETS_BUTTON6_TYPE: "Древесная мука",
    CALLBACK_PELLETS_BUTTON1_BACK: "Выбрать регион ⬅️",
    CALLBACK_PELLETS_BUTTON1_MORE: "Ещё 5 ⚡️",
    CALLBACK_PELLETS_BUTTON2_MORE: "Ещё 5 ⚡️",
    CALLBACK_PELLETS_BUTTON3_MORE: "Ещё 10 ⚡️",
    CALLBACK_PELLETS_BUTTON1_SKIP: "Выбрать всё",
}

REGION_TITLES = {
CALLBACK_BUTTON1_REGION: "Алтайский край",
    CALLBACK_BUTTON2_REGION: "Амурская область",
    CALLBACK_BUTTON3_REGION: "Архангельская область",
    CALLBACK_BUTTON4_REGION: "Белгородская область",
    CALLBACK_BUTTON5_REGION: "Брянская область",
    CALLBACK_BUTTON6_REGION: "Владимирская область",
    CALLBACK_BUTTON7_REGION: "Волгоградская область",
    CALLBACK_BUTTON8_REGION: "Вологодская область",
    CALLBACK_BUTTON9_REGION: "Воронежская область",
    CALLBACK_BUTTON10_REGION: "город Москва",
    CALLBACK_BUTTON11_REGION: "город Санкт-Петербург",
    CALLBACK_BUTTON12_REGION: "город Севастополь",
    CALLBACK_BUTTON13_REGION: "Еврейская автономная область",
    CALLBACK_BUTTON14_REGION: "Забайкальский край",
    CALLBACK_BUTTON15_REGION: "Ивановская область",
    CALLBACK_BUTTON16_REGION: "Иркутская область",
    CALLBACK_BUTTON17_REGION: "Кабардино-Балкарская Республика",
    CALLBACK_BUTTON18_REGION: "Калининградская область",
    CALLBACK_BUTTON19_REGION: "Калужская область",
    CALLBACK_BUTTON20_REGION: "Камчатский край",
    CALLBACK_BUTTON21_REGION: "Карачаево-Черкесская Республика",
    CALLBACK_BUTTON22_REGION: "Кемеровская область",
    CALLBACK_BUTTON23_REGION: "Кировская область",
    CALLBACK_BUTTON24_REGION: "Костромская область",
    CALLBACK_BUTTON25_REGION: "Краснодарский край",
    CALLBACK_BUTTON26_REGION: "Красноярский край",
    CALLBACK_BUTTON27_REGION: "Курганская область",
    CALLBACK_BUTTON28_REGION: "Курская область",
    CALLBACK_BUTTON29_REGION: "Ленинградская область",
    CALLBACK_BUTTON30_REGION: "Липецкая область",
    CALLBACK_BUTTON31_REGION: "Магаданская область",
    CALLBACK_BUTTON32_REGION: "Московская область",
    CALLBACK_BUTTON33_REGION: "Мурманская область",
    CALLBACK_BUTTON34_REGION: "Нанецкий автономный округ",
    CALLBACK_BUTTON35_REGION: "Нижегородская область",
    CALLBACK_BUTTON36_REGION: "Новгородская область",
    CALLBACK_BUTTON37_REGION: "Новосибирская область",
    CALLBACK_BUTTON38_REGION: "Омская область",
    CALLBACK_BUTTON39_REGION: "Оренбургская область",
    CALLBACK_BUTTON40_REGION: "Орловская область",
    CALLBACK_BUTTON41_REGION: "Пензенская область",
    CALLBACK_BUTTON42_REGION: "Пермский край",
    CALLBACK_BUTTON43_REGION: "Приморский край",
    CALLBACK_BUTTON44_REGION: "Псковская область",
    CALLBACK_BUTTON45_REGION: "Республика Адыгея",
    CALLBACK_BUTTON46_REGION: "Республика Алтай",
    CALLBACK_BUTTON47_REGION: "Республика Башкортостан",
    CALLBACK_BUTTON48_REGION: "Республика Бурятия",
    CALLBACK_BUTTON49_REGION: "Республика Дагестан",
    CALLBACK_BUTTON50_REGION: "Республика Ингушетия",
    CALLBACK_BUTTON51_REGION: "Республика Калмыкия",
    CALLBACK_BUTTON52_REGION: "Республика Карелия",
    CALLBACK_BUTTON53_REGION: "Республика Коми",
    CALLBACK_BUTTON54_REGION: "Республика Крым",
    CALLBACK_BUTTON55_REGION: "Республика Марий Эл",
    CALLBACK_BUTTON56_REGION: "Республика Мордовия",
    CALLBACK_BUTTON57_REGION: "Республика Саха(Якутия)",
    CALLBACK_BUTTON58_REGION: "Республика Северная Осения",
    CALLBACK_BUTTON59_REGION: "Республика Татарстан",
    CALLBACK_BUTTON60_REGION: "Республика Тыва",
    CALLBACK_BUTTON61_REGION: "Республика Хакасия",
    CALLBACK_BUTTON62_REGION: "Ростовская область",
    CALLBACK_BUTTON63_REGION: "Рязанская область",
    CALLBACK_BUTTON64_REGION: "Самарская область",
    CALLBACK_BUTTON65_REGION: "Саратовская область",
    CALLBACK_BUTTON66_REGION: "Сахалинская область",
    CALLBACK_BUTTON67_REGION: "Свердловская область",
    CALLBACK_BUTTON68_REGION: "Смоленская область",
    CALLBACK_BUTTON69_REGION: "Ставропольский край",
    CALLBACK_BUTTON70_REGION: "Тамбовская область",
    CALLBACK_BUTTON71_REGION: "Тверская область",
    CALLBACK_BUTTON72_REGION: "Томская область",
    CALLBACK_BUTTON73_REGION: "Тульская область",
    CALLBACK_BUTTON74_REGION: "Тюменская область",
    CALLBACK_BUTTON75_REGION: "Удмуртская Республика",
    CALLBACK_BUTTON76_REGION: "Хабаровский край",
    CALLBACK_BUTTON77_REGION: "Ханты-Мансийский автономный округ - Югра",
    CALLBACK_BUTTON78_REGION: "Челябинская область",
    CALLBACK_BUTTON79_REGION: "Чеченская Республика",
    CALLBACK_BUTTON80_REGION: "Чувашская Республика",
    CALLBACK_BUTTON81_REGION: "Чукотский автономный округ",
    CALLBACK_BUTTON82_REGION: "Ямало-Ненецкий автономный округ",
    CALLBACK_BUTTON83_REGION: "Ярославская область",
}

def get_product_keybord():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_PRODUCT], callback_data=CALLBACK_BUTTON1_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_PRODUCT], callback_data=CALLBACK_BUTTON2_PRODUCT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_PRODUCT], callback_data=CALLBACK_BUTTON3_PRODUCT),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)



def skip_lumber_length_keybord():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_LUMBER_BUTTON_LENGTH], callback_data=CALLBACK_LUMBER_BUTTON_LENGTH),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def skip_lumber_width_keybord():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_LUMBER_BUTTON_WIDTH], callback_data=CALLBACK_LUMBER_BUTTON_WIDTH),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def skip_lumber_thick_keybord():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_LUMBER_BUTTON_THICK], callback_data=CALLBACK_LUMBER_BUTTON_THICK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagonage_keyboard4():
    keyboard = [
        [
            InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON1_MORE], callback_data=CALLBACK_PAGONAGE_BUTTON1_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagonage_keyboard5():
    keyboard = [
        [
            InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON2_MORE], callback_data=CALLBACK_PAGONAGE_BUTTON2_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagonage_keyboard6():
    keyboard = [
        [
            InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON3_MORE], callback_data=CALLBACK_PAGONAGE_BUTTON3_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pellets_keyboard4():
    keyboard = [
        [
            InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON1_MORE], callback_data=CALLBACK_PELLETS_BUTTON1_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pellets_keyboard5():
    keyboard = [
        [
            InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON2_MORE], callback_data=CALLBACK_PELLETS_BUTTON2_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pellets_keyboard6():
    keyboard = [
        [
            InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON3_MORE], callback_data=CALLBACK_PELLETS_BUTTON3_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_lumber_keyboard4():
    keyboard = [
        [
            InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON1_MORE], callback_data=CALLBACK_LUMBER_BUTTON1_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_lumber_keyboard5():
    keyboard = [
        [
            InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON2_MORE], callback_data=CALLBACK_LUMBER_BUTTON2_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_lumber_keyboard6():
    keyboard = [
        [
            InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON3_MORE], callback_data=CALLBACK_LUMBER_BUTTON3_MORE),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_reality():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_BACKTOREALITY], callback_data=CALLBACK_BUTTON_BACKTOREALITY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rows(**kwargs):
    q_filters = {}
    for key, value in kwargs.items():
        if key == 'get_status':
            if value:
                q_filters['status'] = value
        if key == 'get_product':
            if value:
                q_filters['product'] = value
        if key == 'get_region':
            if value:
                q_filters['region'] = value
        if key == 'get_lprice':
            if value:
                q_filters['price__gte'] = value
        if key == 'get_gprice':
            if value:
                q_filters['price__lt'] = value
        if key == 'get_type':
            if value:
                q_filters['type'] = value
        if key == 'get_subtype':
            if value:
                q_filters['subtype'] = value
        if key == 'get_wood_type':
            if value:
                q_filters['wood_type'] = value
        if key == 'get_wood_subtype':
            if value:
                q_filters['wood_subtype'] = value
        if key == 'get_wet':
            if value:
                q_filters['wet'] = value

    if q_filters:
        return Actual.objects.filter(**q_filters)
    else:
        return Actual.objects.all()

def keyboard_callback_handler(update: Update, context: CallbackContext):
    """ Обработчик ВСЕХ кнопок со ВСЕХ клавиатур
    """
    global sell_flag, buy_flag, product, region, status
    global rl_lumber, lm_type, lm_subtype, lprice_lumber, gprice_lumber, wood_type_lumber, wood_subtype_lumber, wet_lumber
    global rl_pagonage, pagonage_type, wood_type_pagonage, wood_subtype_pagonage, wet_pagonage
    global rl_pellets, pellets_type
    global keyboard_region, keyboard1_region, keyboard2_region, keyboard3_region, keyboard4_region, keyboard5_region
    global keyboard_pellets, keyboard_lumber_type, keyboard_lumber_woodtype, keyboard_lumber_wet
    global keyboard_pagonage_type, keyboard_pagonage_woodtype, keyboard_pagonage_wet, keyboard_lumber_price
    global lw_price_list, gt_price_list
    query = update.callback_query
    data = query.data

    # Обратите внимание: используется `effective_message`
    chat_id = update.effective_message.chat_id
    current_text = update.effective_message.text

    if data == CALLBACK_BUTTON_BACKTOREALITY:
        context.bot.send_message(
            chat_id=chat_id,
            text='Выберите тип продукции',
            reply_markup=get_product_keybord(),
        )
    elif data == CALLBACK_REGION_BUTTON_SKIP:
        region = None
        if str(product) == "Пиломатериалы":
            lumber_type_tmp = []
            lumber_type_buttons = []
            lumber_subtype_buttons = []
            # lumber_subtype_query = []
            keyboard_lumber_type = []

            lumber_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related(
                'type').order_by(
                'type').distinct().values('type')
            for obj_type in lumber_type_query:
                if obj_type.get('type') is None:
                    continue
                lum_type = Types.objects.get(
                    type_id=obj_type.get('type')
                )
                lumber_type_tmp.append(lum_type)
            # print('TYPE:', lumber_type_tmp, "\n")
            # for item in lumber_type_tmp:
            #     for key, value in LUMBER_TITLES.items():
            #         if value.find(str(item)) != -1:
            #             lumber_type_buttons.append(key)
            # print(lumber_type_buttons)
            for lumber_type in lumber_type_tmp:
                lumber_subtype_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lumber_type).select_related(
                    'subtype').order_by('subtype').distinct().values('subtype')
                lumber_subtype_tmp = []
                lumber_subtype_tmp.append("все")
                for obj_subtype in lumber_subtype_query:
                    if obj_subtype.get('subtype') is None:
                        continue
                    lum_subtype = SubTypes.objects.get(
                        subtype_id=obj_subtype.get('subtype')
                    )
                    lumber_subtype_tmp.append(lum_subtype)

                # print('SUBTYPE:', lumber_subtype_tmp, '\n')
                for item in lumber_subtype_tmp:
                    for key, value in LUMBER_TITLES.items():
                        if re.search(f'{str(item)}$', value.lower()) and value.find(str(lumber_type)) != -1:
                            lumber_subtype_buttons.append(key)
                # print('BUTTONS: ', lumber_subtype_buttons)
            for lumber_button in lumber_subtype_buttons:
                keyboard_lumber_type.append([
                    InlineKeyboardButton(LUMBER_TITLES[lumber_button], callback_data=lumber_button)
                ])
            keyboard_lumber_type.append(
                [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON1_BACK],
                                      callback_data=CALLBACK_LUMBER_BUTTON1_BACK),
                 ])
            keyboard_lumber_type.append(
                [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON1_SKIP],
                                      callback_data=CALLBACK_LUMBER_BUTTON1_SKIP)])

            query.edit_message_text(
                text="Выберите тип пиломатериалов",
                reply_markup=InlineKeyboardMarkup(keyboard_lumber_type),
            )
        if str(product) == "Погонаж":
            pagonage_type_tmp = []
            pagonage_type_buttons = []
            keyboard_pagonage_type = []

            pagonage_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related(
                'type').order_by(
                'type').distinct().values('type')
            for obj_type in pagonage_type_query:
                if obj_type.get('type') is None:
                    continue
                pag_type = Types.objects.get(
                    type_id=obj_type.get('type')
                )
                pagonage_type_tmp.append(pag_type)

            for pagon_type in pagonage_type_tmp:
                for key, value in PAGONAGE_TITLES.items():
                    if str(value) == str(pagon_type):
                        pagonage_type_buttons.append(key)

            for pagonage_button in pagonage_type_buttons:
                keyboard_pagonage_type.append([
                    InlineKeyboardButton(PAGONAGE_TITLES[pagonage_button], callback_data=pagonage_button)
                ])
            keyboard_pagonage_type.append(
                [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON1_BACK],
                                      callback_data=CALLBACK_PAGONAGE_BUTTON1_BACK),
                 ])
            keyboard_pagonage_type.append(
                [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON1_SKIP],
                                      callback_data=CALLBACK_PAGONAGE_BUTTON1_SKIP)])
            query.edit_message_text(
                text="Выберите вид",
                reply_markup=InlineKeyboardMarkup(keyboard_pagonage_type),
            )
        if str(product) == "Пеллеты":
            pellets_type_tmp = []
            keyboard_pellets_tmp = []
            keyboard_pellets = []
            pellets_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related(
                'type').order_by(
                'type').distinct().values('type')
            # get_rows(get_status=status, get_product=product, get_region=region)
            for obj in pellets_type_query:
                if obj.get('type') is None:
                    continue
                pel_type = Types.objects.get(
                    type_id=obj.get('type')
                )
                pellets_type_tmp.append(pel_type)

            for item in pellets_type_tmp:
                for key, value in PELLETS_TITLES.items():
                    if str(value) == str(item):
                        keyboard_pellets_tmp.append(key)
            # while index < len(keyboard_pellets_tmp):

            for pellet_type in keyboard_pellets_tmp:
                keyboard_pellets.append([
                    InlineKeyboardButton(PELLETS_TITLES[pellet_type], callback_data=pellet_type)
                ])
            keyboard_pellets.append(
                [InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON1_BACK],
                                      callback_data=CALLBACK_PELLETS_BUTTON1_BACK),
                 ])
            keyboard_pellets.append(
                [InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON1_SKIP],
                                      callback_data=CALLBACK_PELLETS_BUTTON1_SKIP)])
            query.edit_message_text(
                text="Выберите тип",
                reply_markup=InlineKeyboardMarkup(keyboard_pellets),
            )
    elif data == CALLBACK_REGION_BUTTON_BACK:
        query.edit_message_text(
            text="Выберите тип продукции",
            reply_markup=get_product_keybord(),
        )
    elif data in (CALLBACK_BUTTON1_REGION, CALLBACK_BUTTON2_REGION, CALLBACK_BUTTON3_REGION, CALLBACK_BUTTON4_REGION,
                  CALLBACK_BUTTON5_REGION, CALLBACK_BUTTON6_REGION, CALLBACK_BUTTON7_REGION, CALLBACK_BUTTON8_REGION,
                  CALLBACK_BUTTON9_REGION, CALLBACK_BUTTON10_REGION, CALLBACK_BUTTON11_REGION, CALLBACK_BUTTON12_REGION,
                  CALLBACK_BUTTON13_REGION, CALLBACK_BUTTON14_REGION, CALLBACK_BUTTON15_REGION, CALLBACK_BUTTON16_REGION,
                  CALLBACK_BUTTON17_REGION, CALLBACK_BUTTON18_REGION, CALLBACK_BUTTON19_REGION, CALLBACK_BUTTON20_REGION,
                  CALLBACK_BUTTON21_REGION, CALLBACK_BUTTON22_REGION, CALLBACK_BUTTON23_REGION, CALLBACK_BUTTON24_REGION,
                  CALLBACK_BUTTON25_REGION, CALLBACK_BUTTON26_REGION, CALLBACK_BUTTON27_REGION, CALLBACK_BUTTON28_REGION,
                  CALLBACK_BUTTON29_REGION, CALLBACK_BUTTON30_REGION, CALLBACK_BUTTON31_REGION, CALLBACK_BUTTON31_REGION,
                  CALLBACK_BUTTON32_REGION, CALLBACK_BUTTON33_REGION, CALLBACK_BUTTON34_REGION, CALLBACK_BUTTON35_REGION,
                  CALLBACK_BUTTON36_REGION, CALLBACK_BUTTON37_REGION, CALLBACK_BUTTON38_REGION, CALLBACK_BUTTON39_REGION,
                  CALLBACK_BUTTON40_REGION, CALLBACK_BUTTON41_REGION, CALLBACK_BUTTON42_REGION, CALLBACK_BUTTON43_REGION,
                  CALLBACK_BUTTON44_REGION, CALLBACK_BUTTON45_REGION, CALLBACK_BUTTON46_REGION, CALLBACK_BUTTON47_REGION,
                  CALLBACK_BUTTON48_REGION, CALLBACK_BUTTON49_REGION, CALLBACK_BUTTON50_REGION, CALLBACK_BUTTON51_REGION,
                  CALLBACK_BUTTON52_REGION, CALLBACK_BUTTON53_REGION, CALLBACK_BUTTON54_REGION, CALLBACK_BUTTON55_REGION,
                  CALLBACK_BUTTON56_REGION, CALLBACK_BUTTON57_REGION, CALLBACK_BUTTON58_REGION, CALLBACK_BUTTON59_REGION,
                  CALLBACK_BUTTON60_REGION, CALLBACK_BUTTON61_REGION, CALLBACK_BUTTON62_REGION, CALLBACK_BUTTON63_REGION,
                  CALLBACK_BUTTON64_REGION, CALLBACK_BUTTON65_REGION, CALLBACK_BUTTON66_REGION, CALLBACK_BUTTON67_REGION,
                  CALLBACK_BUTTON68_REGION, CALLBACK_BUTTON69_REGION, CALLBACK_BUTTON70_REGION, CALLBACK_BUTTON71_REGION,
                  CALLBACK_BUTTON72_REGION, CALLBACK_BUTTON73_REGION, CALLBACK_BUTTON74_REGION, CALLBACK_BUTTON75_REGION,
                  CALLBACK_BUTTON76_REGION, CALLBACK_BUTTON77_REGION, CALLBACK_BUTTON78_REGION, CALLBACK_BUTTON79_REGION,
                  CALLBACK_BUTTON80_REGION, CALLBACK_BUTTON81_REGION, CALLBACK_BUTTON82_REGION, CALLBACK_BUTTON83_REGION):
        region_tmp = {
            CALLBACK_BUTTON1_REGION: "Алтайский край",
            CALLBACK_BUTTON2_REGION: "Амурская область",
            CALLBACK_BUTTON3_REGION: "Архангельская область",
            CALLBACK_BUTTON4_REGION: "Белгородская область",
            CALLBACK_BUTTON5_REGION: "Брянская область",
            CALLBACK_BUTTON6_REGION: "Владимирская область",
            CALLBACK_BUTTON7_REGION: "Волгоградская область",
            CALLBACK_BUTTON8_REGION: "Вологодская область",
            CALLBACK_BUTTON9_REGION: "Воронежская область",
            CALLBACK_BUTTON10_REGION: "город Москва",
            CALLBACK_BUTTON11_REGION: "город Санкт-Петербург",
            CALLBACK_BUTTON12_REGION: "город Севастополь",
            CALLBACK_BUTTON13_REGION: "Еврейская автономная область",
            CALLBACK_BUTTON14_REGION: "Забайкальский край",
            CALLBACK_BUTTON15_REGION: "Ивановская область",
            CALLBACK_BUTTON16_REGION: "Иркутская область",
            CALLBACK_BUTTON17_REGION: "Кабардино-Балкарская Республика",
            CALLBACK_BUTTON18_REGION: "Калининградская область",
            CALLBACK_BUTTON19_REGION: "Калужская область",
            CALLBACK_BUTTON20_REGION: "Камчатский край",
            CALLBACK_BUTTON21_REGION: "Карачаево-Черкесская Республика",
            CALLBACK_BUTTON22_REGION: "Кемеровская область",
            CALLBACK_BUTTON23_REGION: "Кировская область",
            CALLBACK_BUTTON24_REGION: "Костромская область",
            CALLBACK_BUTTON25_REGION: "Краснодарский край",
            CALLBACK_BUTTON26_REGION: "Красноярский край",
            CALLBACK_BUTTON27_REGION: "Курганская область",
            CALLBACK_BUTTON28_REGION: "Курская область",
            CALLBACK_BUTTON29_REGION: "Ленинградская область",
            CALLBACK_BUTTON30_REGION: "Липецкая область",
            CALLBACK_BUTTON31_REGION: "Магаданская область",
            CALLBACK_BUTTON32_REGION: "Московская область",
            CALLBACK_BUTTON33_REGION: "Мурманская область",
            CALLBACK_BUTTON34_REGION: "Нанецкий автономный округ",
            CALLBACK_BUTTON35_REGION: "Нижегородская область",
            CALLBACK_BUTTON36_REGION: "Новгородская область",
            CALLBACK_BUTTON37_REGION: "Новосибирская область",
            CALLBACK_BUTTON38_REGION: "Омская область",
            CALLBACK_BUTTON39_REGION: "Оренбургская область",
            CALLBACK_BUTTON40_REGION: "Орловская область",
            CALLBACK_BUTTON41_REGION: "Пензенская область",
            CALLBACK_BUTTON42_REGION: "Пермский край",
            CALLBACK_BUTTON43_REGION: "Приморский край",
            CALLBACK_BUTTON44_REGION: "Псковская область",
            CALLBACK_BUTTON45_REGION: "Республика Адыгея",
            CALLBACK_BUTTON46_REGION: "Республика Алтай",
            CALLBACK_BUTTON47_REGION: "Республика Башкортостан",
            CALLBACK_BUTTON48_REGION: "Республика Бурятия",
            CALLBACK_BUTTON49_REGION: "Республика Дагестан",
            CALLBACK_BUTTON50_REGION: "Республика Ингушетия",
            CALLBACK_BUTTON51_REGION: "Республика Калмыкия",
            CALLBACK_BUTTON52_REGION: "Республика Карелия",
            CALLBACK_BUTTON53_REGION: "Республика Коми",
            CALLBACK_BUTTON54_REGION: "Республика Крым",
            CALLBACK_BUTTON55_REGION: "Республика Марий Эл",
            CALLBACK_BUTTON56_REGION: "Республика Мордовия",
            CALLBACK_BUTTON57_REGION: "Республика Саха(Якутия)",
            CALLBACK_BUTTON58_REGION: "Республика Северная Осения",
            CALLBACK_BUTTON59_REGION: "Республика Татарстан",
            CALLBACK_BUTTON60_REGION: "Республика Тыва",
            CALLBACK_BUTTON61_REGION: "Республика Хакасия",
            CALLBACK_BUTTON62_REGION: "Ростовская область",
            CALLBACK_BUTTON63_REGION: "Рязанская область",
            CALLBACK_BUTTON64_REGION: "Самарская область",
            CALLBACK_BUTTON65_REGION: "Саратовская область",
            CALLBACK_BUTTON66_REGION: "Сахалинская область",
            CALLBACK_BUTTON67_REGION: "Свердловская область",
            CALLBACK_BUTTON68_REGION: "Смоленская область",
            CALLBACK_BUTTON69_REGION: "Ставропольский край",
            CALLBACK_BUTTON70_REGION: "Тамбовская область",
            CALLBACK_BUTTON71_REGION: "Тверская область",
            CALLBACK_BUTTON72_REGION: "Томская область",
            CALLBACK_BUTTON73_REGION: "Тульская область",
            CALLBACK_BUTTON74_REGION: "Тюменская область",
            CALLBACK_BUTTON75_REGION: "Удмуртская Республика",
            CALLBACK_BUTTON76_REGION: "Хабаровский край",
            CALLBACK_BUTTON77_REGION: "Ханты-Мансийский автономный округ - Югра",
            CALLBACK_BUTTON78_REGION: "Челябинская область",
            CALLBACK_BUTTON79_REGION: "Чеченская Республика",
            CALLBACK_BUTTON80_REGION: "Чувашская Республика",
            CALLBACK_BUTTON81_REGION: "Чукотский автономный округ",
            CALLBACK_BUTTON82_REGION: "Ямало-Ненецкий автономный округ",
            CALLBACK_BUTTON83_REGION: "Ярославская область",
        }[data]
        region, _ = Regions.objects.get_or_create(
            region=region_tmp
        )
        if str(product) == "Пиломатериалы":
            lumber_type_tmp = []
            lumber_type_buttons = []
            lumber_subtype_buttons = []
            # lumber_subtype_query = []
            keyboard_lumber_type = []

            lumber_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related('type').order_by(
                'type').distinct().values('type')
            for obj_type in lumber_type_query:
                if obj_type.get('type') is None:
                    continue
                lum_type = Types.objects.get(
                    type_id=obj_type.get('type')
                )
                lumber_type_tmp.append(lum_type)
            # print('TYPE:', lumber_type_tmp, "\n")
            # for item in lumber_type_tmp:
            #     for key, value in LUMBER_TITLES.items():
            #         if value.find(str(item)) != -1:
            #             lumber_type_buttons.append(key)
            # print(lumber_type_buttons)
            for lumber_type in lumber_type_tmp:
                lumber_subtype_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lumber_type).select_related(
                    'subtype').order_by('subtype').distinct().values('subtype')
                lumber_subtype_tmp = []
                lumber_subtype_tmp.append("все")
                for obj_subtype in lumber_subtype_query:
                    if obj_subtype.get('subtype') is None:
                        continue
                    lum_subtype = SubTypes.objects.get(
                        subtype_id=obj_subtype.get('subtype')
                    )
                    lumber_subtype_tmp.append(lum_subtype)

                # print('SUBTYPE:', lumber_subtype_tmp, '\n')
                for item in lumber_subtype_tmp:
                    for key, value in LUMBER_TITLES.items():
                        if re.search(f'{str(item)}$', value.lower()) and value.find(str(lumber_type)) != -1:
                            lumber_subtype_buttons.append(key)
                # print('BUTTONS: ', lumber_subtype_buttons)
            for lumber_button in lumber_subtype_buttons:
                keyboard_lumber_type.append([
                    InlineKeyboardButton(LUMBER_TITLES[lumber_button], callback_data=lumber_button)
                ])
            keyboard_lumber_type.append(
                [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON1_BACK], callback_data=CALLBACK_LUMBER_BUTTON1_BACK),
                 ])
            keyboard_lumber_type.append(
                [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON1_SKIP], callback_data=CALLBACK_LUMBER_BUTTON1_SKIP)])

            query.edit_message_text(
                text="Выберите тип пиломатериалов",
                reply_markup=InlineKeyboardMarkup(keyboard_lumber_type),
            )
        if str(product) == "Погонаж":
            pagonage_type_tmp = []
            pagonage_type_buttons = []
            keyboard_pagonage_type = []

            pagonage_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related(
                'type').order_by(
                'type').distinct().values('type')
            for obj_type in pagonage_type_query:
                if obj_type.get('type') is None:
                    continue
                pag_type = Types.objects.get(
                    type_id=obj_type.get('type')
                )
                pagonage_type_tmp.append(pag_type)

            for pagon_type in pagonage_type_tmp:
                for key, value in PAGONAGE_TITLES.items():
                    if str(value) == str(pagon_type):
                        pagonage_type_buttons.append(key)

            for pagonage_button in pagonage_type_buttons:
                keyboard_pagonage_type.append([
                    InlineKeyboardButton(PAGONAGE_TITLES[pagonage_button], callback_data=pagonage_button)
                ])
            keyboard_pagonage_type.append(
                [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON1_BACK],
                                      callback_data=CALLBACK_PAGONAGE_BUTTON1_BACK),
                 ])
            keyboard_pagonage_type.append(
                [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON1_SKIP],
                                      callback_data=CALLBACK_PAGONAGE_BUTTON1_SKIP)])

            query.edit_message_text(
                text="Выберите вид",
                reply_markup=InlineKeyboardMarkup(keyboard_pagonage_type),
            )
        if str(product) == "Пеллеты":
            pellets_type_tmp = []
            keyboard_pellets_tmp = []
            keyboard_pellets = []
            pellets_type_query = get_rows(get_status=status, get_product=product, get_region=region).select_related(
                'type').order_by(
                'type').distinct().values('type')
            for obj in pellets_type_query:
                if obj.get('type') is None:
                    continue
                pel_type = Types.objects.get(
                    type_id=obj.get('type')
                )
                pellets_type_tmp.append(pel_type)
            for item in pellets_type_tmp:
                for key, value in PELLETS_TITLES.items():
                    if str(value) == str(item):
                        keyboard_pellets_tmp.append(key)
            # while index < len(keyboard_pellets_tmp):
            for pellet_type in keyboard_pellets_tmp:
                keyboard_pellets.append([
                    InlineKeyboardButton(PELLETS_TITLES[pellet_type], callback_data=pellet_type)
                ])
            keyboard_pellets.append(
                [InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON1_BACK], callback_data=CALLBACK_PELLETS_BUTTON1_BACK),
                 ])
            keyboard_pellets.append(
                [InlineKeyboardButton(PELLETS_TITLES[CALLBACK_PELLETS_BUTTON1_SKIP], callback_data=CALLBACK_PELLETS_BUTTON1_SKIP)])

            query.edit_message_text(
                text="Выберите тип",
                reply_markup=InlineKeyboardMarkup(keyboard_pellets),
            )

    # Пиломатериалы
    elif data == CALLBACK_LUMBER_BUTTON11_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_lumber_type_keybord1(),
        )
    elif data == CALLBACK_LUMBER_BUTTON12_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_lumber_wood_keybord2(),
        )
    elif data == CALLBACK_LUMBER_BUTTON1_BACK:
        query.edit_message_text(
            text='Выберите регион',
            reply_markup=InlineKeyboardMarkup(keyboard_region),
        )
    elif data == CALLBACK_LUMBER_BUTTON2_BACK:
        query.edit_message_text(
            text="Выберите тип пиломатериалов",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_type),
        )
    elif data == CALLBACK_LUMBER_BUTTON3_BACK:
        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_woodtype),
        )
    # elif data == CALLBACK_BUTTON5_BACK:
    #     query.edit_message_text(
    #         text="Выберите тип",
    #         reply_markup=get_type_keybord2(),
    #     )
    elif data == CALLBACK_LUMBER_BUTTON1_SKIP:
        lm_type = None
        lm_subtype = None
        lumber_woodtype_tmp = []
        lumber_woodsubtype_buttons = []
        # lumber_subtype_query = []
        keyboard_lumber_woodtype = []

        lumber_woodtype_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type, get_subtype=lm_subtype).select_related(
            'wood_type').order_by(
            'wood_type').distinct().values('wood_type')
        for obj_woodtype in lumber_woodtype_query:
            if obj_woodtype.get('wood_type') is None:
                continue
            lum_woodtype = WoodTypes.objects.get(
                wood_type_id=obj_woodtype.get('wood_type')
            )
            lumber_woodtype_tmp.append(lum_woodtype)
        for lumber_woodtype in lumber_woodtype_tmp:
            lumber_woodsubtype_query = get_rows(get_status=status, get_product=product, get_region=region,
                                                get_type=lm_type, get_subtype=lm_subtype).select_related(
                    'wood_subtype').order_by('wood_subtype').distinct().values('wood_subtype')
            lumber_woodsubtype_tmp = []
            lumber_woodsubtype_tmp.append("все")
            for obj_woodsubtype in lumber_woodsubtype_query:
                if obj_woodsubtype.get('wood_subtype') is None:
                    continue
                lum_woodsubtype = WoodSubTypes.objects.get(
                    wood_subtype_id=obj_woodsubtype.get('wood_subtype')
                )
                lumber_woodsubtype_tmp.append(lum_woodsubtype)

            # print('SUBTYPE:', lumber_subtype_tmp, '\n')
            for item in lumber_woodsubtype_tmp:
                for key, value in LUMBER_TITLES.items():
                    if re.search(f'{str(item)}$', value.lower()) and value.find(str(lumber_woodtype)) != -1:
                        lumber_woodsubtype_buttons.append(key)
            # print('BUTTONS: ', lumber_subtype_buttons)
        for lumber_button in lumber_woodsubtype_buttons:
            keyboard_lumber_woodtype.append([
                InlineKeyboardButton(LUMBER_TITLES[lumber_button], callback_data=lumber_button)
            ])
        keyboard_lumber_woodtype.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON2_BACK],
                                  callback_data=CALLBACK_LUMBER_BUTTON2_BACK),
             ])
        keyboard_lumber_woodtype.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON2_SKIP],
                                  callback_data=CALLBACK_LUMBER_BUTTON2_SKIP)])
        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_woodtype),
        )

    elif data == CALLBACK_LUMBER_BUTTON2_SKIP:
        wood_type_lumber = None
        wood_subtype_lumber = None
        lumber_wet_tmp = []
        lumber_wet_buttons = []
        keyboard_lumber_wet = []

        lumber_wet_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type,
                                    get_subtype=lm_subtype, get_wood_type=wood_type_lumber,
                                    get_wood_subtype=wood_subtype_lumber).select_related(
            'wet').order_by('wet').distinct().values('wet')
        for obj in lumber_wet_query:
            if obj.get('wet') is None:
                continue
            lum_wet = Wets.objects.get(
                wet_id=obj.get('wet')
            )
            lumber_wet_tmp.append(lum_wet)
        for item in lumber_wet_tmp:
            for key, value in LUMBER_TITLES.items():
                if str(value) == str(item):
                    lumber_wet_buttons.append(key)
        # while index < len(keyboard_pellets_tmp):
        for wet_button in lumber_wet_buttons:
            keyboard_lumber_wet.append([
                InlineKeyboardButton(LUMBER_TITLES[wet_button], callback_data=wet_button)
            ])
        keyboard_lumber_wet.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON4_SKIP],
                                  callback_data=CALLBACK_LUMBER_BUTTON4_SKIP)])

        query.edit_message_text(
            text="Выберите влажность",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_wet)
        )

    elif data == CALLBACK_BUTTON1_PRODUCT:
        product, _ = Products.objects.get_or_create(
            product="Пиломатериалы"
        )
        try:
            if sell_flag == True:
                status_tmp = "Покупка"
            if buy_flag == True:
                status_tmp = 'Продажа'
            status, _ = Statuses.objects.get_or_create(
                status=status_tmp
            )
            keyboard_region = []
            keyboard1_region = []
            keyboard2_region = []
            keyboard3_region = []
            keyboard4_region = []
            keyboard5_region = []
            keyboard_tmp = []
            regions_tmp = []
            index = 0
            regions_query = get_rows(get_status=status, get_product=product).select_related('region').order_by(
                'region').distinct().values('region')
            for obj in regions_query:
                reg = Regions.objects.get(
                    region_id=obj.get('region')
                )
                regions_tmp.append(str(reg))
            for item in sorted(regions_tmp):
                for key, value in REGION_TITLES.items():
                    if str(value) == str(item):
                        keyboard_tmp.append(key)
            while index < len(keyboard_tmp):
                if index < 22:
                    try:
                        keyboard_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 22 and index < 44:
                    try:
                        keyboard1_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard1_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 44 and index < 66:
                    try:
                        keyboard2_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard2_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 66 and index < 88:
                    try:
                        keyboard3_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard3_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 88 and index < 110:
                    try:
                        keyboard4_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard4_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 110:
                    try:
                        keyboard5_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard5_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                index += 2

            if index >= 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK], callback_data=CALLBACK_REGION_BUTTON_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON_MORE)
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP], callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index < 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK], callback_data=CALLBACK_REGION_BUTTON_BACK),
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP], callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON1_MORE)
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 22 and index < 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON2_MORE)
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 44 and index < 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON3_MORE)
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 66 and index < 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON4_MORE)
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 88 and index < 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON5_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON5_BACK)])
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            query.edit_message_text(
                text='Выберите регион',
                reply_markup=InlineKeyboardMarkup(keyboard_region),
            )
        except Exception as e:
            print(e)
        # except UnboundLocalError:
        #     query.edit_message_text(
        #         text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
        #     )
    elif data == CALLBACK_REGION_BUTTON1_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard_region),
        )
    elif data == CALLBACK_REGION_BUTTON2_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard1_region),
        )
    elif data == CALLBACK_REGION_BUTTON3_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard2_region),
        )

    elif data == CALLBACK_REGION_BUTTON4_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard3_region),
        )
    elif data == CALLBACK_REGION_BUTTON5_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard4_region),
        )
    elif data == CALLBACK_REGION_BUTTON_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard1_region),
        )
    elif data == CALLBACK_REGION_BUTTON1_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard2_region),
        )
    elif data == CALLBACK_REGION_BUTTON2_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard3_region),
        )
    elif data == CALLBACK_REGION_BUTTON3_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard4_region),
        )
    elif data == CALLBACK_REGION_BUTTON4_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=InlineKeyboardMarkup(keyboard5_region),
        )

    elif data in (CALLBACK_LUMBER_BUTTON1_TYPE, CALLBACK_LUMBER_BUTTON2_TYPE, CALLBACK_LUMBER_BUTTON3_TYPE, CALLBACK_LUMBER_BUTTON4_TYPE,
                  CALLBACK_LUMBER_BUTTON5_TYPE, CALLBACK_LUMBER_BUTTON6_TYPE, CALLBACK_LUMBER_BUTTON7_TYPE, CALLBACK_LUMBER_BUTTON8_TYPE,
                  CALLBACK_LUMBER_BUTTON9_TYPE, CALLBACK_LUMBER_BUTTON10_TYPE, CALLBACK_LUMBER_BUTTON11_TYPE):
        text = 'Предложения на рынке:\n'
        lm_type_tmp = {
            CALLBACK_LUMBER_BUTTON1_TYPE: 'Обрезные',
            CALLBACK_LUMBER_BUTTON2_TYPE: 'Обрезные',
            CALLBACK_LUMBER_BUTTON3_TYPE: 'Обрезные',
            CALLBACK_LUMBER_BUTTON4_TYPE: 'Обрезные',
            CALLBACK_LUMBER_BUTTON5_TYPE: 'Необрезные',
            CALLBACK_LUMBER_BUTTON6_TYPE: 'Необрезные',
            CALLBACK_LUMBER_BUTTON7_TYPE: 'Необрезные',
            CALLBACK_LUMBER_BUTTON8_TYPE: 'Строганые',
            CALLBACK_LUMBER_BUTTON9_TYPE: 'Строганые',
            CALLBACK_LUMBER_BUTTON10_TYPE: 'Строганые',
            CALLBACK_LUMBER_BUTTON11_TYPE: 'Строганые',
        }[data]
        lm_subtype_tmp = {
            CALLBACK_LUMBER_BUTTON1_TYPE: None,
            CALLBACK_LUMBER_BUTTON2_TYPE: 'доска',
            CALLBACK_LUMBER_BUTTON3_TYPE: 'брус',
            CALLBACK_LUMBER_BUTTON4_TYPE: 'брусок',
            CALLBACK_LUMBER_BUTTON5_TYPE: None,
            CALLBACK_LUMBER_BUTTON6_TYPE: 'доска',
            CALLBACK_LUMBER_BUTTON7_TYPE: 'лафет',
            CALLBACK_LUMBER_BUTTON8_TYPE: None,
            CALLBACK_LUMBER_BUTTON9_TYPE: 'доска',
            CALLBACK_LUMBER_BUTTON10_TYPE: 'брус',
            CALLBACK_LUMBER_BUTTON11_TYPE: 'брусок',
        }[data]

        lm_type, _ = Types.objects.get_or_create(
            type=lm_type_tmp
        )
        try:
            lm_subtype = SubTypes.objects.get(
                subtype=lm_subtype_tmp
            )
        except:
            lm_subtype = None

        lumber_woodtype_tmp = []
        lumber_woodtype_keyboard = []
        lumber_woodsubtype_buttons = []
        # lumber_subtype_query = []
        keyboard_lumber_woodtype = []

        lumber_woodtype_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type, get_subtype=lm_subtype).select_related(
            'wood_type').order_by(
            'wood_type').distinct().values('wood_type')
        for obj_woodtype in lumber_woodtype_query:
            if obj_woodtype.get('wood_type') is None:
                continue
            lum_woodtype = WoodTypes.objects.get(
                wood_type_id=obj_woodtype.get('wood_type')
            )
            lumber_woodtype_tmp.append(lum_woodtype)
        for lumber_woodtype in lumber_woodtype_tmp:
            lumber_woodsubtype_query = get_rows(get_status=status, get_product=product, get_region=region,
                                                get_type=lm_type, get_subtype=lm_subtype).select_related(
                    'wood_subtype').order_by('wood_subtype').distinct().values('wood_subtype')
            lumber_woodsubtype_tmp = []
            lumber_woodsubtype_tmp.append("все")
            for obj_woodsubtype in lumber_woodsubtype_query:
                lum_woodsubtype = WoodSubTypes.objects.get(
                    wood_subtype_id=obj_woodsubtype.get('wood_subtype')
                )
                lumber_woodsubtype_tmp.append(lum_woodsubtype)

            # print('SUBTYPE:', lumber_subtype_tmp, '\n')
            for item in lumber_woodsubtype_tmp:
                for key, value in LUMBER_TITLES.items():
                    if re.search(f'{str(item)}$', value.lower()) and value.find(str(lumber_woodtype)) != -1:
                        lumber_woodsubtype_buttons.append(key)
            # print('BUTTONS: ', lumber_subtype_buttons)
        for lumber_button in lumber_woodsubtype_buttons:
            keyboard_lumber_woodtype.append([
                InlineKeyboardButton(LUMBER_TITLES[lumber_button], callback_data=lumber_button)
            ])
        keyboard_lumber_woodtype.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON2_BACK],
                                  callback_data=CALLBACK_LUMBER_BUTTON2_BACK),
             ])
        keyboard_lumber_woodtype.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON2_SKIP],
                                  callback_data=CALLBACK_LUMBER_BUTTON2_SKIP)])
        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_woodtype),
        )

    elif data in (CALLBACK_LUMBER_BUTTON1_WOOD, CALLBACK_LUMBER_BUTTON2_WOOD, CALLBACK_LUMBER_BUTTON3_WOOD, CALLBACK_LUMBER_BUTTON4_WOOD,
                  CALLBACK_LUMBER_BUTTON5_WOOD, CALLBACK_LUMBER_BUTTON6_WOOD, CALLBACK_LUMBER_BUTTON7_WOOD, CALLBACK_LUMBER_BUTTON8_WOOD,
                  CALLBACK_LUMBER_BUTTON9_WOOD, CALLBACK_LUMBER_BUTTON10_WOOD, CALLBACK_LUMBER_BUTTON11_WOOD, CALLBACK_LUMBER_BUTTON12_WOOD,
                  CALLBACK_LUMBER_BUTTON13_WOOD, CALLBACK_LUMBER_BUTTON14_WOOD, CALLBACK_LUMBER_BUTTON15_WOOD, CALLBACK_LUMBER_BUTTON16_WOOD,
                  CALLBACK_LUMBER_BUTTON17_WOOD, CALLBACK_LUMBER_BUTTON18_WOOD, CALLBACK_LUMBER_BUTTON19_WOOD, CALLBACK_LUMBER_BUTTON20_WOOD,):
        wood_type_lumber_tmp = {
            CALLBACK_LUMBER_BUTTON1_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON2_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON3_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON4_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON5_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON6_WOOD: 'Хвойные',
            CALLBACK_LUMBER_BUTTON7_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON8_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON9_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON10_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON11_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON12_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON13_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON14_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON15_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON16_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON17_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON18_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON19_WOOD: 'Лиственные',
            CALLBACK_LUMBER_BUTTON20_WOOD: 'Лиственные',
        }[data]
        wood_subtype_lumber_tmp = {
            CALLBACK_LUMBER_BUTTON1_WOOD: None,
            CALLBACK_LUMBER_BUTTON2_WOOD: 'сосна',
            CALLBACK_LUMBER_BUTTON3_WOOD: 'пихта',
            CALLBACK_LUMBER_BUTTON4_WOOD: 'ель',
            CALLBACK_LUMBER_BUTTON5_WOOD: 'кедр',
            CALLBACK_LUMBER_BUTTON6_WOOD: 'лиственница',
            CALLBACK_LUMBER_BUTTON7_WOOD: None,
            CALLBACK_LUMBER_BUTTON8_WOOD: 'берёза',
            CALLBACK_LUMBER_BUTTON9_WOOD: 'осина',
            CALLBACK_LUMBER_BUTTON10_WOOD: 'дуб',
            CALLBACK_LUMBER_BUTTON11_WOOD: 'бук',
            CALLBACK_LUMBER_BUTTON12_WOOD: 'липа',
            CALLBACK_LUMBER_BUTTON13_WOOD: 'клён',
            CALLBACK_LUMBER_BUTTON14_WOOD: 'каштан',
            CALLBACK_LUMBER_BUTTON15_WOOD: 'карагач',
            CALLBACK_LUMBER_BUTTON16_WOOD: 'ольха',
            CALLBACK_LUMBER_BUTTON17_WOOD: 'ясень',
            CALLBACK_LUMBER_BUTTON18_WOOD: 'бальса',
            CALLBACK_LUMBER_BUTTON19_WOOD: 'тополь',
            CALLBACK_LUMBER_BUTTON20_WOOD: 'ива',
        }[data]
        wood_type_lumber, _ = WoodTypes.objects.get_or_create(
            wood_type=wood_type_lumber_tmp
        )
        try:
            wood_subtype_lumber = WoodSubTypes.objects.get(
                wood_subtype=wood_subtype_lumber_tmp
            )
        except:
            wood_subtype_lumber = None

        lumber_wet_tmp = []
        lumber_wet_buttons = []
        keyboard_lumber_wet = []

        lumber_wet_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type,
                                    get_subtype=lm_subtype, get_wood_type=wood_type_lumber,
                                    get_wood_subtype=wood_subtype_lumber).select_related(
            'wet').order_by('wet').distinct().values('wet')
        for obj in lumber_wet_query:
            if obj.get('wet') is None:
                continue
            lum_wet = Wets.objects.get(
                wet_id=obj.get('wet')
            )
            lumber_wet_tmp.append(lum_wet)
        for item in lumber_wet_tmp:
            for key, value in LUMBER_TITLES.items():
                if str(value) == str(item):
                    lumber_wet_buttons.append(key)
        # while index < len(keyboard_pellets_tmp):
        for wet_button in lumber_wet_buttons:
            keyboard_lumber_wet.append([
                InlineKeyboardButton(LUMBER_TITLES[wet_button], callback_data=wet_button)
            ])
        keyboard_lumber_wet.append(
            [InlineKeyboardButton(LUMBER_TITLES[CALLBACK_LUMBER_BUTTON4_SKIP],
                                  callback_data=CALLBACK_LUMBER_BUTTON4_SKIP)])

        query.edit_message_text(
            text="Выберите влажность",
            reply_markup=InlineKeyboardMarkup(keyboard_lumber_wet)
        )

    elif data in (CALLBACK_LUMBER_BUTTON1_WET, CALLBACK_LUMBER_BUTTON2_WET):
        wet_lumber_tmp = {
            CALLBACK_LUMBER_BUTTON1_WET: 'Естественная',
            CALLBACK_LUMBER_BUTTON2_WET: 'Сухой лес',
        }[data]
        wet_lumber, _ = Wets.objects.get_or_create(
            wet=wet_lumber_tmp
        )
        text = 'Предложения на рынке:\n'
        try:
            rl_lumber = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type, get_subtype=lm_subtype,
                                 get_wood_type=wood_type_lumber, get_wood_subtype=wood_subtype_lumber, get_wet=wet_lumber)
            rl_lumber[0]
            for e in rl_lumber[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_lumber[6]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_lumber_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass

    elif data == CALLBACK_LUMBER_BUTTON4_SKIP:
        wet_lumber = None
        text = 'Предложения на рынке:\n'
        try:
            rl_lumber = get_rows(get_status=status, get_product=product, get_region=region, get_type=lm_type, get_subtype=lm_subtype,
                                 get_wood_type=wood_type_lumber, get_wood_subtype=wood_subtype_lumber, get_wet=wet_lumber)
            rl_lumber[0]
            for e in rl_lumber[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_lumber[6]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_lumber_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass
    elif data == CALLBACK_LUMBER_BUTTON1_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_lumber[5:10]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_lumber[11]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_lumber_keyboard5(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )

    elif data == CALLBACK_LUMBER_BUTTON2_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_lumber[10:15]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_lumber[16]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_lumber_keyboard6(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
    elif data == CALLBACK_LUMBER_BUTTON3_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_lumber[15:25]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        context.bot.send_message(
            chat_id=chat_id,
            text=f'\n{text}',
            reply_markup=get_back_to_reality(),
        )

    # --------------------------------------------------------------------------------------------------------------
    # Погонаж
    elif data == CALLBACK_PAGONAGE_BUTTON1_BACK:
        query.edit_message_text(
            text='Выберите регион',
            reply_markup=InlineKeyboardMarkup(keyboard_region),
        )
    elif data == CALLBACK_PAGONAGE_BUTTON2_BACK:
        query.edit_message_text(
            text="Выберите вид",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_type),
        )
    elif data == CALLBACK_PAGONAGE_BUTTON3_BACK:
        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_woodtype),
        )
    elif data == CALLBACK_PAGONAGE_BUTTON1_SKIP:
        pagonage_type = None
        pagonage_woodtype_tmp = []
        pagonage_woodsubtype_buttons = []
        keyboard_pagonage_woodtype = []

        pagonage_woodtype_query = get_rows(get_status=status, get_product=product, get_region=region,
                                           get_type=pagonage_type,
                                           ).select_related('wood_type').order_by(
            'wood_type').distinct().values('wood_type')
        for obj_woodtype in pagonage_woodtype_query:
            if obj_woodtype.get('wood_type') is None:
                continue
            pag_woodtype = WoodTypes.objects.get(
                wood_type_id=obj_woodtype.get('wood_type')
            )
            pagonage_woodtype_tmp.append(pag_woodtype)
        for pagonage_woodtype in pagonage_woodtype_tmp:
            pagonage_woodsubtype_query = get_rows(get_status=status, get_product=product, get_region=region,
                                                  get_type=pagonage_type).select_related(
                'wood_subtype').order_by('wood_subtype').distinct().values('wood_subtype')
            pagonage_woodsubtype_tmp = []
            pagonage_woodsubtype_tmp.append("все")
            for obj_woodsubtype in pagonage_woodsubtype_query:
                if obj_woodsubtype.get('wood_subtype') is None:
                    continue
                pag_woodsubtype = WoodSubTypes.objects.get(
                    wood_subtype_id=obj_woodsubtype.get('wood_subtype')
                )
                pagonage_woodsubtype_tmp.append(pag_woodsubtype)

            for item in pagonage_woodsubtype_tmp:
                for key, value in PAGONAGE_TITLES.items():
                    if re.search(f'{str(item)}$', value.lower()) and value.find(str(pagonage_woodtype)) != -1:
                        pagonage_woodsubtype_buttons.append(key)
        for pagonage_button in pagonage_woodsubtype_buttons:
            keyboard_pagonage_woodtype.append([
                InlineKeyboardButton(PAGONAGE_TITLES[pagonage_button], callback_data=pagonage_button)
            ])
        keyboard_pagonage_woodtype.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON2_BACK],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON2_BACK),
             ])
        keyboard_pagonage_woodtype.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON2_SKIP],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON2_SKIP)])
        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_woodtype),
        )
    elif data == CALLBACK_PAGONAGE_BUTTON2_SKIP:
        wood_type_pagonage = None
        wood_subtype_pagonage = None
        pagonage_wet_tmp = []
        pagonage_wet_buttons = []
        keyboard_pagonage_wet = []

        pagonage_wet_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=pagonage_type,
                                    get_wood_type=wood_type_pagonage, get_wood_subtype=wood_subtype_pagonage).select_related(
                                    'wet').order_by('wet').distinct().values('wet')
        for obj in pagonage_wet_query:
            if obj.get('wet') is None:
                continue
            pag_wet = Wets.objects.get(
                wet_id=obj.get('wet')
            )
            pagonage_wet_tmp.append(pag_wet)
        for item in pagonage_wet_tmp:
            for key, value in PAGONAGE_TITLES.items():
                if str(value) == str(item):
                    pagonage_wet_buttons.append(key)
        for wet_button in pagonage_wet_buttons:
            keyboard_pagonage_wet.append([
                InlineKeyboardButton(PAGONAGE_TITLES[wet_button], callback_data=wet_button)
            ])
        keyboard_pagonage_wet.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON3_SKIP],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON3_SKIP)])
        query.edit_message_text(
            text="Выберите влажность",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_wet),
        )
    elif data == CALLBACK_BUTTON2_PRODUCT:
        product, _ = Products.objects.get_or_create(
            product="Погонаж"
        )
        try:
            if sell_flag == True:
                status_tmp = "Покупка"
            if buy_flag == True:
                status_tmp = 'Продажа'
            status, _ = Statuses.objects.get_or_create(
                status=status_tmp
            )

            keyboard_region = []
            keyboard1_region = []
            keyboard2_region = []
            keyboard3_region = []
            keyboard4_region = []
            keyboard5_region = []
            keyboard_tmp = []
            regions_tmp = []
            index = 0
            regions_query = get_rows(get_status=status, get_product=product).select_related('region').order_by(
                'region').distinct().values('region')
            for obj in regions_query:
                reg = Regions.objects.get(
                    region_id=obj.get('region')
                )
                regions_tmp.append(str(reg))
            for item in sorted(regions_tmp):
                for key, value in REGION_TITLES.items():
                    if str(value) == str(item):
                        keyboard_tmp.append(key)
            while index < len(keyboard_tmp):
                if index < 22:
                    try:
                        keyboard_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 22 and index < 44:
                    try:
                        keyboard1_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard1_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 44 and index < 66:
                    try:
                        keyboard2_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard2_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 66 and index < 88:
                    try:
                        keyboard3_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard3_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 88 and index < 110:
                    try:
                        keyboard4_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard4_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 110:
                    try:
                        keyboard5_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard5_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                index += 2

            if index >= 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK], callback_data=CALLBACK_REGION_BUTTON_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON_MORE)
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP], callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index < 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK], callback_data=CALLBACK_REGION_BUTTON_BACK),
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP], callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON1_MORE)
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 22 and index < 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON2_MORE)
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 44 and index < 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON3_MORE)
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 66 and index < 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON4_MORE)
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 88 and index < 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON5_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON5_BACK)])
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            query.edit_message_text(
                text='Выберите регион',
                reply_markup=InlineKeyboardMarkup(keyboard_region),
            )
        except UnboundLocalError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )

    elif data in (CALLBACK_PAGONAGE_BUTTON1_TYPE, CALLBACK_PAGONAGE_BUTTON2_TYPE, CALLBACK_PAGONAGE_BUTTON3_TYPE,
                  CALLBACK_PAGONAGE_BUTTON4_TYPE, CALLBACK_PAGONAGE_BUTTON5_TYPE, CALLBACK_PAGONAGE_BUTTON6_TYPE,
                  CALLBACK_PAGONAGE_BUTTON7_TYPE, CALLBACK_PAGONAGE_BUTTON8_TYPE, CALLBACK_PAGONAGE_BUTTON9_TYPE,
                  CALLBACK_PAGONAGE_BUTTON10_TYPE, CALLBACK_PAGONAGE_BUTTON11_TYPE, CALLBACK_PAGONAGE_BUTTON12_TYPE,
                  CALLBACK_PAGONAGE_BUTTON13_TYPE, CALLBACK_PAGONAGE_BUTTON14_TYPE, CALLBACK_PAGONAGE_BUTTON15_TYPE,
                  CALLBACK_PAGONAGE_BUTTON16_TYPE, CALLBACK_PAGONAGE_BUTTON17_TYPE,):
        text = 'Предложения на рынке:\n'
        pagonage_type_tmp = {
            CALLBACK_PAGONAGE_BUTTON1_TYPE: 'Вагонка',
            CALLBACK_PAGONAGE_BUTTON2_TYPE: 'Плинтус',
            CALLBACK_PAGONAGE_BUTTON3_TYPE: 'Полок',
            CALLBACK_PAGONAGE_BUTTON4_TYPE: 'Половая доска',
            CALLBACK_PAGONAGE_BUTTON5_TYPE: 'Террасная доска',
            CALLBACK_PAGONAGE_BUTTON6_TYPE: 'Террасная доска из ДПК (Декинг)',
            CALLBACK_PAGONAGE_BUTTON7_TYPE: 'Палубная доска',
            CALLBACK_PAGONAGE_BUTTON8_TYPE: 'Рейка',
            CALLBACK_PAGONAGE_BUTTON9_TYPE: 'Имитация бруса',
            CALLBACK_PAGONAGE_BUTTON10_TYPE: 'Блок-хаус',
            CALLBACK_PAGONAGE_BUTTON11_TYPE: 'Планкен',
            CALLBACK_PAGONAGE_BUTTON12_TYPE: 'Наличник',
            CALLBACK_PAGONAGE_BUTTON13_TYPE: 'Брусок строганный',
            CALLBACK_PAGONAGE_BUTTON14_TYPE: 'Брусок сращенный строганный',
            CALLBACK_PAGONAGE_BUTTON15_TYPE: 'Деревянные обои',
            CALLBACK_PAGONAGE_BUTTON16_TYPE: 'Деревянная мозаика',
            CALLBACK_PAGONAGE_BUTTON17_TYPE: 'Лунный паз',
        }[data]
        pagonage_type, _ = Types.objects.get_or_create(
            type=pagonage_type_tmp
        )

        pagonage_woodtype_tmp = []
        pagonage_woodsubtype_buttons = []
        keyboard_pagonage_woodtype = []

        pagonage_woodtype_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=pagonage_type,
                                        ).select_related('wood_type').order_by(
                                        'wood_type').distinct().values('wood_type')
        for obj_woodtype in pagonage_woodtype_query:
            if obj_woodtype.get('wood_type') is None:
                continue
            pag_woodtype = WoodTypes.objects.get(
                wood_type_id=obj_woodtype.get('wood_type')
            )
            pagonage_woodtype_tmp.append(pag_woodtype)
        for pagonage_woodtype in pagonage_woodtype_tmp:
            pagonage_woodsubtype_query = get_rows(get_status=status, get_product=product, get_region=region,
                                                get_type=pagonage_type).select_related(
                'wood_subtype').order_by('wood_subtype').distinct().values('wood_subtype')
            pagonage_woodsubtype_tmp = []
            pagonage_woodsubtype_tmp.append("все")
            for obj_woodsubtype in pagonage_woodsubtype_query:
                if obj_woodsubtype.get('wood_subtype') is None:
                    continue
                pag_woodsubtype = WoodSubTypes.objects.get(
                    wood_subtype_id=obj_woodsubtype.get('wood_subtype')
                )
                pagonage_woodsubtype_tmp.append(pag_woodsubtype)

            for item in pagonage_woodsubtype_tmp:
                for key, value in PAGONAGE_TITLES.items():
                    if re.search(f'{str(item)}$', value.lower()) and value.find(str(pagonage_woodtype)) != -1:
                        pagonage_woodsubtype_buttons.append(key)
        for pagonage_button in pagonage_woodsubtype_buttons:
            keyboard_pagonage_woodtype.append([
                InlineKeyboardButton(PAGONAGE_TITLES[pagonage_button], callback_data=pagonage_button)
            ])
        keyboard_pagonage_woodtype.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON2_BACK],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON2_BACK),
             ])
        keyboard_pagonage_woodtype.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON2_SKIP],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON2_SKIP)])

        query.edit_message_text(
            text="Выберите породу древесины",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_woodtype),
        )

    elif data in (CALLBACK_PAGONAGE_BUTTON1_WOOD, CALLBACK_PAGONAGE_BUTTON2_WOOD, CALLBACK_PAGONAGE_BUTTON3_WOOD,
                  CALLBACK_PAGONAGE_BUTTON4_WOOD, CALLBACK_PAGONAGE_BUTTON5_WOOD, CALLBACK_PAGONAGE_BUTTON6_WOOD,
                  CALLBACK_PAGONAGE_BUTTON7_WOOD, CALLBACK_PAGONAGE_BUTTON8_WOOD, CALLBACK_PAGONAGE_BUTTON9_WOOD,
                  CALLBACK_PAGONAGE_BUTTON10_WOOD, CALLBACK_PAGONAGE_BUTTON11_WOOD, CALLBACK_PAGONAGE_BUTTON12_WOOD):
        wood_type_pagonage_tmp = {
            CALLBACK_PAGONAGE_BUTTON1_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON2_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON3_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON4_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON5_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON6_WOOD: 'Лиственные',
            CALLBACK_PAGONAGE_BUTTON7_WOOD: 'Хвойные',
            CALLBACK_PAGONAGE_BUTTON8_WOOD: 'Хвойные',
            CALLBACK_PAGONAGE_BUTTON9_WOOD: 'Хвойные',
            CALLBACK_PAGONAGE_BUTTON10_WOOD: 'Хвойные',
            CALLBACK_PAGONAGE_BUTTON11_WOOD: 'Хвойные',
            CALLBACK_PAGONAGE_BUTTON12_WOOD: 'Хвойные',
        }[data]
        wood_subtype_pagonage_tmp = {
            CALLBACK_PAGONAGE_BUTTON1_WOOD: None,
            CALLBACK_PAGONAGE_BUTTON2_WOOD: 'берёза',
            CALLBACK_PAGONAGE_BUTTON3_WOOD: 'осина',
            CALLBACK_PAGONAGE_BUTTON4_WOOD: 'дуб',
            CALLBACK_PAGONAGE_BUTTON5_WOOD: 'липа',
            CALLBACK_PAGONAGE_BUTTON6_WOOD: 'ясень',
            CALLBACK_PAGONAGE_BUTTON7_WOOD: None,
            CALLBACK_PAGONAGE_BUTTON8_WOOD: 'сосна',
            CALLBACK_PAGONAGE_BUTTON9_WOOD: 'пихта',
            CALLBACK_PAGONAGE_BUTTON10_WOOD: 'ель',
            CALLBACK_PAGONAGE_BUTTON11_WOOD: 'кедр',
            CALLBACK_PAGONAGE_BUTTON12_WOOD: 'лиственница',
        }[data]
        wood_type_pagonage, _ = WoodTypes.objects.get_or_create(
            wood_type=wood_type_pagonage_tmp
        )
        try:
            wood_subtype_pagonage, _ = WoodSubTypes.objects.get_or_create(
                wood_subtype=wood_subtype_pagonage_tmp
            )
        except:
            wood_subtype_pagonage = None

        pagonage_wet_tmp = []
        pagonage_wet_buttons = []
        keyboard_pagonage_wet = []

        pagonage_wet_query = get_rows(get_status=status, get_product=product, get_region=region, get_type=pagonage_type,
                                    get_wood_type=wood_type_pagonage, get_wood_subtype=wood_subtype_pagonage).select_related(
                                    'wet').order_by('wet').distinct().values('wet')
        for obj in pagonage_wet_query:
            if obj.get('wet') is None:
                continue
            pag_wet = Wets.objects.get(
                wet_id=obj.get('wet')
            )
            pagonage_wet_tmp.append(pag_wet)
        for item in pagonage_wet_tmp:
            for key, value in PAGONAGE_TITLES.items():
                if str(value) == str(item):
                    pagonage_wet_buttons.append(key)
        for wet_button in pagonage_wet_buttons:
            keyboard_pagonage_wet.append([
                InlineKeyboardButton(PAGONAGE_TITLES[wet_button], callback_data=wet_button)
            ])
        keyboard_pagonage_wet.append(
            [InlineKeyboardButton(PAGONAGE_TITLES[CALLBACK_PAGONAGE_BUTTON3_SKIP],
                                  callback_data=CALLBACK_PAGONAGE_BUTTON3_SKIP)])

        query.edit_message_text(
            text="Выберите влажность",
            reply_markup=InlineKeyboardMarkup(keyboard_pagonage_wet),
        )

    elif data in (CALLBACK_PAGONAGE_BUTTON1_WET, CALLBACK_PAGONAGE_BUTTON2_WET, CALLBACK_PAGONAGE_BUTTON3_WET):
        wet_pagonage_tmp = {
            CALLBACK_PAGONAGE_BUTTON1_WET: 'Естественная',
            CALLBACK_PAGONAGE_BUTTON2_WET: 'Сухой лес',
            CALLBACK_PAGONAGE_BUTTON3_WET: 'Термо модифицированная древесина',
        }[data]
        wet_pagonage, _ = Wets.objects.get_or_create(
            wet=wet_pagonage_tmp
        )
        text = 'Предложения на рынке:\n'
        try:
            rl_pagonage = get_rows(get_status=status, get_product=product, get_region=region, get_type=pagonage_type,
                                   get_wood_type=wood_type_pagonage, get_wood_subtype=wood_subtype_pagonage, get_wet=wet_pagonage)
            rl_pagonage[0]
            for e in rl_pagonage[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_pagonage[6]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_pagonage_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass

    elif data == CALLBACK_PAGONAGE_BUTTON3_SKIP:
        wet_pagonage = None
        text = 'Предложения на рынке:\n'
        try:
            rl_pagonage = get_rows(get_status=status, get_product=product, get_region=region, get_type=pagonage_type,
                                   get_wood_type=wood_type_pagonage, get_wood_subtype=wood_subtype_pagonage,
                                   get_wet=wet_pagonage)
            rl_pagonage[0]
            for e in rl_pagonage[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_pagonage[6]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_pagonage_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass
    elif data == CALLBACK_PAGONAGE_BUTTON1_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pagonage[5:10]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_pagonage[11]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_pagonage_keyboard5(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )

    elif data == CALLBACK_PAGONAGE_BUTTON2_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pagonage[10:15]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_pagonage[16]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_pagonage_keyboard6(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
    elif data == CALLBACK_PAGONAGE_BUTTON3_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pagonage[15:25]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        context.bot.send_message(
            chat_id=chat_id,
            text=f'\n{text}',
            reply_markup=get_back_to_reality(),
        )

    # -----------------------------------------------------------------------------------------------------------------
    # Пеллеты
    elif data == CALLBACK_PELLETS_BUTTON1_BACK:
        query.edit_message_text(
            text='Выберите регион',
            reply_markup=InlineKeyboardMarkup(keyboard_region),
        )
    elif data == CALLBACK_BUTTON3_PRODUCT:
        product, _ = Products.objects.get_or_create(
            product="Пеллеты"
        )
        try:
            if sell_flag == True:
                status_tmp = "Покупка"
            if buy_flag == True:
                status_tmp = 'Продажа'
            status, _ = Statuses.objects.get_or_create(
                status=status_tmp
            )
            keyboard_region = []
            keyboard1_region = []
            keyboard2_region = []
            keyboard3_region = []
            keyboard4_region = []
            keyboard5_region = []
            keyboard_tmp = []
            regions_tmp = []
            index = 0
            regions_query = Actual.objects.filter(status=status, product=product).select_related('region').order_by(
                'region').distinct().values('region')
            for obj in regions_query:
                reg = Regions.objects.get(
                    region_id=obj.get('region')
                )
                regions_tmp.append(str(reg))
            for item in sorted(regions_tmp):
                for key, value in REGION_TITLES.items():
                    if str(value) == str(item):
                        keyboard_tmp.append(key)
            while index < len(keyboard_tmp):
                if index < 22:
                    try:
                        keyboard_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 22 and index < 44:
                    try:
                        keyboard1_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard1_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 44 and index < 66:
                    try:
                        keyboard2_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard2_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 66 and index < 88:
                    try:
                        keyboard3_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard3_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 88 and index < 110:
                    try:
                        keyboard4_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard4_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                if index >= 110:
                    try:
                        keyboard5_region.append([
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]], callback_data=keyboard_tmp[index]),
                            InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index + 1]],
                                                 callback_data=keyboard_tmp[index + 1])
                        ])
                    except:
                        keyboard5_region.append(
                            [InlineKeyboardButton(REGION_TITLES[keyboard_tmp[index]],
                                                  callback_data=keyboard_tmp[index])])
                index += 2

            if index >= 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON_MORE)
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index < 22:
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON_BACK),
                     ])
                keyboard_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON1_MORE)
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 22 and index < 44:
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON1_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON1_BACK),
                     ])
                keyboard1_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON2_MORE)
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 44 and index < 66:
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON2_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON2_BACK),
                     ])
                keyboard2_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON3_MORE)
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 66 and index < 88:
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON3_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON3_BACK),
                     ])
                keyboard3_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_MORE],
                                          callback_data=CALLBACK_REGION_BUTTON4_MORE)
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            elif index > 88 and index < 110:
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON4_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON4_BACK),
                     ])
                keyboard4_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            if index >= 110:
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON5_BACK],
                                          callback_data=CALLBACK_REGION_BUTTON5_BACK)])
                keyboard5_region.append(
                    [InlineKeyboardButton(TITLES[CALLBACK_REGION_BUTTON_SKIP],
                                          callback_data=CALLBACK_REGION_BUTTON_SKIP)])
            query.edit_message_text(
                text="Выберите регион",
                reply_markup=InlineKeyboardMarkup(keyboard_region),
            )
        except UnboundLocalError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
    elif data in (CALLBACK_PELLETS_BUTTON1_TYPE, CALLBACK_PELLETS_BUTTON2_TYPE, CALLBACK_PELLETS_BUTTON3_TYPE, CALLBACK_PELLETS_BUTTON4_TYPE,
                  CALLBACK_PELLETS_BUTTON5_TYPE, CALLBACK_PELLETS_BUTTON6_TYPE):
        text = 'Предложения на рынке:\n'
        pellets_type_tmp = {
            CALLBACK_PELLETS_BUTTON1_TYPE: 'Пеллеты',
            CALLBACK_PELLETS_BUTTON2_TYPE: 'Брикеты',
            CALLBACK_PELLETS_BUTTON3_TYPE: 'Щепа',
            CALLBACK_PELLETS_BUTTON4_TYPE: 'Опилки',
            CALLBACK_PELLETS_BUTTON5_TYPE: 'Деревянная стружка',
            CALLBACK_PELLETS_BUTTON6_TYPE: 'Древесная мука',
        }[data]
        pellets_type, _ = Types.objects.get_or_create(
            type=pellets_type_tmp
        )
        try:
            rl_pellets = get_rows(get_status=status, get_product=product, get_region=region, get_type=pellets_type)
            rl_pellets[0]
            for e in rl_pellets[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_pellets[5]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_pellets_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass
    elif data == CALLBACK_PELLETS_BUTTON1_SKIP:
        text = 'Предложения на рынке:\n'
        pellets_type = None
        try:
            rl_pellets = get_rows(get_status=status, get_product=product, get_region=region, get_type=pellets_type)
            rl_pellets[0]
            for e in rl_pellets[0:5]:
                text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        except NameError:
            query.edit_message_text(
                text="Сначала, пожалуйста, выберите команду для поиска \n /buy или /sell",
            )
        except IndexError:
            text = "Объявления не найдены"
        try:
            rl_pellets[5]
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_pellets_keyboard4(),
            )
        except IndexError:
            query.edit_message_text(
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
        except NameError:
            pass
    elif data == CALLBACK_PELLETS_BUTTON1_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pellets[5:10]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_pellets[10]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_pellets_keyboard5(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )

    elif data == CALLBACK_PELLETS_BUTTON2_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pellets[10:15]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        try:
            rl_pellets[15]
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_pellets_keyboard6(),
            )
        except IndexError:
            context.bot.send_message(
                chat_id=chat_id,
                text=f'\n{text}',
                reply_markup=get_back_to_reality(),
            )
    elif data == CALLBACK_PELLETS_BUTTON3_MORE:
        text = 'Предложения на рынке:\n'
        for e in rl_pellets[15:25]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        context.bot.send_message(
            chat_id=chat_id,
            text=f'\n{text}',
            reply_markup=get_back_to_reality(),
        )

def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=f'Пожалуйста выберите команду для поиска\n'
             '/buy или /sell\nТакже список команд есть в меню'
    )

def do_buy(update: Update, context: CallbackContext):
    global sell_flag, buy_flag
    sell_flag = False
    buy_flag = True
    update.message.reply_text(
        text=f'Выберите тип продукции',
        reply_markup=get_product_keybord(),
    )

def do_sell(update: Update, context: CallbackContext):
    global sell_flag, buy_flag
    sell_flag = True
    buy_flag = False
    update.message.reply_text(
        text=f'Выберите тип продукции',
        reply_markup=get_product_keybord(),
    )

def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    m = Message(
        profile=p,
        text=text,
    )
    m.save()

    if text == "buy":
        status, _ = Statuses.objects.get_or_create(
            status="Продажа"
        )
        product, _ = Products.objects.get_or_create(
            product="Пиломатериалы"
        )
        rl_pellets = get_rows(get_status=status, get_product=product)
        rl_pellets[0]
        for e in rl_pellets[0:20]:
            text = text + '\n'.join([f'{e.title}:\n{e.post_url}\n\n'])
        context.bot.send_message(
            chat_id=chat_id,
            text=f"\n{text}",
        )

dispatcher.add_handler(CommandHandler("buy", do_buy))
dispatcher.add_handler(CommandHandler("sell", do_sell))
dispatcher.add_handler(CommandHandler("start", do_start))
message_handler = MessageHandler(Filters.text, do_echo)
buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(buttons_handler)


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        logger.info(str(request.body))
        try:
            update = Update.de_json(json.loads(request.body), bot)
            dispatcher.process_update(update)
        except Exception:
            logger.exception('error')
        return HttpResponse('ok')
