# 工作教室年間プログラム PDF生成スクリプト
# ソース: R8_工作教室年間プログラム.canvas
# 出力: 20260422_doc_工作教室年間プログラム_final.pdf

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─────────────────────────────────────
# フォント
# ─────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("NS",  os.path.join(FONT_DIR, "NotoSansJP-VF.ttf")))
pdfmetrics.registerFont(TTFont("NSB", os.path.join(FONT_DIR, "BIZ-UDGothicB.ttc")))

# ─────────────────────────────────────
# カラー（センター別・白黒印刷でもグレー差で区別可能）
# ─────────────────────────────────────
C_MIDORI  = HexColor("#D6EAD0")  # 緑ヶ丘（薄緑）
C_MIMAE   = HexColor("#D0E8EA")  # 北松園（薄シアン）
C_AOYAMA  = HexColor("#FFE4CC")  # 青山（薄オレンジ）
C_TAKAMATSU = HexColor("#FADADD")  # 高松（薄赤）
C_KAMINAI = HexColor("#E8D8F0")  # 上米内（薄紫）
C_HEADER  = HexColor("#2B2B2B")  # ヘッダー文字色
C_LINE    = HexColor("#888888")  # 罫線

# ─────────────────────────────────────
# データ（canvasから変換）
# ─────────────────────────────────────

def prog(filename):
    """ファイル名からプログラム名を取得（.md除去）"""
    return filename.replace("工作教室/プログラム/", "").replace(".md", "")

CENTERS = [
    {
        "name": "緑ヶ丘",
        "color": C_MIDORI,
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
        "name": "北松園",
        "color": C_MIMAE,
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
        "name": "青山",
        "color": C_AOYAMA,
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
        "name": "高松\nAグループ",
        "color": C_TAKAMATSU,
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
        "name": "高松\nBグループ",
        "color": C_TAKAMATSU,
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
        "name": "上米内",
        "color": C_KAMINAI,
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
# スタイル
# ─────────────────────────────────────
def styles():
    title_s = ParagraphStyle("title",
        fontName="NSB", fontSize=14, leading=20,
        textColor=C_HEADER, spaceAfter=6*mm)
    center_s = ParagraphStyle("center",
        fontName="NSB", fontSize=9, leading=12,
        textColor=C_HEADER, alignment=TA_CENTER)
    session_s = ParagraphStyle("session",
        fontName="NSB", fontSize=8, leading=10,
        textColor=C_HEADER, alignment=TA_CENTER)
    date_s = ParagraphStyle("date",
        fontName="NS", fontSize=7.5, leading=10,
        textColor=HexColor("#555555"), alignment=TA_CENTER)
    prog_s = ParagraphStyle("prog",
        fontName="NS", fontSize=8, leading=11,
        textColor=black, alignment=TA_CENTER)
    return title_s, center_s, session_s, date_s, prog_s

# ─────────────────────────────────────
# テーブル構築
# ─────────────────────────────────────
def build_center_table(center, session_s, date_s, prog_s, center_s, col_w):
    sessions = center["sessions"]
    n = len(sessions)
    bg = center["color"]

    # ヘッダー行（回数）
    row_session = [Paragraph(s[0], session_s) for s in sessions]
    # 日付行
    row_date    = [Paragraph(s[1][5:], date_s) for s in sessions]  # MM/DD のみ
    # プログラム行
    row_prog    = [Paragraph(s[2], prog_s) for s in sessions]

    # センター名セル（3行スパン）
    name_cell = Paragraph(center["name"], center_s)

    # テーブルデータ：センター名 + 各行
    data = [
        [name_cell] + row_session,
        [""]        + row_date,
        [""]        + row_prog,
    ]

    col_widths = [22*mm] + [col_w] * n

    tbl = Table(data, colWidths=col_widths, rowHeights=[8*mm, 7*mm, 14*mm])

    style = TableStyle([
        # センター名セルを3行マージ
        ("SPAN",       (0, 0), (0, 2)),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        # センター名背景
        ("BACKGROUND", (0, 0), (0, 2), bg),
        # セッション行背景（ごく薄く）
        ("BACKGROUND", (1, 0), (-1, 0), bg),
        # 外枠
        ("BOX",        (0, 0), (-1, -1), 0.8, C_LINE),
        # 縦線（セル間）
        ("INNERGRID",  (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
        # センター名と内容の間の縦線を強調
        ("LINEAFTER",  (0, 0), (0, 2), 1.0, C_LINE),
        # プログラム行上線
        ("LINEABOVE",  (1, 2), (-1, 2), 0.4, C_LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",  (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ])
    tbl.setStyle(style)
    return tbl

# ─────────────────────────────────────
# メイン
# ─────────────────────────────────────
def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=14*mm, rightMargin=14*mm,
        topMargin=16*mm, bottomMargin=14*mm,
    )

    title_s, center_s, session_s, date_s, prog_s = styles()

    # usable width = 210 - 28 = 182mm
    usable_w = 210*mm - 28*mm

    story = []

    # タイトル
    story.append(Paragraph("令和8年度　工作教室年間プログラム", title_s))

    for center in CENTERS:
        n = len(center["sessions"])
        col_w = (usable_w - 22*mm) / n

        tbl = build_center_table(center, session_s, date_s, prog_s, center_s, col_w)
        story.append(tbl)
        story.append(Spacer(1, 4*mm))

    # 備考（canvasのフリーノード）
    note_s = ParagraphStyle("note",
        fontName="NS", fontSize=7.5, leading=12,
        textColor=HexColor("#555555"))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("【メモ】", ParagraphStyle("noteh",
        fontName="NSB", fontSize=8, leading=12, textColor=C_HEADER)))
    notes = [
        "レオレオニから工作へ／動物をつくる／厨川　日程入りの参加カード作る／オリジナルバッグをつくろう／結び方の図解を印刷&ラミ",
        "ゲーム、ロボット、恐竜、車",
        "ビーズ、バッグ、人形、着せ替え、布",
    ]
    for note in notes:
        story.append(Paragraph("・" + note, note_s))

    doc.build(story)
    print(f"PDF生成完了: {output_path}")

# ─────────────────────────────────────
if __name__ == "__main__":
    out_dir = r"D:\toumei.shippo\04_common（共通・横断）\schedule"
    output_path = os.path.join(out_dir, "20260422_doc_工作教室年間プログラム_final.pdf")
    generate_pdf(output_path)
