from __future__ import annotations

import html
import os
import struct
import zlib
from pathlib import Path
from typing import Any

from utils import configured_site_url, load_json, product_url, root_path, write_text


def png_chunk(kind: bytes, data: bytes) -> bytes:
    import binascii

    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    )


def save_png(path: Path, width: int, height: int, pixels: list[bytearray]) -> None:
    raw = b"".join(b"\x00" + bytes(row) for row in pixels)
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    data += png_chunk(b"IDAT", zlib.compress(raw, 9))
    data += png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def draw_rect(pixels: list[bytearray], width: int, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
    height = len(pixels)
    r, g, b = color
    for yy in range(max(0, y), min(height, y + h)):
        row = pixels[yy]
        for xx in range(max(0, x), min(width, x + w)):
            i = xx * 3
            row[i : i + 3] = bytes((r, g, b))


def generate_hero(path: Path) -> None:
    width, height = 1200, 520
    base = (248, 249, 250)
    pixels = [bytearray(base * width) for _ in range(height)]

    for x in range(0, width, 48):
        draw_rect(pixels, width, x, 0, 2, height, (232, 235, 238))
    for y in range(0, height, 48):
        draw_rect(pixels, width, 0, y, width, 2, (232, 235, 238))

    draw_rect(pixels, width, 720, 70, 330, 260, (16, 118, 110))
    draw_rect(pixels, width, 750, 100, 270, 30, (255, 255, 255))
    draw_rect(pixels, width, 750, 155, 160, 18, (242, 193, 78))
    draw_rect(pixels, width, 750, 195, 220, 18, (255, 255, 255))
    draw_rect(pixels, width, 750, 235, 120, 18, (228, 87, 46))

    draw_rect(pixels, width, 520, 170, 250, 230, (35, 43, 51))
    draw_rect(pixels, width, 550, 205, 190, 20, (255, 255, 255))
    draw_rect(pixels, width, 550, 245, 80, 18, (242, 193, 78))
    draw_rect(pixels, width, 650, 245, 80, 18, (228, 87, 46))
    draw_rect(pixels, width, 550, 290, 160, 18, (255, 255, 255))

    draw_rect(pixels, width, 880, 270, 190, 150, (242, 193, 78))
    draw_rect(pixels, width, 910, 310, 130, 18, (35, 43, 51))
    draw_rect(pixels, width, 910, 350, 80, 18, (16, 118, 110))

    save_png(path, width, height, pixels)


def css() -> str:
    return """
:root {
  color-scheme: light;
  --ink: #20262d;
  --muted: #65717d;
  --line: #d8dee4;
  --paper: #ffffff;
  --soft: #f7f9fb;
  --teal: #0f766e;
  --coral: #e4572e;
  --gold: #f2c14e;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Arial, "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
  color: var(--ink);
  background: var(--paper);
  line-height: 1.7;
}

a { color: inherit; }

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
  padding: 16px clamp(18px, 4vw, 56px);
  border-bottom: 1px solid var(--line);
  background: rgba(255,255,255,.92);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand { font-weight: 700; }

.nav {
  display: flex;
  gap: 18px;
  font-size: 14px;
  color: var(--muted);
}

.nav a { text-decoration: none; }

.hero {
  min-height: min(46vh, 420px);
  display: grid;
  align-items: end;
  padding: clamp(32px, 6vw, 72px) clamp(18px, 4vw, 56px);
  background-image: linear-gradient(90deg, rgba(255,255,255,.95) 0%, rgba(255,255,255,.80) 45%, rgba(255,255,255,.10) 100%), url("./assets/hero.png");
  background-size: cover;
  background-position: center;
}

.hero-inner { max-width: 720px; }

h1, h2, h3 { line-height: 1.25; letter-spacing: 0; }

h1 {
  margin: 0 0 14px;
  font-size: clamp(38px, 6vw, 76px);
}

.lead {
  margin: 0;
  max-width: 640px;
  color: #36424d;
  font-size: clamp(16px, 2.2vw, 21px);
}

.band {
  padding: 44px clamp(18px, 4vw, 56px);
}

.band.alt { background: var(--soft); }

.section-head {
  max-width: 860px;
  margin: 0 auto 24px;
}

.section-head h2 {
  margin: 0 0 8px;
  font-size: clamp(24px, 3vw, 36px);
}

.section-head p { margin: 0; color: var(--muted); }

.product-grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.article-grid {
  max-width: 1120px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  padding: 22px;
  display: flex;
  min-height: 360px;
  flex-direction: column;
}

.badge {
  display: inline-flex;
  width: fit-content;
  padding: 3px 9px;
  border-radius: 999px;
  background: #e5f3f1;
  color: var(--teal);
  font-size: 12px;
  font-weight: 700;
}

.price {
  margin: 14px 0 8px;
  font-size: 26px;
  font-weight: 700;
}

.summary { color: var(--muted); }

.article-meta {
  color: var(--muted);
  font-size: 13px;
  margin: 0 0 10px;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: auto;
  padding-top: 18px;
}

.button {
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 14px;
  border-radius: 6px;
  border: 1px solid var(--ink);
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

.button.primary {
  background: var(--ink);
  color: white;
}

.button.disabled {
  border-color: var(--line);
  color: var(--muted);
  pointer-events: none;
}

.content {
  max-width: 840px;
  margin: 0 auto;
}

.content h1 { font-size: clamp(32px, 5vw, 56px); }
.content h2 { margin-top: 36px; }
.content li { margin: 8px 0; }

.notice {
  border-left: 4px solid var(--gold);
  background: #fff9e8;
  padding: 14px 16px;
  margin: 20px 0;
}

.tool-list {
  max-width: 840px;
  margin: 0 auto;
  display: grid;
  gap: 14px;
}

.tool-item {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--paper);
  padding: 18px;
}

.tool-item h3 { margin: 0 0 8px; }
.tool-item p { margin: 0 0 12px; color: var(--muted); }

.footer {
  border-top: 1px solid var(--line);
  padding: 28px clamp(18px, 4vw, 56px);
  color: var(--muted);
  font-size: 14px;
}

.footer a { margin-right: 14px; }

@media (max-width: 860px) {
  .product-grid,
  .article-grid { grid-template-columns: 1fr; }
  .topbar { align-items: flex-start; flex-direction: column; }
  .hero { min-height: 360px; }
}
""".strip()


def page_shell(
    title: str,
    body: str,
    brand: dict[str, Any],
    description: str | None = None,
    prefix: str = "",
) -> str:
    analytics = brand.get("google_analytics_id") or os.environ.get("GOOGLE_ANALYTICS_ID") or ""
    analytics_tag = ""
    if analytics:
        analytics_tag = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={html.escape(analytics)}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{html.escape(analytics)}');
</script>
"""
    desc = html.escape(description or brand["description"])
    root_href = prefix or "./"
    products_href = f"{root_href}#products"
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{html.escape(title)} | {html.escape(brand['name'])}</title>
  <link rel="stylesheet" href="{html.escape(prefix)}assets/styles.css">
  {analytics_tag}
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{html.escape(root_href)}">{html.escape(brand['name'])}</a>
    <nav class="nav">
      <a href="{html.escape(products_href)}">商品</a>
      <a href="{html.escape(prefix)}articles/">記事</a>
      <a href="{html.escape(prefix)}disclaimer/">免責</a>
      <a href="{html.escape(prefix)}privacy/">プライバシー</a>
      <a href="{html.escape(prefix)}contact/">問い合わせ</a>
    </nav>
  </header>
  {body}
  <footer class="footer">
    <div>{html.escape(brand['name'])}</div>
    <a href="{html.escape(prefix)}privacy/">Privacy</a>
    <a href="{html.escape(prefix)}disclaimer/">Disclaimer</a>
    <a href="{html.escape(prefix)}contact/">Contact</a>
  </footer>
</body>
</html>
"""


def get_product(products: list[dict[str, Any]], slug: str) -> dict[str, Any]:
    for product in products:
        if product["slug"] == slug:
            return product
    return products[0]


def get_affiliate(affiliate: dict[str, Any], name: str) -> dict[str, Any] | None:
    for link in affiliate.get("links", []):
        if link.get("program_name") == name and link.get("status") == "approved":
            return link
    return None


def render_affiliate_tools(affiliate: dict[str, Any]) -> str:
    links = [item for item in affiliate.get("links", []) if item.get("status") == "approved" and item.get("url")]
    if not links:
        return ""

    items = []
    for item in links:
        pixel = ""
        if item.get("impression_pixel"):
            pixel = (
                f'<img border="0" width="1" height="1" src="{html.escape(item["impression_pixel"])}" '
                'alt="" loading="lazy">'
            )
        items.append(
            f"""<article class="tool-item">
  <h3>{html.escape(item.get('program_name', '制作補助ツール'))}</h3>
  <p>動画編集や画面録画をまとめて扱いたい場合は、制作補助ツールの選択肢になります。必要な機能が合うか、公式情報を確認してから検討してください。</p>
  <a class="button" href="{html.escape(item['url'])}" rel="nofollow sponsored">{html.escape(item.get('text', item.get('program_name', '詳細を見る')))}</a>
  {pixel}
</article>"""
        )

    return f"""
<section class="band">
  <div class="section-head">
    <h2>制作補助ツール</h2>
    <p>{html.escape(affiliate.get('disclosure', '広告・アフィリエイトリンクを含みます。'))}</p>
  </div>
  <div class="tool-list">
    {''.join(items)}
  </div>
</section>
"""


def render_articles_section(topics: list[dict[str, Any]], products: list[dict[str, Any]]) -> str:
    cards = []
    for topic in topics[:6]:
        product = get_product(products, topic["product_slug"])
        cards.append(
            f"""<article class="card">
  <p class="article-meta">実用メモ</p>
  <h3>{html.escape(topic['title'])}</h3>
  <p class="summary">{html.escape(topic['angle'])}</p>
  <div class="actions">
    <a class="button" href="articles/{html.escape(topic['slug'])}/">読む</a>
    <a class="button" href="products/{html.escape(product['slug'])}/">関連商品</a>
  </div>
</article>"""
        )

    return f"""
<section class="band alt">
  <div class="section-head">
    <h2>実用メモ</h2>
    <p>note販売、匿名発信、SNS投稿導線を小さく改善するための短い記事です。</p>
  </div>
  <div class="article-grid">
    {''.join(cards)}
  </div>
</section>
"""


def render_index(
    brand: dict[str, Any],
    rules: dict[str, Any],
    products: list[dict[str, Any]],
    site_url: str,
    affiliate: dict[str, Any],
    topics: list[dict[str, Any]],
) -> str:
    cards = []
    for product in products:
        detail_url = f"products/{product['slug']}/"
        note = product.get("note_url") or ""
        note_button = (
            f'<a class="button primary" href="{html.escape(note)}">noteで読む</a>'
            if note
            else '<span class="button disabled">note準備中</span>'
        )
        cards.append(
            f"""<article class="card">
  <span class="badge">有料ミニ商品</span>
  <h3>{html.escape(product['title'])}</h3>
  <div class="price">{product['price_yen']:,}円</div>
  <p class="summary">{html.escape(product['summary'])}</p>
  <div class="actions">
    <a class="button" href="{detail_url}">詳細を見る</a>
    {note_button}
  </div>
</article>"""
        )

    body = f"""
<section class="hero">
  <div class="hero-inner">
    <h1>{html.escape(brand['name'])}</h1>
    <p class="lead">{html.escape(brand['tagline'])}。小さなテンプレート商品から始め、反応が出たテーマだけ育てます。</p>
  </div>
</section>
<section class="band" id="products">
  <div class="section-head">
    <h2>商品</h2>
    <p>{html.escape(rules['required_disclosure'])}</p>
  </div>
  <div class="product-grid">
    {''.join(cards)}
  </div>
</section>
{render_articles_section(topics, products)}
{render_affiliate_tools(affiliate)}
<section class="band alt">
  <div class="content">
    <h2>運用方針</h2>
    <p>匿名で始めやすい有料noteとテンプレート商品を中心に、SNS投稿と検索流入から販売ページへ案内します。成果を保証する表現は使わず、購入前に内容と注意点がわかる形で公開します。</p>
  </div>
</section>
"""
    return page_shell(brand["name"], body, brand)


def render_article_index(
    topics: list[dict[str, Any]],
    products: list[dict[str, Any]],
    brand: dict[str, Any],
) -> str:
    cards = []
    for topic in topics:
        product = get_product(products, topic["product_slug"])
        cards.append(
            f"""<article class="card">
  <p class="article-meta">実用メモ</p>
  <h3>{html.escape(topic['title'])}</h3>
  <p class="summary">{html.escape(topic['angle'])}</p>
  <div class="actions">
    <a class="button" href="{html.escape(topic['slug'])}/">読む</a>
    <a class="button" href="../products/{html.escape(product['slug'])}/">関連商品</a>
  </div>
</article>"""
        )
    body = f"""
<main class="band">
  <div class="section-head">
    <h1>実用メモ</h1>
    <p>匿名で小さく始めるnote販売、SNS投稿、デジタル商品作成の改善メモです。</p>
  </div>
  <div class="article-grid">
    {''.join(cards)}
  </div>
</main>
"""
    return page_shell("実用メモ", body, brand, prefix="../")


def render_article(
    topic: dict[str, Any],
    products: list[dict[str, Any]],
    affiliate: dict[str, Any],
    brand: dict[str, Any],
    rules: dict[str, Any],
) -> str:
    product = get_product(products, topic["product_slug"])
    product_link = product.get("note_url") or f"../../products/{html.escape(product['slug'])}/"
    affiliate_link = get_affiliate(affiliate, topic.get("affiliate_program", ""))
    affiliate_block = ""
    if affiliate_link:
        pixel = ""
        if affiliate_link.get("impression_pixel"):
            pixel = (
                f'<img border="0" width="1" height="1" src="{html.escape(affiliate_link["impression_pixel"])}" '
                'alt="" loading="lazy">'
            )
        affiliate_block = f"""
    <h2>制作補助ツール</h2>
    <p>動画編集や画面録画をまとめて扱いたい場合は、{html.escape(affiliate_link['program_name'])} のような制作補助ツールも選択肢になります。必要な機能が合うか、公式情報を確認してから検討してください。</p>
    <p><a class="button" href="{html.escape(affiliate_link['url'])}" rel="nofollow sponsored">{html.escape(affiliate_link.get('text', affiliate_link['program_name']))}</a>{pixel}</p>
"""

    body = f"""
<main class="band">
  <article class="content">
    <p class="article-meta">実用メモ</p>
    <h1>{html.escape(topic['title'])}</h1>
    <p class="lead">{html.escape(topic['angle'])}ためのメモです。</p>
    <div class="notice">{html.escape(rules['required_disclosure'])}</div>
    <h2>結論</h2>
    <p>最初から大きな仕組みを作るより、1つの小さな商品、1つの投稿導線、1つの改善ポイントに絞るほうが動きやすくなります。</p>
    <h2>まず決めること</h2>
    <ul>
      <li>誰に向けるか</li>
      <li>無料部分でどこまで見せるか</li>
      <li>有料部分に何を入れるか</li>
      <li>投稿からどのページへ案内するか</li>
      <li>今週どの数字だけを見るか</li>
    </ul>
    <h2>失敗しやすいところ</h2>
    <p>成果を急いで強い言葉に寄せると、読者の期待値がずれます。成果保証ではなく、作業時間を短くするテンプレートやチェックリストとして見せるほうが安全です。</p>
    <h2>今日やること</h2>
    <ul>
      <li>見出しを1つだけ改善する</li>
      <li>X投稿を1本作る</li>
      <li>リンク先がスマホで読めるか確認する</li>
    </ul>
    <h2>関連テンプレート</h2>
    <p>{html.escape(product['title'])}</p>
    <p><a class="button primary" href="{html.escape(product_link)}">関連ページを見る</a></p>
    {affiliate_block}
  </article>
</main>
"""
    return page_shell(topic["title"], body, brand, topic["angle"], prefix="../../")


def render_product(product: dict[str, Any], brand: dict[str, Any], rules: dict[str, Any]) -> str:
    free_items = "".join(f"<li>{html.escape(item)}</li>" for item in product["free_value"])
    paid_items = "".join(f"<li>{html.escape(item)}</li>" for item in product["paid_value"])
    note = product.get("note_url") or ""
    action = (
        f'<a class="button primary" href="{html.escape(note)}">noteで読む</a>'
        if note
        else '<span class="button disabled">販売ページ準備中</span>'
    )
    body = f"""
<main class="band">
  <article class="content">
    <h1>{html.escape(product['title'])}</h1>
    <p class="lead">{html.escape(product['summary'])}</p>
    <div class="notice">{html.escape(rules['required_disclosure'])}</div>
    <p class="price">{product['price_yen']:,}円</p>
    <div class="actions">{action}<a class="button" href="../../">一覧へ戻る</a></div>
    <h2>合う人</h2>
    <p>{html.escape(product['audience'])}</p>
    <h2>無料部分</h2>
    <ul>{free_items}</ul>
    <h2>有料部分</h2>
    <ul>{paid_items}</ul>
    <h2>購入前の注意</h2>
    <p>この商品は成果を保証するものではありません。下書き、テンプレート、チェックリストを使って作業時間を短くするためのコンテンツです。</p>
  </article>
</main>
"""
    return page_shell(product["title"], body, brand, product["summary"], prefix="../../")


def render_simple_page(title: str, content: str, brand: dict[str, Any]) -> str:
    return page_shell(
        title,
        f'<main class="band"><article class="content">{content}</article></main>',
        brand,
        prefix="../",
    )


def render_feed(
    brand: dict[str, Any],
    products: list[dict[str, Any]],
    topics: list[dict[str, Any]],
    site_url: str,
) -> str:
    items = []
    for product in products:
        url = product_url(site_url, product)
        items.append(
            f"""<item>
  <title>{html.escape(product['title'])}</title>
  <link>{html.escape(url)}</link>
  <guid>{html.escape(url)}</guid>
  <description>{html.escape(product['summary'])}</description>
</item>"""
        )
    for topic in topics:
        url = f"{site_url}articles/{topic['slug']}/"
        items.append(
            f"""<item>
  <title>{html.escape(topic['title'])}</title>
  <link>{html.escape(url)}</link>
  <guid>{html.escape(url)}</guid>
  <description>{html.escape(topic['angle'])}</description>
</item>"""
        )
    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{html.escape(brand['name'])}</title>
  <link>{html.escape(site_url)}</link>
  <description>{html.escape(brand['description'])}</description>
  {''.join(items)}
</channel>
</rss>
"""


def render_sitemap(products: list[dict[str, Any]], topics: list[dict[str, Any]], site_url: str) -> str:
    urls = [site_url, f"{site_url}articles/", f"{site_url}privacy/", f"{site_url}disclaimer/", f"{site_url}contact/"]
    urls.extend(product_url(site_url, product) for product in products)
    urls.extend(f"{site_url}articles/{topic['slug']}/" for topic in topics)
    locs = "".join(f"<url><loc>{html.escape(url)}</loc></url>" for url in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{locs}
</urlset>
"""


def build() -> list[Path]:
    brand = load_json("config", "brand.json")
    rules = load_json("config", "rules.json")
    products = load_json("data", "products.json")
    affiliate = load_json("config", "affiliate_links.json")
    topics = load_json("data", "growth_topics.json")
    site_url = configured_site_url(brand)
    site_dir = root_path("site")
    written: list[Path] = []

    generate_hero(site_dir / "assets" / "hero.png")
    write_text(site_dir / "assets" / "styles.css", css())
    written.append(site_dir / "assets" / "styles.css")

    write_text(site_dir / "index.html", render_index(brand, rules, products, site_url, affiliate, topics))
    written.append(site_dir / "index.html")

    for product in products:
        path = site_dir / "products" / product["slug"] / "index.html"
        write_text(path, render_product(product, brand, rules))
        written.append(path)

    article_index = site_dir / "articles" / "index.html"
    write_text(article_index, render_article_index(topics, products, brand))
    written.append(article_index)

    for topic in topics:
        path = site_dir / "articles" / topic["slug"] / "index.html"
        write_text(path, render_article(topic, products, affiliate, brand, rules))
        written.append(path)

    privacy = """
<h1>プライバシーポリシー</h1>
<p>当サイトでは、アクセス解析や広告・アフィリエイトリンクを利用する場合があります。取得される情報は、サイト改善、クリック計測、成果確認のために使います。</p>
<p>外部サービスのCookieや識別子が利用される場合があります。ブラウザ設定によりCookieを無効にできます。</p>
"""
    disclaimer = """
<h1>免責事項</h1>
<p>当サイトのコンテンツは、作業効率化や収益化検証の参考情報です。成果、収益、審査通過を保証するものではありません。</p>
<p>リンク先の商品やサービスの条件は変更される場合があります。購入や登録の前に、公式情報と利用規約を確認してください。</p>
"""
    contact = f"""
<h1>問い合わせ</h1>
<p>連絡先: {html.escape(brand.get('contact', 'contact@example.com'))}</p>
"""
    write_text(site_dir / "privacy" / "index.html", render_simple_page("プライバシーポリシー", privacy, brand))
    write_text(site_dir / "disclaimer" / "index.html", render_simple_page("免責事項", disclaimer, brand))
    write_text(site_dir / "contact" / "index.html", render_simple_page("問い合わせ", contact, brand))
    write_text(site_dir / "feed.xml", render_feed(brand, products, topics, site_url))
    write_text(site_dir / "sitemap.xml", render_sitemap(products, topics, site_url))
    write_text(site_dir / "robots.txt", "User-agent: *\nAllow: /\nSitemap: " + site_url + "sitemap.xml\n")
    written.extend(
        [
            site_dir / "privacy" / "index.html",
            site_dir / "disclaimer" / "index.html",
            site_dir / "contact" / "index.html",
            site_dir / "feed.xml",
            site_dir / "sitemap.xml",
            site_dir / "robots.txt",
        ]
    )
    return written


if __name__ == "__main__":
    for item in build():
        print(item)
