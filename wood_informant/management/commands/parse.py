import requests
import re
import sys
import time
import logging
import locale

from random import choice
from datetime import datetime
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from wood_informant.models import (
    Statuses,
    Products,
    Cities,
    Regions,
    Countries,
    Types,
    WoodTypes,
    Wets,
    Actual,
    Previous,
    SubTypes,
    WoodSubTypes,
)


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            file_content1 = "<{}>  <{}> <{}> <{}>  <{}>\n".format(
                f.__name__, type(e).__name__, kwargs, Exception, e
            )
            with open("parser_errors.log", "a", encoding="utf8") as file:
                file.write(file_content1)
            raise e

    return inner


class WoodParser(object):
    def __init__(self):
        self.session = requests.Session()
        # Список с заголовками для http-запроса
        desktop_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
        ]
        # Вызов рандомого заголовка для http-запроса
        self.session.headers = {
            "User-Agent": choice(desktop_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    def get_page(self, parametr, url):
        """Возвращает html-код страницы с постами по пиломатериалам"""
        url += str(parametr)
        try:
            page = self.session.get(url, timeout=7)
        except requests.ConnectionError as e:
            print(
                "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n"
            )
            logging.error(e)
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            logging.error(e)
        except requests.RequestException as e:
            print("OOPS!! General Error")
            logging.error(e)
        except KeyboardInterrupt:
            print("Someone closed the program")
        return page.text

    def get_post_page(self, post_url):
        """Возвращает html-код страницы с указанного URL"""
        try:
            post_page = self.session.get(post_url, timeout=10)
        except requests.ConnectionError as e:
            print(
                "OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n"
            )
            logging.error(e)
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            logging.error(e)
        except requests.RequestException as e:
            print("OOPS!! General Error")
            logging.error(e)
        except KeyboardInterrupt:
            print("Someone closed the program")
        try:
            return post_page.text
        except Exception as e:
            logging.error(e)
            post_page = ""
            return post_page

    @log_errors
    def parse_urls(self, product_status):
        """Собирает URL'ы с объявлениями со страницы"""
        url_list = []
        if product_status == "LumberSell":
            url = "https://woodresource.ru/browse/sell/lumber/?page="
        if product_status == "LumberBuy":
            url = "https://woodresource.ru/browse/buy/lumber/?page="
        if product_status == "PagonageSell":
            url = "https://woodresource.ru/browse/sell/pogonazhnyie-izdeliya/?page="
        if product_status == "PagonageBuy":
            url = "https://woodresource.ru/browse/buy/pogonazhnyie-izdeliya/?page="
        if product_status == "PelletsSell":
            url = "https://woodresource.ru/browse/sell/pelletyi-briketyi/?page="
        if product_status == "PelletsBuy":
            url = "https://woodresource.ru/browse/buy/pelletyi-briketyi/?page="
        try:
            count_text = self.get_page(parametr=1, url=url)
        except:
            count_text = self.get_page(parametr=1, url=url)
        count_soup = BeautifulSoup(count_text, "html.parser")
        page_count = (
            count_soup.find("div", class_="pagination").findAll("a")[-5].text.strip()
        )
        # for p in range(1, 3):
        # print("Кол-во страниц:", page_count)
        for p in range(1, int(page_count) + 1):
            a_link = []
            try:
                page_text = self.get_page(p, url)
            except:
                continue
            soup = BeautifulSoup(page_text, "html.parser")
            a_link = soup.find("tbody").findAll("a")
            for item in a_link:
                if item.get("href").find("show") != -1:
                    url_list.append(
                        "https://woodresource.ru" + item.get("href")
                    )  # В url_list храним список ссылок
        return url_list

    @log_errors
    def parse_post(self):
        locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")  # the ru locale is installed
        start_time = time.time()
        product_statuses = [
            "PagonageSell",
            "PagonageBuy",
            "PelletsSell",
            "PelletsBuy",
            "LumberSell",
            "LumberBuy",
        ]
        # product_statuses = ["PelletsSell", "PelletsBuy", "PagonageSell", "PagonageBuy"]
        for pr_status in product_statuses:
            url_list = self.parse_urls(product_status=pr_status)
            count_requests = 0
            if pr_status.find("Sell") != -1:
                status_tmp = "Покупка"
            else:
                status_tmp = "Продажа"
            if pr_status.find("Lumber") != -1:
                product_tmp = "Пиломатериалы"
            if pr_status.find("Pagonage") != -1:
                product_tmp = "Погонаж"
            if pr_status.find("Pellets") != -1:
                product_tmp = "Пеллеты"

            for url in url_list:
                all_text = ""
                all_discription = ""
                publish_date = ""
                city_tmp = None
                post_id = price = 0
                status = (
                    product
                ) = title = region = country = discription = post_url = ""
                subtype = (
                    type_lm
                ) = (
                    wood_type
                ) = (
                    wet
                ) = (
                    length
                ) = (
                    width
                ) = thickness = post_date = post_views = city = wood_subtype = None
                additional_regions = False
                title_old = (
                    city_old
                ) = (
                    region_old
                ) = (
                    country_old
                ) = price_old = type_old = wood_type_old = wet_old = length_old = None
                width_old = (
                    thickness_old
                ) = (
                    discription_old
                ) = (
                    post_views_old
                ) = post_url_old = subtype_old = wood_subtype_old = None
                if divmod(count_requests, 20)[1] == 0 and count_requests != 0:
                    time.sleep(7)
                count_requests += 1
                post_page_text = self.get_post_page(url)
                if post_page_text == "":
                    continue
                soup = BeautifulSoup(post_page_text, "html.parser")
                all_attr = soup.find(
                    "div", class_="", id="content-after-sidebar"
                ).findAll("p")
                small_attr = soup.find(
                    "div", class_="", id="content-after-sidebar"
                ).findAll("small")

                for item in small_attr:
                    publish_date += item.get_text()
                datetime_publish = publish_date[: publish_date.find("г.")].strip()
                datetime_publish_obj = datetime.strptime(
                    "2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
                )
                try:
                    datetime_publish_obj = datetime.strptime(
                        datetime_publish, "%d %B %Y"
                    )
                except Exception as e:
                    print(e)
                start_date = (datetime.strptime("2022-02-24", "%Y-%m-%d")).date()
                post_date = datetime_publish_obj.date()
                # if post_date < datetime.today().date() - relativedelta(months=12):
                if post_date < start_date:
                    continue
                for item in all_attr:
                    all_text += item.get_text().strip() + "\n"
                    discription_list = item.findAll("br")
                    for x in discription_list:
                        if x.get_text() != "":
                            all_discription += str(x)
                            break
                filtered_text = re.sub(r"\s+", " ", all_text)
                filtered_text = filtered_text.replace("РоссияЗакрыть", "").replace(
                    "УкраинаЗакрыть", ""
                )

                parse_id = (
                    soup.find("div", class_="breadcrumb active")
                    .find("span")
                    .text.strip()
                )
                post_id = int(parse_id[12:])
                status, _ = Statuses.objects.get_or_create(status=status_tmp)
                product, _ = Products.objects.get_or_create(product=product_tmp)
                title = (
                    soup.find("div", class_="", id="content-after-sidebar")
                    .find("h1")
                    .text.strip()
                )

                if filtered_text.find("Город:") != -1:
                    filtered_text = filtered_text[filtered_text.find("Город:") + 7 :]
                else:
                    filtered_text = filtered_text[filtered_text.find("Регион:") + 8 :]

                city_text = filtered_text[: filtered_text.find("Название")]
                if city_text.find("(") != -1 and city_text.count(",") == 2:
                    additional_regions = True
                    city_text = city_text[: city_text.find(".")]
                    country_tmp = city_text[city_text.rfind(",") + 1 :].strip()
                    region_tmp = city_text[
                        city_text.find(",") + 1 : city_text.rfind(",")
                    ].strip()
                    city_tmp = city_text[: city_text.find(",")].strip()
                elif city_text.find("(") == -1 and city_text.count(",") == 2:
                    country_tmp = city_text[city_text.rfind(",") + 1 :].strip()
                    region_tmp = city_text[
                        city_text.find(",") + 1 : city_text.rfind(",")
                    ].strip()
                    city_tmp = city_text[: city_text.find(",")].strip()
                elif city_text.find("(") != -1 and city_text.count(",") == 1:
                    additional_regions = True
                    city_text = city_text[: city_text.find(".")]
                    country_tmp = city_text[city_text.rfind(",") + 1 :].strip()
                    region_tmp = city_text[: city_text.find(",")].strip()
                elif city_text.find("(") == -1 and city_text.count(",") == 1:
                    country_tmp = city_text[city_text.rfind(",") + 1 :].strip()
                    region_tmp = city_text[: city_text.find(",")].strip()
                try:
                    country, _ = Countries.objects.get_or_create(country=country_tmp)
                except:
                    country = None
                try:
                    region, _ = Regions.objects.get_or_create(region=region_tmp)
                except:
                    region = None
                try:
                    if city_tmp != None:
                        city, _ = Cities.objects.get_or_create(city=city_tmp)
                except:
                    city = None

                post_cost_str = filtered_text[
                    filtered_text.find("Цена") : filtered_text.find("Описание:")
                ]
                try:
                    price = float(
                        post_cost_str[
                            post_cost_str.find(":") + 1 : post_cost_str.find("₽")
                        ].strip()
                    )
                except Exception as e_rub:
                    price = 0.0
                    logging.error(e_rub)
                if product_tmp == "Пиломатериалы":
                    type_str_tmp = filtered_text[
                        filtered_text.find("Тип:")
                        + 4 : filtered_text.find("Порода древесины:")
                    ].strip()
                    type_tmp = type_str_tmp[: type_str_tmp.find(":")].strip()
                    subtype_tmp = type_str_tmp[type_str_tmp.find(":") + 1 :].strip()
                    try:
                        type_lm, _ = Types.objects.get_or_create(type=type_tmp)
                    except:
                        type_lm = None
                    try:
                        subtype, _ = SubTypes.objects.get_or_create(subtype=subtype_tmp)
                    except:
                        subtype = None
                if product_tmp == "Погонаж":
                    type_tmp = filtered_text[
                        filtered_text.find("Вид:")
                        + 4 : filtered_text.find("Порода древесины:")
                    ].strip()
                    try:
                        type_lm, _ = Types.objects.get_or_create(type=type_tmp)
                    except:
                        type_lm = None
                if product_tmp == "Пеллеты":
                    type_tmp = filtered_text[
                        filtered_text.find("Тип:") + 4 : filtered_text.find("Цена")
                    ].strip()
                    try:
                        type_lm, _ = Types.objects.get_or_create(type=type_tmp)
                    except:
                        type_lm = None
                if product_tmp != "Пеллеты":
                    wood_type_str_tmp = filtered_text[
                        filtered_text.find("Порода древесины:")
                        + 17 : filtered_text.find("Влажность:")
                    ].strip()
                    wood_type_tmp = wood_type_str_tmp[
                        : wood_type_str_tmp.find(":")
                    ].strip()
                    wood_subtype_tmp = wood_type_str_tmp[
                        wood_type_str_tmp.find(":") + 1 :
                    ].strip()
                    try:
                        wood_type, _ = WoodTypes.objects.get_or_create(
                            wood_type=wood_type_tmp
                        )
                    except:
                        wood_type = None
                    try:
                        wood_subtype, _ = WoodSubTypes.objects.get_or_create(
                            wood_subtype=wood_subtype_tmp
                        )
                    except:
                        wood_subtype = None
                if product_tmp == "Пиломатериалы":
                    wet_tmp = filtered_text[
                        filtered_text.find("Влажность:")
                        + 10 : filtered_text.find("Длина в мм:")
                    ].strip()
                    try:
                        wet, _ = Wets.objects.get_or_create(wet=wet_tmp)
                    except:
                        wet = None
                if product_tmp == "Погонаж":
                    wet_tmp = filtered_text[
                        filtered_text.find("Влажность:")
                        + 10 : filtered_text.find("Цена")
                    ].strip()
                    try:
                        wet, _ = Wets.objects.get_or_create(wet=wet_tmp)
                    except:
                        wet = None
                if product_tmp == "Пиломатериалы":
                    length = filtered_text[
                        filtered_text.find("Длина в мм:")
                        + 11 : filtered_text.find("Ширина в мм:")
                    ].strip()
                    width = filtered_text[
                        filtered_text.find("Ширина в мм:")
                        + 12 : filtered_text.find("Толщина в мм:")
                    ].strip()
                    if (
                        filtered_text[filtered_text.find("Толщина в мм:") :].find(
                            "Наличие:"
                        )
                        != -1
                    ):
                        thickness = filtered_text[
                            filtered_text.find("Толщина в мм:")
                            + 13 : filtered_text.find("Наличие:")
                        ].strip()
                        post_have = filtered_text[
                            filtered_text.find("Наличие:")
                            + 8 : filtered_text.find("Цена")
                        ].strip()
                    else:
                        post_have = " "
                        thickness = filtered_text[
                            filtered_text.find("Толщина в мм:")
                            + 13 : filtered_text.find("Цена")
                        ].strip()
                all_discription = (
                    all_discription.replace("<br>", " ")
                    .replace("</br>", " ")
                    .replace("<br/>", " ")
                )
                discription = re.sub(r"\s+", " ", all_discription).strip()
                parse_date = datetime.now().date()
                post_views = int(publish_date[publish_date.find("Просмотров:") + 11 :])
                post_url = url
                # post_discription = filtered_text[filtered_text.find("Описание"):filtered_text.find("Контактные")]
                if length is not None and len(length) > 20:
                    length = None
                if width is not None and len(width) > 20:
                    width = None
                if thickness is not None and len(thickness) > 20:
                    thickness = None

                try:
                    lm = Actual.objects.get(post_id=post_id)

                    if lm.post_date != post_date:
                        if lm.title != title:
                            title_old = lm.title
                        if lm.city != city:
                            city_old = lm.city
                        if lm.region != region:
                            region_old = lm.region
                        if lm.country != country:
                            country_old = lm.country
                        if lm.price != price:
                            price_old = lm.price
                        if lm.type != type_lm:
                            type_old = lm.type
                        if lm.subtype != subtype:
                            subtype_old = lm.subtype
                        if lm.wood_type != wood_type:
                            wood_type_old = lm.wood_type
                        if lm.wood_subtype != wood_subtype:
                            wood_subtype_old = lm.wood_subtype
                        if lm.wet != wet:
                            wet_old = lm.wet
                        if lm.length != length:
                            length_old = lm.length
                        if lm.width != width:
                            width_old = lm.width
                        if lm.thickness != thickness:
                            thickness_old = lm.thickness
                        if lm.discription != discription:
                            discription_old = lm.discription
                        if lm.post_views != post_views:
                            post_views_old = lm.post_views
                        if lm.post_url != post_url:
                            post_url_old = lm.post_url

                        lm_old = Previous(
                            post_id=lm.post_id,
                            status=status,
                            product=product,
                            title=title_old,
                            city=city_old,
                            region=region_old,
                            country=country_old,
                            price=price_old,
                            type=type_old,
                            subtype=subtype,
                            wood_type=wood_type_old,
                            wood_subtype=wood_subtype,
                            wet=wet_old,
                            length=length_old,
                            width=width_old,
                            thickness=thickness_old,
                            discription=discription_old,
                            post_date=lm.post_date,
                            parse_date=lm.parse_date,
                            post_views=post_views_old,
                            post_url=post_url_old,
                            additional_regions=lm.additional_regions,
                        ).save()

                        lm.post_id = post_id
                        lm.status = status
                        lm.product = product
                        lm.title = title
                        lm.city = city
                        lm.region = region
                        lm.country = country
                        lm.price = price
                        lm.type = type_lm
                        lm.subtype = subtype
                        lm.wood_type = wood_type
                        lm.wood_subtype = wood_subtype
                        lm.wet = wet
                        lm.length = length
                        lm.width = width
                        lm.thickness = thickness
                        lm.discription = discription
                        lm.post_date = post_date
                        lm.parse_date = parse_date
                        lm.post_views = post_views
                        lm.post_url = post_url
                        lm.additional_regions = additional_regions
                        lm.save()
                except Actual.DoesNotExist:
                    lm = Actual(
                        post_id=post_id,
                        status=status,
                        product=product,
                        title=title,
                        city=city,
                        region=region,
                        country=country,
                        price=price,
                        type=type_lm,
                        subtype=subtype,
                        wood_type=wood_type,
                        wood_subtype=wood_subtype,
                        wet=wet,
                        length=length,
                        width=width,
                        thickness=thickness,
                        discription=discription,
                        post_date=post_date,
                        parse_date=parse_date,
                        post_views=post_views,
                        post_url=post_url,
                        additional_regions=additional_regions,
                    ).save()
                except Exception as e:
                    logging.error(e, "\n post_id", post_id)

                print("--- %s seconds ---" % (time.time() - start_time))

    # 123


class Command(BaseCommand):
    help = "Парсинг Пиломатериалов"

    def handle(self, *args, **options):
        wood_parse = WoodParser()
        wood_parse.parse_post()
