from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape


OUTPUT_FILE = "index.html"


def format_published_at(published_at):
    """Return a human-readable UTC datetime string."""
    if published_at is None:
        return "Unknown publish time"

    return datetime.fromtimestamp(published_at, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )


def generate_html(articles, output_file=OUTPUT_FILE):
    """Generate a styled static HTML page with ranked articles."""
    article_items = []

    for rank, article in enumerate(articles, start=1):
        title = escape(article.get("title", "Untitled"))
        source = escape(article.get("source", "Unknown source"))
        url = escape(article.get("url", "#"))
        published_at = format_published_at(article.get("published_at"))
        score = article.get("score", 0)

        article_items.append(
            (
                f"<article class=\"story\">"
                f"<div class=\"story-rank\">{rank:02}</div>"
                f"<div class=\"story-body\">"
                f"<div class=\"story-meta\"><span class=\"source\">{source}</span>"
                f"<span>{published_at}</span></div>"
                f"<h2><a href=\"{url}\" target=\"_blank\" "
                f"rel=\"noopener noreferrer\">{title}</a></h2>"
                f"<p class=\"story-score\">Signal score <strong>{score}</strong></p>"
                f"</div>"
                f"</article>"
            )
        )

    html_content = (
        "<!doctype html>"
        "<html lang=\"en\">"
        "<head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<style>"
        ":root{"
        "--background:#211c23;"
        "--surface:#2b252e;"
        "--surface-hover:#352d38;"
        "--text:#f5f1f5;"
        "--muted:#b8adb9;"
        "--accent:#c78bc7;"
        "--line:#493e4b;"
        "}"
        "*{box-sizing:border-box;}"
        "body{margin:0;background:var(--background);color:var(--text);"
        "font-family:Arial,Helvetica,sans-serif;line-height:1.5;}"
        ".shell{width:min(1120px,calc(100% - 40px));margin:0 auto;}"
        ".site-header{display:flex;align-items:center;justify-content:space-between;"
        "padding:28px 0;border-bottom:1px solid var(--line);}"
        ".brand{color:var(--text);font-size:1.25rem;font-weight:700;"
        "letter-spacing:.12em;text-decoration:none;text-transform:uppercase;}"
        ".brand-mark{color:var(--accent);}"
        ".nav{display:flex;gap:28px;color:var(--muted);font-size:.8rem;"
        "letter-spacing:.08em;text-transform:uppercase;}"
        ".nav span{white-space:nowrap;}"
        ".hero{padding:88px 0 72px;max-width:760px;}"
        ".eyebrow{color:var(--accent);font-size:.78rem;font-weight:700;"
        "letter-spacing:.16em;text-transform:uppercase;}"
        "h1{font-size:clamp(3rem,8vw,6.5rem);font-weight:400;line-height:.95;"
        "letter-spacing:-.06em;margin:22px 0 28px;}"
        ".hero h1 em{color:var(--accent);font-family:Georgia,serif;font-weight:400;}"
        ".hero p{color:var(--muted);font-size:1.05rem;max-width:560px;}"
        ".section-heading{align-items:end;border-bottom:1px solid var(--line);"
        "display:flex;justify-content:space-between;margin-bottom:18px;padding-bottom:14px;}"
        ".section-heading h2{font-size:1.1rem;font-weight:400;letter-spacing:.08em;"
        "margin:0;text-transform:uppercase;}"
        ".section-heading span{color:var(--muted);font-size:.8rem;}"
        ".stories{display:grid;gap:10px;margin-bottom:72px;}"
        ".story{background:var(--surface);display:grid;gap:20px;grid-template-columns:56px 1fr;"
        "padding:26px 28px;transition:background .2s ease;}"
        ".story:hover{background:var(--surface-hover);}"
        ".story-rank{color:var(--accent);font-family:Georgia,serif;font-size:1.4rem;"
        "padding-top:2px;}"
        ".story-meta{color:var(--muted);display:flex;flex-wrap:wrap;font-size:.75rem;"
        "gap:14px;letter-spacing:.05em;text-transform:uppercase;}"
        ".source{color:var(--accent);}"
        ".story h2{font-size:clamp(1.25rem,2.4vw,2rem);font-weight:400;line-height:1.15;"
        "margin:12px 0;max-width:820px;}"
        ".story h2 a{color:var(--text);text-decoration:none;}"
        ".story h2 a:hover{color:var(--accent);}"
        ".story-score{color:var(--muted);font-size:.8rem;margin:0;}"
        ".story-score strong{color:var(--text);font-weight:400;}"
        "footer{border-top:1px solid var(--line);color:var(--muted);font-size:.8rem;"
        "padding:24px 0 40px;}"
        "@media(max-width:650px){"
        ".shell{width:min(100% - 28px,1120px);}"
        ".site-header{align-items:flex-start;gap:18px;}"
        ".nav{flex-direction:column;gap:5px;text-align:right;}"
        ".hero{padding:60px 0 50px;}"
        ".story{grid-template-columns:36px 1fr;padding:20px 18px;}"
        "}"
        "</style>"
        "<title>Signal Daily</title>"
        "</head>"
        "<body>"
        "<div class=\"shell\">"
        "<header class=\"site-header\">"
        "<a class=\"brand\" href=\"index.html\">Signal<span class=\"brand-mark\">.</span></a>"
        "<nav class=\"nav\"><span>Technology</span><span>Finance</span>"
        "<span>Daily Brief</span></nav>"
        "</header>"
        "<main>"
        "<section class=\"hero\">"
        "<div class=\"eyebrow\">The daily signal</div>"
        "<h1>News for <em>better</em> decisions.</h1>"
        "<p>Ranked technology and finance stories, collected from trusted sources "
        "and refreshed every day.</p>"
        "</section>"
        "<section>"
        "<div class=\"section-heading\"><h2>Latest intelligence</h2>"
        f"<span>{len(article_items)} stories</span></div>"
        "<div class=\"stories\">"
        + "".join(article_items) +
        "</div>"
        "</section>"
        "</main>"
        "<footer>Signal Daily &mdash; technology, finance, and the ideas shaping tomorrow.</footer>"
        "</div>"
        "</body>"
        "</html>"
    )

    Path(output_file).write_text(html_content, encoding="utf-8")
