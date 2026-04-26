from __future__ import annotations

from pathlib import Path
from typing import Any

from utils import configured_site_url, load_json, root_path, write_text


def primary_product(products: list[dict[str, Any]]) -> dict[str, Any]:
    for product in products:
        if product.get("note_url"):
            return product
    return products[0]


def generate() -> Path:
    brand = load_json("config", "brand.json")
    products = load_json("data", "products.json")
    site_url = configured_site_url(brand)
    product = primary_product(products)
    note_url = product.get("note_url") or site_url
    x_url = brand.get("x_url", "").strip()

    content = f"""# Launch Copy

外部サービスに貼るための初期設定文です。公開やプロフィール変更は、各サービスの画面で確認してから反映してください。

## 共通リンク

- 公式サイト: {site_url}
- note販売ページ: {note_url}
- Xプロフィール: {x_url}

## noteプロフィール

### 名前

{brand["name"]}

### プロフィール文

匿名で小さく始めるデジタル収益化の実用メモとテンプレートを作っています。note有料ミニ商品、SNS投稿導線、公開前チェックリストを中心に更新します。

### プロフィールURL

{site_url}

## Xプロフィール

### 名前

{brand["name"]}

### 自己紹介

匿名で小さく始めるnote販売・SNS投稿・テンプレート作成の実用メモ。成果保証ではなく、公開前チェックと作業短縮の型を共有します。

### Web

{site_url}

## X固定ポスト

匿名で小さく収益化を始める人向けに、最初の導線をまとめました。

まずは大きな教材ではなく、1つの小さなテンプレートと販売ページから。

公開前チェック、note構成、SNS投稿導線はこちら。
{note_url}

この投稿には有料コンテンツへのリンクを含みます。

## 今日の初回X投稿

匿名で有料noteを出すなら、最初に作るのは大きな教材より「小さなチェックリスト」で十分です。

無料部分で全体像を見せて、有料部分でテンプレートを渡す。
まずはここから始めます。

{note_url}

この投稿には有料コンテンツへのリンクを含みます。

## note記事への追記

公開後の追記:

公式サイト側にも、関連テンプレートと実用メモをまとめました。
{site_url}

今後は、匿名運用の公開前チェック、SNS投稿導線、note販売ページの改善メモを追加していきます。

## Instagramプロフィール

匿名で小さく始めるnote販売・SNS投稿・テンプレート作成の実用メモ。公開前チェックと作業短縮の型を更新します。

リンク: {site_url}

## YouTube概要欄

匿名で小さく始めるデジタル収益化の実用メモを投稿します。note販売、SNS投稿、テンプレート作成の公開前チェックを中心に扱います。

公式サイト: {site_url}

## Google Search Console

プロパティタイプは URLプレフィックス を選び、以下を登録します。

{site_url}

サイトマップURL:

{site_url}sitemap.xml

## A8媒体URL

媒体URLを聞かれたら以下を使います。

{site_url}

媒体紹介文100文字以内:

匿名で小さく始めるnote販売、SNS投稿、テンプレート作成の実用メモを掲載しています。
"""

    out = root_path("dist", "launch_copy.md")
    write_text(out, content)
    return out


if __name__ == "__main__":
    print(generate())
