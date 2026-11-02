import unittest

from url_utils import normalize_url


class TestNormalizeUrl(unittest.TestCase):
    def test_removes_tracking_parameters_and_fragment(self):
        url = "https://Example.com/story/?utm_source=email#comments"

        result = normalize_url(url)

        self.assertEqual(result, "https://example.com/story")

    def test_preserves_meaningful_query_parameters(self):
        url = "https://example.com/article?id=123&utm_medium=email"

        result = normalize_url(url)

        self.assertEqual(result, "https://example.com/article?id=123")

    def test_adds_https_when_scheme_is_missing(self):
        result = normalize_url("example.com/news")

        self.assertEqual(result, "https://example.com/news")

    def test_preserves_root_trailing_slash(self):
        result = normalize_url("https://example.com/")

        self.assertEqual(result, "https://example.com/")

    def test_rejects_empty_url(self):
        with self.assertRaises(ValueError):
            normalize_url("")

    def test_rejects_whitespace_only_url(self):
        with self.assertRaises(ValueError):
            normalize_url("   ")


if __name__ == "__main__":
    unittest.main()