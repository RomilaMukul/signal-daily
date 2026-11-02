from urllib.parse import (
    parse_qsl,
    urlencode,
    urlparse,
    urlunparse,
)
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "gclid",
    "fbclid",
}

def normalize_url(url):

    # 1. Reject empty URLs
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")

    # 2. Remove unnecessary whitespace
    url = url.strip()

    # 3. Add HTTPS if scheme is missing
    if "://" not in url:
        url = "https://" + url

    # 4. Parse URL into components
    parsed = urlparse(url)

    # 5. Validate hostname
    if not parsed.hostname:
        raise ValueError("Invalid URL: missing hostname")

    # 6. Lowercase hostname
    hostname = parsed.hostname.lower()

    # Preserve username/password and port if present
    if parsed.port:
        hostname += f":{parsed.port}"

    if parsed.username:
        credentials = parsed.username
        if parsed.password:
            credentials += f":{parsed.password}"
        hostname = f"{credentials}@{hostname}"

    # 7. Remove tracking parameters
    query_params = parse_qsl(
        parsed.query,
        keep_blank_values=True
    )

    filtered_params = [
        (key, value)
        for key, value in query_params
        if key.lower() not in TRACKING_PARAMS
    ]

    # 8. Rebuild query string
    clean_query = urlencode(filtered_params)

    # 9. Remove trailing slash except root
    path = parsed.path

    if path != "/":
        path = path.rstrip("/")

    # 10. Rebuild normalized URL
    normalized = urlunparse((
        parsed.scheme.lower(),
        hostname,
        path,
        parsed.params,
        clean_query,
        ""  # Remove fragment
    ))

    return normalized

if __name__ == "__main__":

    test_urls = [
        "https://Example.com/story/?utm_source=x#top",

        "https://example.com/article?id=123&utm_medium=email",

        "https://example.com/article?id=123",

        "example.com/news/?fbclid=123",

        "https://example.com/"
    ]

    for url in test_urls:

        result = normalize_url(url)

        print("Original :", url)
        print("Normalized:", result)
        print("-" * 50)
