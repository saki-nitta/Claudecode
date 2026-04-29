# 工作教室年間プログラム表（各センター配布用）HTML生成スクリプト
# ブラウザで開いて印刷 → A4 PDF化できる
# CSS変数 --row-padding / --font-size を変更して行間・文字サイズを調整可能

import os

PROG_DIR = r"D:\Obsidian_Sync\リモート保管庫1\工作教室\プログラム"
OUT_DIR  = r"D:\toumei.shippo\04_common（共通・横断）\schedule"

SPECIAL_LABELS = {
    "夏":     "夏休み",
    "冬":     "冬休み",
    "母の日": "母の日",
    "父の日": "父の日",
    "節分":   "節分",
    "お楽しみ": "お楽しみ会",
}

CENTERS = [
    {
        "name": "緑ヶ丘児童センター",
        "short": "緑ヶ丘",
        "sessions": [
            ("第1回",  "2026/05/15", "かんたんポップアップカード"),
            ("第2回",  "2026/06/26", "紙コップで遊ぼう"),
            ("第3回",  "2026/07/10", "あやつりアニマル"),
            ("第4回",  "2026/09/04", "キラキラモビール"),
            ("第5回",  "2026/10/09", "ストローキャッチャー"),
            ("第6回",  "2026/10/23", "飛び出すびっくり箱"),
            ("第7回",  "2026/11/13", "カラフル遊園地"),
            ("第8回",  "2026/12/11", "毛糸でドリームキャッチャー"),
            ("第9回",  "2027/01/22", "へんてこオニの仮面"),
            ("第10回", "2027/02/12", "花かごメッセージスタンド"),
        ],
    },
    {
        "name": "北松園児童センター",
        "short": "北松園",
        "sessions": [
            ("第1回",  "2026/05/22", "かんたんポップアップカード"),
            ("第2回",  "2026/06/19", "紙コップで遊ぼう"),
            ("夏",    "2026/07/30", "はこにわ水族館"),
            ("第3回",  "2026/07/17", "カラフル遊園地①"),
            ("第4回",  "2026/09/18", "カラフル遊園地②"),
            ("第5回",  "2026/10/16", "あやつりアニマル"),
            ("第6回",  "2026/11/20", "キラキラモビール"),
            ("第7回",  "2026/12/18", "ストローキャッチャー"),
            ("冬",    "2026/12/25", "毛糸でドリームキャッチャー"),
            ("第8回",  "2027/02/19", "飛び出すびっくり箱"),
        ],
    },
    {
        "name": "青山児童センター",
        "short": "青山",
        "sessions": [
            ("第1回",  "2026/05/28", "かんたんポップアップカード"),
            ("第2回",  "2026/06/25", "紙コップで遊ぼう"),
            ("第3回",  "2026/07/16", "あやつりアニマル"),
            ("第4回",  "2026/08/27", "カラフル遊園地①"),
            ("第5回",  "2026/09/24", "カラフル遊園地②"),
            ("第6回",  "2026/10/22", "ストローキャッチャー"),
            ("第7回",  "2026/11/26", "カラフル遊園地"),
            ("第8回",  "2026/12/17", "キラキラモビール"),
            ("第9回",  "2026/12/24", "飛び出すびっくり箱"),
            ("第10回", "2027/01/21", "へんてこオニの仮面"),
        ],
    },
    {
        "name": "高松児童センター（Aグループ）",
        "short": "高松A",
        "sessions": [
            ("A1",  "2026/04/23", "かんたんポップアップカード"),
            ("A2",  "2026/06/04", "紙コップで遊ぼう"),
            ("A3",  "2026/07/02", "あやつりアニマル"),
            ("夏",  "2026/07/28", "はこにわ水族館"),
            ("A4",  "2026/09/03", "キラキラモビール"),
            ("A5",  "2026/09/17", "カラフル遊園地①"),
            ("A6",  "2026/10/08", "カラフル遊園地②"),
            ("A7",  "2026/11/05", "ストローキャッチャー"),
            ("A8",  "2026/12/03", "クリスマスツリー"),
            ("A9",  "2027/03/04", "飛び出すびっくり箱"),
        ],
    },
    {
        "name": "高松児童センター（Bグループ）",
        "short": "高松B",
        "sessions": [
            ("B1",  "2026/05/07", "かんたんポップアップカード"),
            ("B2",  "2026/06/18", "紙コップで遊ぼう"),
            ("B3",  "2026/07/09", "あやつりアニマル"),
            ("B4",  "2026/09/10", "キラキラモビール"),
            ("B5",  "2026/10/01", "カラフル遊園地①"),
            ("B6",  "2026/10/15", "カラフル遊園地②"),
            ("B7",  "2026/11/12", "ストローキャッチャー"),
            ("B8",  "2027/02/04", "クリスマスツリー"),
            ("冬",  "2027/01/07", "毛糸でドリームキャッチャー"),
            ("B9",  "2027/03/11", "飛び出すびっくり箱"),
        ],
    },
    {
        "name": "上米内児童センター",
        "short": "上米内",
        "sessions": [
            ("第1回",   "2026/04/17", "かんたんポップアップカード"),
            ("第2回",   "2026/04/24", "紙コップで遊ぼう"),
            ("母の日",  "2026/05/01", "花かごメッセージスタンド"),
            ("第3回",   "2026/05/29", "あやつりアニマル"),
            ("父の日",  "2026/06/12", "ビックリ！カメラ"),
            ("第4回",   "2026/07/24", "はこにわ水族館"),
            ("第5回",   "2026/09/18", "キラキラモビール"),
            ("第6回",   "2026/10/30", "ストローキャッチャー"),
            ("第7回",   "2026/11/20", "カラフル遊園地①"),
            ("第8回",   "2026/12/18", "カラフル遊園地②"),
            ("節分",    "2027/01/29", "へんてこオニの仮面"),
            ("第9回",   "2027/02/19", "飛び出すびっくり箱"),
            ("第10回",  "2027/03/12", "毛糸でドリームキャッチャー"),
            ("お楽しみ","2027/03/19", "オリジナルケーキ"),
            ("第11回",  "2027/03/26", "おらのはたけ"),
        ],
    },
]

