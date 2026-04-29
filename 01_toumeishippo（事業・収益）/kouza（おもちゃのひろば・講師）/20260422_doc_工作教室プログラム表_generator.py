# 工作教室年間プログラム表（各センター配布用）生成スクリプト
# 出力: 20260422_doc_工作教室プログラム表_<センター名>.pdf

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ─────────────────────────────────────
# フォント
# ─────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("NS",  os.path.join(FONT_DIR, "NotoSansJP-VF.ttf")))
pdfmetrics.registerFont(TTFont("NSB", os.path.join(FONT_DIR, "BIZ-UDGothicB.ttc")))

# ─────────────────────────────────────
# 定数
# ─────────────────────────────────────
PROG_DIR = r"D:\Obsidian_Sync\リモート保管庫1\工作教室\プログラム"
OUT_DIR  = r"D:\toumei.shippo\04_common（共通・横断）\schedule"

C_HEADER  = HexColor("#2B2B2B")
C_LINE    = HexColor("#AAAAAA")
C_TH_BG   = HexColor("#3A3A3A")
C_ROW_ALT = HexColor("#F7F7F7")
C_ACCENT  = HexColor("#D6EAD0")

SPECIAL_LABELS = {
    "夏":     "夏休み",
    "冬":     "冬休み",
    "母の日": "母の日",
    "父の日": "父の日",
    "節分":   "節分",
    "お楽しみ": "お楽しみ会",
}

# ─────────────────────────────────────
# セッションデータ
# ─────────────────────────────────────
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

# ─────────────────────────────────────
# ヘルパー
# ─────────────────────────────────────
def get_gaiyou(prog_name):
    """プログラムの概要をmdファイルから取得"""
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
        return "\n".join(result)
    except:
        return ""


def get_session_title(session_id, prog_name):
    """特別回は【ラベル】を付ける"""
    label = SPECIAL_LABELS.get(session_id)
    return f"【{label}】{prog_name}" if label else prog_name


def find_bikkuri_date(sessions):
    """飛び出すびっくり箱の実施日を取得"""
    for sid, date, prog in sessions:
        if prog == "飛び出すびっくり箱":
            y, m, d = date.split("/")
            return f"{int(m)}月{int(d)}日"
    return None

# ─────────────────────────────────────
# スタイル
# ─────────────────────────────────────
def make_styles(n_sessions=10):
    """セッション数に応じてテーブル本文フォントを調整"""
    if n_sessions <= 10:
        fs, ld = 8.0, 11
    elif n_sessions <= 13:
        fs, ld = 7.5, 10
    else:
        fs, ld = 7.0, 10

    center_title_s = ParagraphStyle("ct",
        fontName="NSB", fontSize=13, leading=18, textColor=C_HEADER)
    year_s = ParagraphStyle("yr",
        fontName="NSB", fontSize=10, leading=14, textColor=C_HEADER)
    label_s = ParagraphStyle("lb",
        fontName="NSB", fontSize=8, leading=11, textColor=C_HEADER)
    body_s = ParagraphStyle("bd",
        fontName="NS", fontSize=8, leading=11, textColor=C_HEADER)
    note_s = ParagraphStyle("nt",
        fontName="NS", fontSize=7.5, leading=11, textColor=HexColor("#555555"))
    th_s = ParagraphStyle("th",
        fontName="NSB", fontSize=fs, leading=ld,
        textColor=white, alignment=TA_CENTER)
    td_num_s = ParagraphStyle("tn",
        fontName="NSB", fontSize=fs, leading=ld,
        textColor=C_HEADER, alignment=TA_CENTER)
    td_date_s = ParagraphStyle("td",
        fontName="NS", fontSize=fs, leading=ld,
        textColor=HexColor("#444444"), alignment=TA_CENTER)
    td_title_s = ParagraphStyle("tt",
        fontName="NSB", fontSize=fs, leading=ld, textColor=C_HEADER)
    td_body_s = ParagraphStyle("tb",
        fontName="NS", fontSize=fs - 0.5, leading=ld, textColor=C_HEADER)
    return center_title_s, year_s, label_s, body_s, note_s, th_s, td_num_s, td_date_s, td_title_s, td_body_s

