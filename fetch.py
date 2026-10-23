import requests

BASE = "https://hacker-news.firebaseio.com/v0"

def get_top_stories(n=10):
    ids = requests.get(f"{BASE}/topstories.json", timeout=10).json()[:n]
    stories = []
    for i in ids:
        item = requests.get(f"{BASE}/item/{i}.json", timeout=10).json()
        if item and "title" in item:
            stories.append(item)
    return stories

if __name__ == "__main__":
    for s in get_top_stories():
        print(s["title"], "|", s.get("url", "no url"))