TAKAMATSU_TANOSHIMI = [
    ("夏", "2026/07/28", "はこにわ水族館"),
    ("冬", "2027/01/07", "毛糸でドリームキャッチャー"),
]

# ─────────────────────────────────────
def get_zairyou(prog_name):
    path = os.path.join(PROG_DIR, prog_name + ".md")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_zairyou, result = False, []
        for line in lines:
            if line.strip() == "## 材料":
                in_zairyou = True
            elif line.startswith("## ") and in_zairyou:
                break
            elif in_zairyou and line.strip():
                result.append(line.strip())
        return "<br>".join(result)
    except:
        return ""


def get_gaiyou(prog_name):
    path = os.path.join(PROG_DIR, prog_name + ".md")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        in_gaiyou, result = False, []
        for line in lines:
            if line.strip() == "## 概要":
                in_gaiyou = True
            elif line.startswith("## ") and in_gaiyou:
                break
            elif in_gaiyou and line.strip():
                result.append(line.strip())
        return "<br>".join(result)
    except:
        return ""


def get_title(sid, prog):
    label = SPECIAL_LABELS.get(sid)
    escaped = prog.replace("&", "&amp;").replace("<", "&lt;")
    if label:
        return f'<span class="special-label">【{label}】</span>{escaped}'
    return escaped


def find_bikkuri_date(sessions):
    for sid, date, prog in sessions:
        if prog == "飛び出すびっくり箱":
            y, m, d = date.split("/")
            return f"{int(m)}月{int(d)}日"
    return None