# ─────────────────────────────────────
# PDF生成
# ─────────────────────────────────────
def generate_pdf(center, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=13*mm, rightMargin=13*mm,
        topMargin=13*mm, bottomMargin=13*mm,
    )

    n_sessions = len(center["sessions"])
    (center_title_s, year_s, label_s, body_s, note_s,
     th_s, td_num_s, td_date_s, td_title_s, td_body_s) = make_styles(n_sessions)

    usable_w = 210*mm - 26*mm  # 184mm

    story = []

    # ── ヘッダー（2カラム） ──
    header_left = [
        [Paragraph(center["name"] + "　様", center_title_s)],
        [Paragraph("令和８年度　工作教室　実施計画", year_s)],
    ]
    header_right = [
        [Paragraph("講師　新田紗希", label_s),
         Paragraph("おもちゃコンサルタント／公認心理師", body_s)],
        [Paragraph("毎回ご用意いただきたいもの", label_s), None],
        [Paragraph("人数分：はさみ、のり、セロハンテープ", body_s), None],
        [Paragraph("あれば：カラーペン、色画用紙の端材", body_s), None],
    ]

    header_tbl = Table(
        [
            [
                Table(header_left, colWidths=[105*mm]),
                Table(header_right, colWidths=[62*mm, 17*mm]),
            ]
        ],
        colWidths=[105*mm, 79*mm],
    )
    header_tbl.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, C_LINE),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 3*mm))

    # ── 注意書き ──
    bikkuri_date = find_bikkuri_date(center["sessions"])
    notes = [
        "ご用意いただきたい材料は、右端の「必要な材料」欄に記載しています。ご準備いただければ助かりますが、難しければ無くても構いません。",
        "その他の材料については、材料費の範囲で講師がご用意いたします。",
        "参加者の様子や材料の入手状況等によって、予告なく内容を変更することがございます。",
    ]
    if bikkuri_date:
        notes.append(
            f"「飛び出すびっくり箱」（{bikkuri_date}実施）までに、牛乳パックを参加者お一人につき２本ずつ"
            "センターで回収・保管しておいていただけますと大変助かります。"
        )

    for n in notes:
        story.append(Paragraph("・" + n, note_s))
    story.append(Spacer(1, 3*mm))

    # ── テーブル ──
    # 列幅: 回数12 / 日付24 / タイトル46 / 内容82 / 必要な材料20 = 184mm
    COL_W = [12*mm, 24*mm, 46*mm, 82*mm, 20*mm]

    # ヘッダー行
    rows = [[
        Paragraph("回数",     th_s),
        Paragraph("実施日",   th_s),
        Paragraph("タイトル", th_s),
        Paragraph("内容",     th_s),
        Paragraph("必要な材料\n（一人１つ）", th_s),
    ]]

    for i, (sid, date, prog) in enumerate(center["sessions"], 1):
        y, m, d = date.split("/")
        date_str = f"{y}年{int(m)}月{int(d)}日"
        title    = get_session_title(sid, prog)
        gaiyou   = get_gaiyou(prog)

        rows.append([
            Paragraph(str(i), td_num_s),
            Paragraph(date_str, td_date_s),
            Paragraph(title, td_title_s),
            Paragraph(gaiyou, td_body_s),
            Paragraph("", td_body_s),
        ])

    tbl = Table(rows, colWidths=COL_W, repeatRows=1)

    # 交互背景
    style_cmds = [
        ("BACKGROUND",  (0, 0), (-1, 0),  C_TH_BG),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  white),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",       (0, 0), (1, -1),  "CENTER"),
        ("BOX",         (0, 0), (-1, -1), 0.8, C_LINE),
        ("INNERGRID",   (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
        ("TOPPADDING",  (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0,0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",(0, 0), (-1, -1), 3),
    ]
    # 特別回に薄い背景
    for i, (sid, date, prog) in enumerate(center["sessions"], 1):
        if sid in SPECIAL_LABELS:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), HexColor("#FFF3CD")))
        elif i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), C_ROW_ALT))

    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)

    doc.build(story)
    print(f"生成完了: {output_path}")


# ─────────────────────────────────────
# 高松合同表（A・B・お楽しみ工作を日付順）
# ─────────────────────────────────────
TAKAMATSU_TANOSHIMI = [
    ("夏", "2026/07/28", "はこにわ水族館"),
    ("冬", "2027/01/07", "毛糸でドリームキャッチャー"),
]

GROUP_COLORS = {
    "A":      HexColor("#EAF4EA"),
    "B":      HexColor("#EAF0FA"),
    "お楽しみ": HexColor("#FFF3CD"),
}

