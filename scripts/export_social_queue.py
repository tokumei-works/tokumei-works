from __future__ import annotations

import csv
import json
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote

from utils import compact, configured_site_url, load_json, product_url, root_path


def x_text(product: dict, url: str, n: int) -> str:
    patterns = [
        f"匿名で小さく収益化を始めるなら、最初に作るのは大きな教材ではなく小さなテンプレートで十分です。有料コンテンツ案内: {product['title']} {url}",
        f"有料noteは無料部分を薄くしすぎると信頼が作れません。無料部分で全体像、有料部分でテンプレートを渡す形が始めやすいです。{url}",
        f"今日のチェック: プロフィール導線、PR表記、購入前の注意、スマホ表示。小さく売って反応を見ます。{url}",
    ]
    return patterns[n % len(patterns)]


def x_profile_url(brand: dict) -> str:
    return brand.get("x_url", "").strip()


def instagram_text(product: dict, url: str, n: int) -> str:
    patterns = [
        f"匿名で始める小さな収益化\\n\\n1. テーマを決める\\n2. 扱わない話題を決める\\n3. 最初の商品を1つ作る\\n4. 投稿から販売ページへつなぐ\\n\\n{product['title']}\\n{url}",
        f"売り込み感を下げる投稿の作り方\\n\\n・先に悩みを整理する\\n・無料で1つ役に立つことを書く\\n・最後に必要な人だけ案内する\\n\\n{url}",
        f"有料note公開前チェック\\n\\n・成果保証を書かない\\n・PR表記を入れる\\n・無料部分だけでも価値を出す\\n・リンク先を確認する\\n\\n{url}",
    ]
    return patterns[n % len(patterns)]


def shorts_text(product: dict, url: str, n: int) -> str:
    patterns = [
        f"Hook: 匿名で副業を始めるなら、最初に大きな教材は作らなくていいです。\\nScript: まず小さなテンプレートを1つ作ります。次に無料部分で価値を見せます。最後に必要な人だけ有料部分へ案内します。\\nDescription: {product['title']} {url}",
        f"Hook: 有料noteが売れにくい原因は、無料部分が薄すぎることがあります。\\nScript: 無料部分で全体像を渡し、有料部分で手順とテンプレートを渡すと、期待値がそろいやすくなります。\\nDescription: {url}",
        f"Hook: 投稿が続かないときは、30日分を先に作るより、3つの型を回します。\\nScript: 共感、チェックリスト、制作過程。この3つを回すだけで販売導線を自然に置きやすくなります。\\nDescription: {url}",
    ]
    return patterns[n % len(patterns)]


def export() -> tuple[Path, Path]:
    brand = load_json("config", "brand.json")
    rules = load_json("config", "rules.json")
    products = load_json("data", "products.json")
    site_url = configured_site_url(brand)
    out_dir = root_path("dist")
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "social_queue.csv"
    x_json_path = out_dir / "x_intents.json"
    profile_url = x_profile_url(brand)

    rows = []
    intents = []
    today = date.today()
    post_count = int(rules.get("daily_social_posts", 3))
    platforms = ["X", "Instagram", "YouTube Shorts"]
    for day in range(14):
        product = products[day % len(products)]
        url = product.get("note_url") or product_url(site_url, product)
        for slot in range(post_count):
            platform = platforms[slot % len(platforms)]
            scheduled = today + timedelta(days=day)
            if platform == "X":
                text = compact(x_text(product, url, day + slot))
                if len(text) > rules.get("max_x_chars", 240):
                    text = text[: rules.get("max_x_chars", 240) - 1] + "…"
                intents.append(
                    {
                        "scheduled_date": scheduled.isoformat(),
                        "product_slug": product["slug"],
                        "text": text,
                        "intent_url": "https://twitter.com/intent/tweet?text=" + quote(text),
                        "profile_url": profile_url,
                    }
                )
            elif platform == "Instagram":
                text = instagram_text(product, url, day + slot)
            else:
                text = shorts_text(product, url, day + slot)
            rows.append(
                {
                    "scheduled_date": scheduled.isoformat(),
                    "platform": platform,
                    "product_slug": product["slug"],
                    "text": text,
                    "url": url,
                    "asset": "site/assets/hero.png",
                    "status": "draft",
                    "profile_url": profile_url,
                }
            )

    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scheduled_date",
                "platform",
                "product_slug",
                "text",
                "url",
                "asset",
                "status",
                "profile_url",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    x_json_path.write_text(json.dumps(intents, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return csv_path, x_json_path


if __name__ == "__main__":
    print(export())
