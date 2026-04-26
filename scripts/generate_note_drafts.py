from __future__ import annotations

from pathlib import Path
from typing import Any

from utils import load_json, root_path, write_text


def starter_paid_body() -> str:
    return """## 1. ペンネーム設計シート

以下を埋めるだけで、匿名運用の軸ができます。

```text
ペンネーム:
扱うテーマ:
扱わないテーマ:
読者の悩み:
提供するもの:
投稿の口調:
販売する初回商品:
```

## 2. 最初の商品ページ構成

```text
タイトル:
誰向けか:
この商品で解決すること:
無料部分で見せる価値:
有料部分に入れるテンプレート:
価格:
購入前の注意:
```

## 3. 7日分の投稿カレンダー

| Day | 投稿テーマ | 目的 |
|---:|---|---|
| 1 | 匿名で始める理由 | 共感を作る |
| 2 | 最初に決める5項目 | 保存される投稿 |
| 3 | やらないことリスト | 信頼を作る |
| 4 | 商品作成の裏側 | 制作過程を見せる |
| 5 | 無料テンプレの一部 | 体験してもらう |
| 6 | よくある不安への回答 | 購入前の迷いを減らす |
| 7 | 商品案内 | 販売導線を置く |

## 4. 公開前チェックリスト

- PR/広告/有料コンテンツの表示がある
- 実績を盛っていない
- 未確認の数字を書いていない
- 返金や成果を誤認させない
- リンク先が正しい
- 無料部分だけでも役に立つ
"""


def social_paid_body() -> str:
    rows = []
    angles = [
        "始める前に決めること",
        "投稿が続かない理由",
        "売り込み感を下げる方法",
        "無料部分の見せ方",
        "有料導線の置き方",
        "匿名プロフィールの作り方",
        "避けるべき表現",
        "小さな商品を作る手順",
        "1投稿1メッセージの原則",
        "反応が出た投稿の再利用",
    ]
    for day in range(1, 31):
        angle = angles[(day - 1) % len(angles)]
        rows.append(
            f"| {day} | {angle} | X短文、Instagram見出し、Shorts台本に転用 |"
        )

    return f"""## 1. 30日分の投稿テーマ

| Day | テーマ | 使い方 |
|---:|---|---|
{chr(10).join(rows)}

## 2. X投稿の型

```text
匿名で始めるなら、最初に決めるのは「何を売るか」より「何を売らないか」です。
扱わないテーマを決めると、投稿も商品も作りやすくなります。
```

```text
有料noteは、無料部分を薄くすると逆に売れにくいです。
無料部分で「この人は整理してくれる」と伝わるほど、有料部分への期待値が上がります。
```

```text
今日のチェック:
・プロフィールに販売導線がある
・投稿に1つだけ行動先がある
・誇大表現がない
・リンク先がスマホで読める
```

## 3. Instagramカルーセル見出し

```text
1枚目: 匿名で収益化する前に決める5項目
2枚目: 名前より先に決めるもの
3枚目: 扱うテーマ
4枚目: 扱わないテーマ
5枚目: 最初の商品
6枚目: 投稿頻度
7枚目: 今日やること
```

## 4. Shorts台本

```text
冒頭: 匿名で副業を始めるなら、まず商品を作る前にこれを決めてください。
本編: 1つ目は扱うテーマ。2つ目は扱わないテーマ。3つ目は最初に売る小さなテンプレートです。
締め: 大きく始めるより、小さく売って反応を見ます。
```
"""


def paid_note_body() -> str:
    return """## 1. 500円商品の構成テンプレート

```text
# タイトル
誰向けか:
このnoteでできること:
無料部分で渡すもの:
有料部分で渡すもの:
購入前の注意:
```

## 2. 980円商品の構成テンプレート

```text
# タイトル
悩みの具体例:
この商品が合う人:
この商品が合わない人:
無料部分:
有料部分:
テンプレート:
チェックリスト:
追加特典:
```

## 3. 有料ライン前の文例

```text
ここまでで全体像はつかめます。
ここから先は、実際にそのまま使えるテンプレート、チェックリスト、記入例をまとめています。
```

## 4. 追記・改訂のお知らせ文

```text
追記: 反応が多かった項目を増補しました。購入済みの方は追加料金なしで読めます。
```

## 5. 期待値調整の文例

```text
このnoteは成果を保証するものではありません。最初の下書き作成と公開準備を短くするためのテンプレート集です。
```
"""


def paid_body_for(slug: str) -> str:
    if slug == "starter-kit":
        return starter_paid_body()
    if slug == "social-30":
        return social_paid_body()
    return paid_note_body()


def build_note_draft(product: dict[str, Any], brand: dict[str, Any], rules: dict[str, Any]) -> str:
    free_list = "\n".join(f"- {item}" for item in product["free_value"])
    paid_list = "\n".join(f"- {item}" for item in product["paid_value"])

    return f"""# {product['title']}

{rules['required_disclosure']}

{product['summary']}

## このnoteが合う人

{product['audience']}

## 無料部分で持ち帰れること

{free_list}

## まず決めること

最初から大きな仕組みを作ろうとすると、手が止まりやすくなります。まずは小さな商品を1つ置き、投稿から販売ページへ流す導線を作ります。

このnoteでは、匿名でも使いやすい言い回し、販売前のチェック、投稿への転用を前提にしています。

## 注意

この内容は成果を保証するものではありません。販売ページや投稿文を作る時間を短くし、最初の検証を始めやすくするためのテンプレートです。

<!-- note-paid-line -->

# 有料部分

ここから先は、実際に使うためのテンプレートと記入例です。

## 入っているもの

{paid_list}

{paid_body_for(product['slug'])}

## 次にやること

1. このnoteのテンプレートを自分のテーマに置き換える
2. 無料部分と有料部分を分ける
3. 価格を {product['price_yen']} 円前後に設定する
4. X、Instagram、YouTube Shorts向けに1週間分だけ告知を作る
5. 反応があった投稿だけ増やす

{product['cta']}

---

発行: {brand['name']}
"""


def generate() -> list[Path]:
    brand = load_json("config", "brand.json")
    rules = load_json("config", "rules.json")
    products = load_json("data", "products.json")
    out_dir = root_path("dist", "note_drafts")
    written: list[Path] = []
    for product in products:
        path = out_dir / f"{product['slug']}.md"
        write_text(path, build_note_draft(product, brand, rules))
        written.append(path)
    return written


if __name__ == "__main__":
    for draft in generate():
        print(draft)