def generate_takamatsu_combined(output_path):
    """高松A・B・お楽しみ工作を日付順にまとめた合同表を生成"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=13*mm, rightMargin=13*mm,
        topMargin=13*mm, bottomMargin=13*mm,
    )

    (center_title_s, year_s, label_s, body_s, note_s,
     th_s, td_num_s, td_date_s, td_title_s, td_body_s) = make_styles()

    # A・B・お楽しみを統合
    raw = []
    a_sessions = next(c for c in CENTERS if c["short"] == "高松A")["sessions"]
    b_sessions = next(c for c in CENTERS if c["short"] == "高松B")["sessions"]

    for sid, date, prog in a_sessions:
        group = "お楽しみ" if sid == "夏" else "A"
        raw.append((date, group, sid, prog))
    for sid, date, prog in b_sessions:
        group = "お楽しみ" if sid == "冬" else "B"
        raw.append((date, group, sid, prog))
    # お楽しみ工作の夏・冬（A/Bに含まれていない場合の保険）
    existing_dates = {r[0] for r in raw if r[1] == "お楽しみ"}
    for sid, date, prog in TAKAMATSU_TANOSHIMI:
        if date not in existing_dates:
            raw.append((date, "お楽しみ", sid, prog))

    # 日付順ソート
    raw.sort(key=lambda x: x[0])

    story = []

    # ヘッダー
    header_left = [
        [Paragraph("高松児童センター　様", center_title_s)],
        [Paragraph("令和８年度　工作教室　実施計画　（A・B・お楽しみ工作 合同一覧）", year_s)],
    ]
    header_right = [
        [Paragraph("講師　新田紗希", label_s),
         Paragraph("おもちゃコンサルタント／公認心理師", body_s)],
        [Paragraph("毎回ご用意いただきたいもの", label_s), None],
        [Paragraph("人数分：はさみ、のり、セロハンテープ", body_s), None],
        [Paragraph("あれば：カラーペン、色画用紙の端材", body_s), None],
    ]
    header_tbl = Table(
        [[Table(header_left, colWidths=[105*mm]),
          Table(header_right, colWidths=[62*mm, 17*mm])]],
        colWidths=[105*mm, 79*mm],
    )
    header_tbl.setStyle(TableStyle([
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0),  1.0, C_LINE),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 3*mm))

    # 注意書き
    bikkuri_rows = [(d, g, s, p) for d, g, s, p in raw if p == "飛び出すびっくり箱"]
    bikkuri_note = ""
    if bikkuri_rows:
        dates_str = "・".join(
            f"{g}グループ {int(d.split('/')[1])}月{int(d.split('/')[2])}日"
            for d, g, s, p in bikkuri_rows if g != "お楽しみ"
        )
        bikkuri_note = f"「飛び出すびっくり箱」（{dates_str}実施）までに、牛乳パックを参加者お一人につき２本ずつセンターで回収・保管しておいていただけますと大変助かります。"

    notes = [
        "ご用意いただきたい材料は、右端の「必要な材料」欄に記載しています。難しければ無くても構いません。",
        "その他の材料については、材料費の範囲で講師がご用意いたします。",
        "参加者の様子や材料の入手状況等によって、予告なく内容を変更することがございます。",
    ]
    if bikkuri_note:
        notes.append(bikkuri_note)
    for n in notes:
        story.append(Paragraph("・" + n, note_s))

    # グループ凡例
    legend_s = ParagraphStyle("leg", fontName="NS", fontSize=7.5, leading=11,
                               textColor=HexColor("#555555"))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "　■ Aグループ（緑）　■ Bグループ（青）　■ お楽しみ工作（黄）", legend_s))
    story.append(Spacer(1, 2*mm))

    # テーブル
    # 列幅: グループ12 / 回数12 / 日付26 / タイトル44 / 内容70 / 必要な材料20 = 184mm
    COL_W = [12*mm, 12*mm, 26*mm, 44*mm, 70*mm, 20*mm]

    rows = [[
        Paragraph("グループ", th_s),
        Paragraph("回数",     th_s),
        Paragraph("実施日",   th_s),
        Paragraph("タイトル", th_s),
        Paragraph("内容",     th_s),
        Paragraph("必要な材料\n（一人１つ）", th_s),
    ]]

    for i, (date, group, sid, prog) in enumerate(raw, 1):
        y, m, d = date.split("/")
        date_str = f"{y}年{int(m)}月{int(d)}日"
        title    = get_session_title(sid, prog)
        gaiyou   = get_gaiyou(prog)
        rows.append([
            Paragraph(group,    td_num_s),
            Paragraph(sid,      td_num_s),
            Paragraph(date_str, td_date_s),
            Paragraph(title,    td_title_s),
            Paragraph(gaiyou,   td_body_s),
            Paragraph("",       td_body_s),
        ])

    tbl = Table(rows, colWidths=COL_W, repeatRows=1)

    style_cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0),  C_TH_BG),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",        (0, 0), (2, -1),  "CENTER"),
        ("BOX",          (0, 0), (-1, -1), 0.8, C_LINE),
        ("INNERGRID",    (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
        ("TOPPADDING",   (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 2),
        ("LEFTPADDING",  (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]
    for i, (date, group, sid, prog) in enumerate(raw, 1):
        bg = GROUP_COLORS.get(group, C_ROW_ALT)
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)

    doc.build(story)
    print(f"生成完了: {output_path}")


# ─────────────────────────────────────
if __name__ == "__main__":
    for center in CENTERS:
        filename = f"20260422_doc_工作教室プログラム表_{center['short']}.pdf"
        out = os.path.join(OUT_DIR, filename)
        generate_pdf(center, out)

    out_combined = os.path.join(OUT_DIR, "20260422_doc_工作教室プログラム表_高松合同.pdf")
    generate_takamatsu_combined(out_combined)
