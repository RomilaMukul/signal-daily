import os
import tempfile
import unittest

import db


class TestDatabaseDeduplication(unittest.TestCase):
    def setUp(self):
        file_descriptor, self.database_path = tempfile.mkstemp(
            suffix=".db"
        )
        os.close(file_descriptor)

        self.original_db_name = db.DB_NAME
        db.DB_NAME = self.database_path
        db.init_db()

    def tearDown(self):
        db.DB_NAME = self.original_db_name
        os.remove(self.database_path)

    def test_normalized_url_is_not_inserted_twice(self):
        first_article = {
            "title": "First version",
            "url": "https://example.com/story?utm_source=email",
            "source": "Test",
        }

        second_article = {
            "title": "Second version",
            "url": "https://example.com/story",
            "source": "Test",
        }

        self.assertEqual(db.save_articles([first_article]), 1)
        self.assertEqual(db.save_articles([second_article]), 0)


if __name__ == "__main__":
    unittest.main()