def make_html(center_name, sessions, notes_extra=""):
    bikkuri = find_bikkuri_date(sessions)
    notes = [
        "ご用意いただきたい材料は、右端の「必要な材料」欄に記載しています。難しければ無くても構いません。",
        "その他の材料については、材料費の範囲で講師がご用意いたします。",
        "参加者の様子や材料の入手状況等によって、予告なく内容を変更することがございます。",
    ]
    if bikkuri:
        notes.append(
            f"「飛び出すびっくり箱」（{bikkuri}実施）までに、"
            "牛乳パックを参加者お一人につき２本ずつセンターで回収・保管しておいていただけますと大変助かります。"
        )

    notes_html = "\n".join(f"<li>{n}</li>" for n in notes)

    rows_html = ""
    for i, (sid, date, prog) in enumerate(sessions, 1):
        y, m, d = date.split("/")
        date_str = f"{y}年{int(m)}月{int(d)}日"
        title    = get_title(sid, prog)
        gaiyou   = get_gaiyou(prog)
        zairyou  = get_zairyou(prog)
        is_special = sid in SPECIAL_LABELS
        tr_class = "special" if is_special else ("alt" if i % 2 == 0 else "")
        rows_html += f"""
        <tr class="{tr_class}">
          <td class="center">{i}</td>
          <td class="center">{date_str}</td>
          <td class="title">{title}</td>
          <td class="content">{gaiyou}</td>
          <td class="material">{zairyou}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>{center_name} 令和8年度工作教室実施計画</title>
<style>
  /*
   * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   *  ▼ 行間・文字サイズの調整はここで行ってください
   * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   */
  :root {{
    --font-size:    9pt;      /* 全体の文字サイズ */
    --content-font: 8.5pt;   /* 内容欄の文字サイズ */
    --row-padding:  5px;      /* 行の上下余白（行間の調整） */
    --line-height:  1.45;    /* 行内の行間 */
  }}
  /* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */

  @page {{ size: A4 portrait; margin: 13mm; }}
  @media print {{
    body {{ margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .no-print {{ display: none; }}
  }}

  body {{
    font-family: "BIZ UDGothic", "Noto Sans JP", "Yu Gothic", sans-serif;
    font-size: var(--font-size);
    line-height: var(--line-height);
    color: #2b2b2b;
    margin: 0;
    padding: 13mm;
    box-sizing: border-box;
    max-width: 210mm;
  }}

  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1.5px solid #888;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }}
  .header-left h1 {{
    font-size: 13pt;
    font-weight: bold;
    margin: 0 0 2px 0;
  }}
  .header-left h2 {{
    font-size: 10pt;
    font-weight: bold;
    margin: 0;
  }}
  .header-right {{
    text-align: right;
    font-size: 8pt;
    line-height: 1.6;
  }}
  .header-right .lecturer {{
    font-weight: bold;
    font-size: 9pt;
  }}

  ul.notes {{
    margin: 0 0 6px 0;
    padding-left: 1.4em;
    font-size: 7.5pt;
    color: #555;
    line-height: 1.5;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
  }}
  col.col-num     {{ width: 6%; }}
  col.col-date    {{ width: 13%; }}
  col.col-title   {{ width: 24%; }}
  col.col-content {{ width: 44%; }}
  col.col-mat     {{ width: 13%; }}

  th {{
    background: #3a3a3a;
    color: white;
    font-size: var(--font-size);
    font-weight: bold;
    text-align: center;
    padding: var(--row-padding) 4px;
    border: 1px solid #aaa;
  }}
  td {{
    border: 1px solid #ccc;
    padding: var(--row-padding) 4px;
    vertical-align: middle;
    font-size: var(--font-size);
    line-height: var(--line-height);
    word-break: break-all;
  }}
  td.content {{
    font-size: var(--content-font);
  }}
  td.center {{ text-align: center; }}
  td.title  {{ font-weight: bold; }}

  tr.alt     {{ background: #f7f7f7; }}
  tr.special {{ background: #fff3cd; }}

  .special-label {{
    font-weight: bold;
    color: #7a5c00;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <h1>{center_name}　様</h1>
    <h2>令和８年度　工作教室　実施計画</h2>
  </div>
  <div class="header-right">
    <div class="lecturer">講師　新田紗希</div>
    <div>毎回ご用意いただきたいもの</div>
    <div>人数分：はさみ、のり、セロハンテープ</div>
    <div>あれば：カラーペン、色画用紙の端材</div>
  </div>
</div>

<ul class="notes">
{notes_html}
</ul>

<table>
  <colgroup>
    <col class="col-num">
    <col class="col-date">
    <col class="col-title">
    <col class="col-content">
    <col class="col-mat">
  </colgroup>
  <thead>
    <tr>
      <th>回数</th>
      <th>実施日</th>
      <th>タイトル</th>
      <th>内容</th>
      <th>材料</th>
    </tr>
  </thead>
  <tbody>{rows_html}
  </tbody>
</table>

</body>
</html>
"""


