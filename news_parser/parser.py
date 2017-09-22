from __future__ import print_function
from __future__ import unicode_literals

import json
import os

import requests
from lxml import html

from configs.main_configs import LOGGER, BASE_DIR


class News(object):
    """
    Class that represent news object.
    Must contain title, text, date. Additionally can contain and images.
    """
    WEBSITE_URL = "https://www.reuters.com"

    def __init__(self, title, text, date, images):
        self.title = title
        self.text = text
        self.date = date
        self.images = list(images)

    def __eq__(self, o):
        if not isinstance(o, self.__class__):
            return False
        if self.title != o.title:
            return False
        if self.text != o.text:
            return False
        if self.date != o.date:
            return False
        return self.images == o.images

    def __str__(self):
        return "title : {}, text : {}, date = {}, images : {}" \
            .format(self.title, self.text, self.date, self.images).encode('utf-8')

    @staticmethod
    def parse_reuters_com_website(amount=1000):
        """
        Parse news from reuters.com website.
        Return given amount of News. Starting from oldest to latest.
        :param amount amount of news to be scraped, default is 1000.
        :return: array of News objects.
        """
        all_news_url = News.WEBSITE_URL + "/news/archive/worldNews"
        params = {
            "view": "page",
            "page": "1",
            "pageSize": "10"

        }
        newses = []
        current_page = 1
        while len(newses) < amount:
            params["page"] = current_page
            r = requests.get(all_news_url, params)
            if r.status_code != 200:
                LOGGER.ERROR("Response code of url: {} with parameters {} was {}. Stoping."
                             .format(all_news_url, params, r.status_code))
                return newses
            newses_page = r.content
            current_page += 1
            for link in News.__get_links_to_news(newses_page):
                link = News.WEBSITE_URL + link
                r = requests.get(link)
                if r.status_code != 200:
                    LOGGER.warning("Response code of url: {} was {}. Skipping this page."
                                   .format(link, r.status_code))
                    continue
                news_page = r.content
                newses.append(News.__parse_news_page(news_page))
                if len(newses) == amount:  # If we already add enough news return array.
                    return newses
        return newses

    @staticmethod
    def __get_links_to_news(page, path="//div[@class='story-content']/a/@href"):
        """
        Scarp links to newses from news/archive page.
        :param path: xpath to link. Default is current(22/09/2017) xpath.
        :param page: html representation of euters.com news/archive page.
        :return: array with links to newses.
        """
        links = []
        try:
            tree = html.fromstring(page)
            links = tree.xpath(path)
        except Exception:
            LOGGER.warning("Cant scrap links for webpage, xpath was: " + path)
        return links

    @staticmethod
    def __parse_news_page(page):
        """
        Parse news page of reuters.com for title, text, tags, images, data.
        :param page: html representation of reuters.com news page.
        :return: News object.
        """
        tree = html.fromstring(page)
        title = News.__parse_for_title(tree)
        text = News.__parse_for_text(tree)
        date = News.__parse_for_date(tree)
        images = News.__parse_for_images(tree)
        return News(title, text, date, images)

    @staticmethod
    def __parse_for_title(tree, path="//h1[@class='ArticleHeader_headline_2zdFM']/text()"):
        """
        Parse news tree for title.
        :param tree: tree of news page.
        :param path: xpath to title element. Default is current(22/09/2017) xpath.
        :return: title of this news.
        """
        title = ""
        try:
            title = tree.xpath(path)
        except Exception:
            LOGGER.warning("Cant scrap title for news, xpath was: " + path)
        return title[0]

    @staticmethod
    def __parse_for_text(tree, path="//div[@class='ArticleBody_body_2ECha']/p/text()"):
        """
        Parse news tree for text.
        :param tree: tree of news page.
        :param path: xpath to text element. Default is current(22/09/2017) xpath.
        :return: text of this news.
        """
        text = ""
        try:
            text_parts = tree.xpath(path)
            for part in text_parts:
                text += part + '\n'
        except Exception:
            LOGGER.warning("Cant scrap text for news, xpath was: " + path)
        return text

    @staticmethod
    def __parse_for_date(tree, path="//div[@class='ArticleHeader_date_V9eGk']/text()"):
        """
        Parse news tree for date.
        :param tree: tree of news page.
        :param path: xpath to date element. Default is current(22/09/2017) xpath.
        :return: date of this news.
        """
        date = ""
        try:
            date_parts = tree.xpath(path)[0].split("/")
            date = date_parts[0] + date_parts[1]  # remove not needed part of string.
        except Exception:
            LOGGER.warning("Cant scrap date for news, xpath was: " + path)
        return date

    @staticmethod
    def __parse_for_images(tree, path=""):
        """
        Parse news tree for images links.
        :param tree: tree of news page.
        :param path: xpath to images elements. Default is current(22/09/2017) xpath.
        :return: array with links to images.
        """
        images = []
        # TODO parse for images.
        return images

    @staticmethod
    def serialize_news_array_as_json(newses, path=os.path.join(BASE_DIR, "tmp"), filename="news_data.json"):
        """
        Serialize news array to json, create new json file for given path with filename.
        :param newses: array of news.
        :param path: path to directory for storing json file. Default is base directory of script tmp folder.
        If directory does not exist method will create it.
        :param filename: filename of json file. If extension ommited, add it.
        :return: true if successfully serialize array.
        """
        if not os.path.exists(path):
            LOGGER.info("Directory does not exist, creating directory: " + path)
            os.makedirs(path)
        if ".json" not in filename:
            LOGGER.info("Filename: {} does not contain extension .json. Adding extension.".format(filename))
            filename += ".json"
        with open(os.path.join(path, filename), "w".encode("utf-8")) as f:
            json_string = json.dumps([ob.__dict__ for ob in newses])
            f.write(json_string)

    @staticmethod
    def read_file(path=os.path.join(BASE_DIR, "tmp/news_data.json")):
        """
        Read file as json string.
        :param path: path to file. Default is script dir + tmp/news_data.json
        :return: file content as json string.
        """
        with open(path, "r".encode("utf-8")) as f:
            content = f.read()
        return json.loads(content)


if __name__ == '__main__':
    pass