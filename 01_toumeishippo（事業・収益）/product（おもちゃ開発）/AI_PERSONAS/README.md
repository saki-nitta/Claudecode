# AI_PERSONAS — てもりクラファン専門家チーム

## ファイル一覧

| ファイル名 | 役割 | 使うタイミング |
|---|---|---|
| persona_pm.md | チーフPM（戦略・進捗管理） | 全体計画・スケジュール確認・リスク洗い出し |
| persona_writer.md | ストーリーテラー＆コピーライター | プロジェクト本文・タイトル・リターン説明文の作成 |
| persona_marketer.md | SNS・PRマーケター | SNS投稿計画・ティザー施策・プレスリリース |
| persona_finance.md | 商品企画＆財務FP | 原価計算・リターン価格設計・収益シミュレーション |

## 呼び出し方（Claude Codeの場合）

チャット欄の冒頭に以下のように入力するだけ：

```
@AI_PERSONAS/persona_finance.md このファイルを読み込み、財務担当として振る舞ってください。
```

### 最新情報を持たせる（毎回この3点セットで起動）

```
以下の3つのファイルを読んで、財務担当として振る舞ってください。
1. @AI_PERSONAS/persona_finance.md （人格・ルール）
2. @AI_PERSONAS/context_finance.md （前回の引き継ぎ）
3. Googleドライブ フォルダID: 1XEZwW0dKQ6hF7lXAaa0arc9RXu4pUvNuk の「【AIチーム共有ログ】最新版」（今日の状況）
```

※ PMはpersona_pm / context_pm、ライターはpersona_writer / context_writer、マーケターはpersona_marketer / context_marketerに読み替える。

### 終了時（必ず実行）

会話の最後にこれを送る：
```
今日の引き継ぎメモをcontext_finance.mdの形式で出して
```
→ 出力された内容でcontext_finance.mdを上書き保存する。

## おすすめの使い順

1. **財務（finance）** → 原価・目標金額・リターン価格を先に固める
2. **PM** → スケジュールと全体フェーズを確認
3. **ライター（writer）** → プロジェクト本文・タイトルを執筆
4. **マーケター（marketer）** → 事前告知〜ラストスパートの発信計画を立てる