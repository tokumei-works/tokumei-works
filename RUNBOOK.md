# Runbook

## いま動いているもの

ローカルでは以下の自動生成が完了しています。

- note下書き: `dist/note_drafts/`
- 公開サイト: `site/`
- SNS投稿キュー: `dist/social_queue.csv`
- X共有URL: `dist/x_intents.json`
- Xプロフィール: https://x.com/tokumei_works

再生成する場合:

```powershell
python scripts/run_all.py
```

週次改善パックだけ作る場合:

```powershell
python scripts/generate_growth_pack.py
```

## 本番開始の順番

1. `dist/note_drafts/starter-kit.md` をnoteに貼り付けて有料記事として公開
2. 公開URLを `data/products.json` の `starter-kit.note_url` に入れる
3. `python scripts/run_all.py` を再実行
4. GitHubへpushしてGitHub Pagesを公開
5. 公開URLを `config/brand.json` の `site_url` に入れる
6. `python scripts/run_all.py` を再実行
7. A8.net、もしも、afb、楽天にGitHub Pages URLを媒体登録
8. 提携できた案件だけ `config/affiliate_links.json` に入れる
9. `dist/social_queue.csv` からSNS投稿を予約
10. 週1回、売れたテーマを増補する

## 現在の広告リンク

VideoProc:

```text
https://px.a8.net/svt/ejp?a8mat=4B1U9X+2NUTY2+428G+BX3J6
```

掲載位置はトップページの「制作補助ツール」です。

## X初期設定

プロフィールURL:

```text
https://x.com/tokumei_works
```

プロフィールリンクは、最初は購入まで近いnote記事にします。

```text
https://note.com/tokumei_works/n/nc0c35b105216
```

初回固定ポスト候補:

```text
匿名で小さく始めるnote販売・SNS投稿・デジタル商品作成のテンプレートを作っています。

成果保証ではなく、最初の下書きと公開準備を短くするための実用メモです。

最初の商品はこちら。
https://note.com/tokumei_works/n/nc0c35b105216
```

## GitHub Actionsで全自動化

GitHub Pages公開後は、`.github/workflows/auto-build.yml` が毎日1回動きます。

手動実行:

1. GitHubのリポジトリを開く
2. Actionsタブ
3. `Auto Build Monetization Site`
4. `Run workflow`

定期実行では、サイト、note下書き、SNSキューが再生成されます。

## 自動化の境界

完全自動にできるもの:

- note下書き生成
- 記事下書き生成
- X投稿案生成
- SNS投稿キュー生成
- サイト生成
- A8リンク管理
- 週次改善パック生成

確認が必要なもの:

- note公開
- X投稿
- A8提携申請
- 広告リンクを外部公開サイトへ反映するpush
- 本人確認、銀行、税務、決済に関する入力

週次改善の自動フォローは、毎週月曜9時にこのスレッドで動きます。

## 触るファイル

- 商品を増やす: `data/products.json`
- ブランド名やURLを変える: `config/brand.json`
- 禁止表現を増やす: `config/rules.json`
- ASPリンクを入れる: `config/affiliate_links.json`

## 最初の14日間

- まず `starter-kit` だけ公開する
- Xは1日1から3投稿
- Instagramは週3投稿
- YouTube Shortsは週2本
- 1件売れたら `starter-kit` を増補
- 売れなければタイトルと無料部分を変える