def make_takamatsu_combined_html():
    a_sessions = next(c for c in CENTERS if c["short"] == "高松A")["sessions"]
    b_sessions = next(c for c in CENTERS if c["short"] == "高松B")["sessions"]

    raw = []
    for sid, date, prog in a_sessions:
        group = "お楽しみ" if sid == "夏" else "A"
        raw.append((date, group, sid, prog))
    for sid, date, prog in b_sessions:
        group = "お楽しみ" if sid == "冬" else "B"
        raw.append((date, group, sid, prog))
    existing_dates = {r[0] for r in raw if r[1] == "お楽しみ"}
    for sid, date, prog in TAKAMATSU_TANOSHIMI:
        if date not in existing_dates:
            raw.append((date, "お楽しみ", sid, prog))
    raw.sort(key=lambda x: x[0])

    bikkuri_rows = [(d, g, s, p) for d, g, s, p in raw if p == "飛び出すびっくり箱" and g != "お楽しみ"]
    bikkuri_note = ""
    if bikkuri_rows:
        dates_str = "・".join(
            f"{g}グループ {int(d.split('/')[1])}月{int(d.split('/')[2])}日"
            for d, g, s, p in bikkuri_rows
        )
        bikkuri_note = (
            f"「飛び出すびっくり箱」（{dates_str}実施）までに、"
            "牛乳パックを参加者お一人につき２本ずつセンターで回収・保管しておいていただけますと大変助かります。"
        )

    notes = [
        "ご用意いただきたい材料は、右端の「必要な材料」欄に記載しています。難しければ無くても構いません。",
        "その他の材料については、材料費の範囲で講師がご用意いたします。",
        "参加者の様子や材料の入手状況等によって、予告なく内容を変更することがございます。",
    ]
    if bikkuri_note:
        notes.append(bikkuri_note)
    notes_html = "\n".join(f"<li>{n}</li>" for n in notes)

    GROUP_BG = {"A": "#eaf4ea", "B": "#eaf0fa", "お楽しみ": "#fff3cd"}

    rows_html = ""
    for i, (date, group, sid, prog) in enumerate(raw, 1):
        y, m, d = date.split("/")
        date_str = f"{y}年{int(m)}月{int(d)}日"
        title    = get_title(sid, prog)
        gaiyou   = get_gaiyou(prog)
        zairyou  = get_zairyou(prog)
        bg       = GROUP_BG.get(group, "")
        rows_html += f"""
        <tr style="background:{bg}">
          <td class="center">{group}</td>
          <td class="center">{sid}</td>
          <td class="center">{date_str}</td>
          <td class="title">{title}</td>
          <td class="content">{gaiyou}</td>
          <td class="material">{zairyou}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>高松児童センター 令和8年度工作教室実施計画（合同）</title>
<style>
  :root {{
    --font-size:    8.5pt;
    --content-font: 8pt;
    --row-padding:  4px;
    --line-height:  1.4;
  }}
  @page {{ size: A4 portrait; margin: 13mm; }}
  @media print {{
    body {{ margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  }}
  body {{
    font-family: "BIZ UDGothic", "Noto Sans JP", "Yu Gothic", sans-serif;
    font-size: var(--font-size);
    line-height: var(--line-height);
    color: #2b2b2b;
    margin: 0;
    padding: 13mm;
    box-sizing: border-box;
    max-width: 210mm;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1.5px solid #888;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }}
  .header-left h1 {{ font-size: 13pt; font-weight: bold; margin: 0 0 2px 0; }}
  .header-left h2 {{ font-size: 9.5pt; font-weight: bold; margin: 0; }}
  .header-right {{ text-align: right; font-size: 8pt; line-height: 1.6; }}
  .header-right .lecturer {{ font-weight: bold; font-size: 9pt; }}
  ul.notes {{
    margin: 0 0 4px 0;
    padding-left: 1.4em;
    font-size: 7pt;
    color: #555;
    line-height: 1.45;
  }}
  .legend {{ font-size: 7.5pt; color: #555; margin-bottom: 4px; }}
  table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
  col.col-grp   {{ width: 8%; }}
  col.col-num   {{ width: 7%; }}
  col.col-date  {{ width: 13%; }}
  col.col-title {{ width: 23%; }}
  col.col-cont  {{ width: 38%; }}
  col.col-mat   {{ width: 11%; }}
  th {{
    background: #3a3a3a; color: white;
    font-size: var(--font-size); font-weight: bold;
    text-align: center;
    padding: var(--row-padding) 3px;
    border: 1px solid #aaa;
  }}
  td {{
    border: 1px solid #ccc;
    padding: var(--row-padding) 3px;
    vertical-align: middle;
    font-size: var(--font-size);
    line-height: var(--line-height);
    word-break: break-all;
  }}
  td.content {{ font-size: var(--content-font); }}
  td.center {{ text-align: center; }}
  td.title  {{ font-weight: bold; }}
  .special-label {{ font-weight: bold; color: #7a5c00; }}
</style>
</head>
<body>
<div class="header">
  <div class="header-left">
    <h1>高松児童センター　様</h1>
    <h2>令和８年度　工作教室　実施計画（A・B・お楽しみ工作 合同一覧）</h2>
  </div>
  <div class="header-right">
    <div class="lecturer">講師　新田紗希</div>
    <div>毎回ご用意いただきたいもの</div>
    <div>人数分：はさみ、のり、セロハンテープ</div>
    <div>あれば：カラーペン、色画用紙の端材</div>
  </div>
</div>
<ul class="notes">
{notes_html}
</ul>
<p class="legend">■ Aグループ（緑）　■ Bグループ（青）　■ お楽しみ工作（黄）</p>
<table>
  <colgroup>
    <col class="col-grp"><col class="col-num"><col class="col-date">
    <col class="col-title"><col class="col-cont"><col class="col-mat">
  </colgroup>
  <thead>
    <tr>
      <th>グループ</th><th>回数</th><th>実施日</th>
      <th>タイトル</th><th>内容</th><th>必要な材料<br>（一人１つ）</th>
    </tr>
  </thead>
  <tbody>{rows_html}
  </tbody>
</table>
</body>
</html>
"""


# ─────────────────────────────────────
if __name__ == "__main__":
    SKIP = {"高松A", "高松B"}
    for center in CENTERS:
        if center["short"] in SKIP:
            print(f"スキップ: {center['short']}")
            continue
        html = make_html(center["name"], center["sessions"])
        out  = os.path.join(OUT_DIR, f"20260422_doc_工作教室プログラム表_{center['short']}.html")
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"生成完了: {out}")

    html_combined = make_takamatsu_combined_html()
    out_combined  = os.path.join(OUT_DIR, "20260422_doc_工作教室プログラム表_高松合同.html")
    with open(out_combined, 'w', encoding='utf-8') as f:
        f.write(html_combined)
    print(f"生成完了: {out_combined}")
