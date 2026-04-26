from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from utils import configured_site_url, load_json, product_url, root_path, write_text


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


def latest_metrics_summary(metrics_path: Path) -> str:
    if not metrics_path.exists():
        return "まだ計測データがありません。"

    with metrics_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = [row for row in csv.DictReader(f) if row.get("date")]

    if not rows:
        return "まだ計測データがありません。"

    latest = rows[-1]
    return (
        f"最新記録: {latest.get('date', '')} / "
        f"X投稿 {latest.get('x_posts', '0')} / "
        f"note閲覧 {latest.get('note_views', '0')} / "
        f"note購入 {latest.get('note_sales', '0')} / "
        f"A8クリック {latest.get('a8_clicks', '0')}"
    )


def article_draft(
    topic: dict[str, Any],
    product: dict[str, Any],
    affiliate_link: dict[str, Any] | None,
    fallback_site_url: str,
) -> str:
    affiliate_block = ""
    if affiliate_link:
        affiliate_block = f"""
## 制作補助ツール

動画編集や画面録画をまとめて扱いたい場合は、{affiliate_link['program_name']} のような制作補助ツールも選択肢になります。

成果や収益を保証するものではありません。必要な機能が合うか、公式情報を確認してから検討してください。

{affiliate_link['url']}
"""

    return f"""# {topic['title']}

このページには広告・アフィリエイトリンク・有料コンテンツへのリンクを含む場合があります。

## 誰向けか

{topic['angle']}人向けです。

## まず決めること

1. 何を作るか
2. 誰に向けるか
3. 無料でどこまで見せるか
4. 有料部分に何を入れるか
5. 投稿からどこへ案内するか

## 失敗しやすいところ

最初から大きな商品や完璧なサイトを作ろうとすると止まりやすくなります。まずは小さなテンプレートやチェックリストを置き、反応を見て増補するほうが現実的です。

## 今日やること

- タイトルを1つ決める
- 無料部分の見出しを3つ書く
- 有料部分に入れるテンプレートを1つ決める
- X投稿を1本作る

## 関連商品

{product['title']}: {product.get('note_url') or product_url(fallback_site_url, product)}
{affiliate_block}
"""


def x_posts(topic: dict[str, Any], product: dict[str, Any], site_url: str) -> list[str]:
    url = product.get("note_url") or site_url
    return [
        f"{topic['title']}。最初に見るのは完成度より、無料部分で何が伝わるかです。小さく出して反応を見ます。{url}",
        f"匿名で始めるなら、プロフィールより先に「扱わないテーマ」を決めるとブレにくくなります。{url}",
        f"有料noteは無料部分を薄くしすぎないほうが作りやすいです。無料で全体像、有料でテンプレート。{url}",
    ]


def csv_escape(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def generate() -> list[Path]:
    brand = load_json("config", "brand.json")
    products = load_json("data", "products.json")
    affiliate = load_json("config", "affiliate_links.json")
    topics = load_json("data", "growth_topics.json")
    site_url = configured_site_url(brand)
    week_start = date.today()
    out_dir = root_path("dist", "growth_pack", week_start.isoformat())
    written: list[Path] = []

    offset = week_start.toordinal() % len(topics)
    selected = (topics[offset:] + topics[:offset])[:3]

    summary_lines = [
        f"# 週次改善パック {week_start.isoformat()}",
        "",
        latest_metrics_summary(root_path("data", "metrics.csv")),
        "",
        "## 今週作る下書き",
    ]

    social_rows = ["scheduled_date,platform,topic_slug,text,url,status"]
    for i, topic in enumerate(selected):
        product = get_product(products, topic["product_slug"])
        link = get_affiliate(affiliate, topic.get("affiliate_program", ""))
        article_path = out_dir / "articles" / f"{topic['slug']}.md"
        write_text(article_path, article_draft(topic, product, link, site_url))
        written.append(article_path)
        summary_lines.append(f"- {topic['title']}: `{article_path.relative_to(root_path())}`")

        for j, text in enumerate(x_posts(topic, product, site_url)):
            scheduled = week_start + timedelta(days=i * 2 + j)
            social_rows.append(
                ",".join(
                    [
                        scheduled.isoformat(),
                        "X",
                        topic["slug"],
                        csv_escape(text),
                        product.get("note_url") or site_url,
                        "draft",
                    ]
                )
            )

    summary_lines.extend(
        [
            "",
            "## 公開前に確認すること",
            "",
            "- 誇大表現がない",
            "- PR/広告表記がある",
            "- 外部公開やSNS投稿はユーザー確認後に行う",
            "- A8リンクは承認済み案件だけ使う",
            "",
            "## 次の改善候補",
            "",
            "- 反応のあったX投稿を1本だけ言い換えて再投稿する",
            "- note無料部分の冒頭3行を読みやすくする",
            "- トップページに記事導線を追加する",
        ]
    )

    summary_path = out_dir / "weekly_plan.md"
    social_path = out_dir / "x_posts.csv"
    write_text(summary_path, "\n".join(summary_lines) + "\n")
    write_text(social_path, "\n".join(social_rows) + "\n")
    written.extend([summary_path, social_path])
    return written


if __name__ == "__main__":
    for path in generate():
        print(path)

