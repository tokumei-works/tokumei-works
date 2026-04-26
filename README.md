# Anonymous Monetization Kit

匿名・資産ゼロ・月予算1万円以内で、初収益を最短で狙うための自動運用キットです。

最終方針は **note有料ミニ商品を主収益源にし、GitHub Pagesを母艦、X/Instagram/YouTubeは投稿キューで送客補助** です。登録や本人確認だけは本人対応が必要ですが、それ以外の下書き生成、サイト生成、SNS投稿文生成、RSS/sitemap生成、公開前チェックはこのリポジトリで自動化します。

## Quick Start

```powershell
python scripts/run_all.py
```

生成されるもの:

- `site/`: GitHub Pagesで公開する静的サイト
- `dist/note_drafts/`: noteへ貼り付ける有料記事下書き
- `dist/social_queue.csv`: X/Instagram/YouTube Shorts向け投稿キュー
- `dist/x_intents.json`: X共有URLの候補
- `dist/launch_copy.md`: note、X、Instagram、YouTube、Search Console、A8に貼る初期設定文

## What To Register

最初に必要なのは以下です。

1. noteの販売設定と売上受取設定
2. GitHubリポジトリとGitHub Pages
3. ASP登録: A8.net、もしもアフィリエイト、afb、楽天アフィリエイト
4. Google Search Console
5. 必要になったら X API / Meta Business Suite / YouTube Data API

詳細は `LAUNCH_CHECKLIST.md` を見てください。

## Operating Model

1. `data/products.json` に販売するミニ商品を置く
2. `python scripts/run_all.py` で下書き、サイト、投稿キューを生成
3. noteに有料記事を公開し、URLを `data/products.json` に追記
4. GitHub Pagesを公開し、ASPに媒体URLとして登録
5. 投稿キューをSNSに予約投稿または手動投稿
6. 売れた商品を増補し、同テーマの第2版やセット販売へ展開

## Safety

全自動での無差別SNS投稿、DM、フォロー、いいね、コメント、自己購入依頼、誇大広告は避けます。初期は「公開物を自動生成し、人間が登録・投稿・販売設定を行う」運用にして、アカウント停止やASP否認のリスクを抑えます。
