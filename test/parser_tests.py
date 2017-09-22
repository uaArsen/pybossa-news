import json
import os
import unittest

from configs.main_configs import BASE_DIR
from news_parser.parser import News


class TestParser(unittest.TestCase):
    """
    Test for parser module.
    """

    def tearDown(self):
        """
        Remove test files.
        """
        path = os.path.join(BASE_DIR, "tmp/test.json")
        if os.path.exists(path):
            os.remove(path)

    def test_parse_reuters_com_website_return_news_from_reuters_com(self):
        """
        Integration test, testing that we method successfully scribe given amount of newses.
        """
        result = News.parse_reuters_com_website(17)
        self.assertEqual(17, len(result))
        for n in result:
            self.assertIsInstance(n, News)
            self.assertTrue(n.title and len(n.title) > 0)
            self.assertTrue(n.text and len(n.text) > 50)
            self.assertTrue(n.date and len(n.date) > 5)

    def test_news_json_serialization_is_correct(self):
        """
        Testing json serialization is correct.
        """
        newses = [News("Test1 title", "Test1 text", "Test1 date", ["Test1 image"]),
                  News("Test2 title", "Test2 text", "Test2 date", ["Test2 image"])
                  ]
        News.serialize_news_array_as_json(newses, filename="test")
        path = os.path.join(BASE_DIR, "tmp/test.json")
        self.assertTrue(os.path.exists(path) and os.path.isfile(path))
        with open(path, "r") as f:
            content = f.read()
            self.assertTrue(len(content) > 0)
            json.loads(content)  # If throw exception than cant create json from string.

    def test_news_json_deserialization_is_correct(self):
        """
        Testing json deserialization is correct.
        """
        News.serialize_news_array_as_json([News("Test1 title", "Test1 text", "Test1 date", [])], filename="test")
        path = os.path.join(BASE_DIR, "tmp/test.json")
        d = News.read_file(path)
        self.assertEquals(d[0]["title"], "Test1 title")
        self.assertEquals(d[0]["text"], "Test1 text")
        self.assertEquals(d[0]["date"], "Test1 date")
        self.assertEquals(d[0]["images"], [])
