# Launch Checklist

登録・本人確認は本人対応が必要です。ここだけ進めれば、自動生成キットを本番運用に入れられます。

## 1. note

- [ ] ペンネーム、プロフィール、アイコンを整える
- [ ] 売上受取用の銀行口座を登録する
- [ ] `dist/note_drafts/` の3本をnoteに貼り付ける
- [ ] 有料ラインを `<!-- note-paid-line -->` の位置に置く
- [ ] 価格を最初は `500円` または `980円` にする
- [ ] 公開後のURLを `data/products.json` の `note_url` に入れる

## 2. GitHub Pages

- [ ] GitHubに新規リポジトリを作る
- [ ] このフォルダをpushする
- [ ] Settings > Pages > Source を `GitHub Actions` にする
- [ ] Actionsで `Auto Build Monetization Site` を手動実行する
- [ ] 公開URLを `config/brand.json` の `site_url` に入れる

## 3. ASP

最初は以下を登録します。

- [ ] A8.net
- [ ] もしもアフィリエイト
- [ ] afb
- [ ] 楽天アフィリエイト

登録時の媒体URLは、GitHub Pagesの公開URLを使います。SNSだけで登録できる場合もありますが、母艦サイトを登録しておくほうが案件審査で説明しやすいです。

## 4. ASPリンク設定

- [ ] 提携できた案件だけ `config/affiliate_links.json` に入れる
- [ ] 案件ごとのSNS掲載可否を確認する
- [ ] 本人申込可否を確認する
- [ ] リスティング禁止語、商標利用禁止を確認する
- [ ] 商品画像・価格表示の許可範囲を確認する

## 5. SNS

初期はAPI自動投稿ではなく、投稿キューを使います。

- [ ] XプロフィールにGitHub PagesまたはnoteプロフィールURLを置く
- [ ] XプロフィールURL: `https://x.com/tokumei_works`
- [ ] 最初はnote記事URLをプロフィールに置く
- [ ] Instagramを必要ならプロアカウントへ切り替える
- [ ] YouTube Shorts用にチャンネル概要へリンクを置く
- [ ] `dist/social_queue.csv` を見て投稿する

## 6. 計測

- [ ] Google Search ConsoleにGitHub Pagesを登録する
- [ ] 必要なら Google Analytics ID を `config/brand.json` に入れる
- [ ] noteのビュー、スキ、購入、SNS反応を週1回記録する

## 7. 予算配分

- 0円から開始
- 必要なら素材/デザインに月1,000円から2,000円
- AI APIを使う場合は月3,000円上限
- 広告は初回販売が出るまで使わない
- X APIやSNS自動投稿ツールは、販売導線が当たってから検討
