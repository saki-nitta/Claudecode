# 東北地区里親研修会 岩手大会　工作教室 制作内容・予算ご提案 PDF生成スクリプト
# 宛先: 岩手県里親会事務局 川崎舞美様
# 出力: 20260619_doc_里親大会工作内容予算提案_draft_v1.pdf

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# ─────────────────────────────────────
# フォント
# ─────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("NS",  os.path.join(FONT_DIR, "NotoSansJP-VF.ttf")))
pdfmetrics.registerFont(TTFont("NSB", os.path.join(FONT_DIR, "BIZ-UDGothicB.ttc")))

# ─────────────────────────────────────
# 配色
# ─────────────────────────────────────
C_HEADER  = HexColor("#2B2B2B")
C_LINE    = HexColor("#AAAAAA")
C_TH_BG   = HexColor("#3A3A3A")
C_ROW_ALT = HexColor("#F7F7F7")

OUT_DIR   = r"D:\toumei.shippo\01_toumeishippo（事業・収益）\kouza（おもちゃのひろば・講師）"
ASSET_DIR = os.path.join(OUT_DIR, "assets")

# ─────────────────────────────────────
# スタイル
# ─────────────────────────────────────
title_s = ParagraphStyle("title", fontName="NSB", fontSize=15, leading=20, textColor=C_HEADER)
sub_s   = ParagraphStyle("sub",   fontName="NS",  fontSize=9.5, leading=13, textColor=HexColor("#555555"))
label_s = ParagraphStyle("lb",    fontName="NSB", fontSize=8.5, leading=12, textColor=C_HEADER)
addr_s  = ParagraphStyle("ad",    fontName="NS",  fontSize=8.5, leading=12, textColor=C_HEADER, alignment=TA_CENTER)
heading_s = ParagraphStyle("hd",  fontName="NSB", fontSize=12, leading=16, textColor=C_HEADER, spaceAfter=2)
body_s  = ParagraphStyle("bd",    fontName="NS",  fontSize=9.5, leading=14, textColor=C_HEADER)
bullet_s = ParagraphStyle("bl",   fontName="NS",  fontSize=9.5, leading=14, textColor=C_HEADER, leftIndent=2*mm)
note_s  = ParagraphStyle("nt",    fontName="NS",  fontSize=8, leading=11, textColor=HexColor("#777777"))
photo_caption_s = ParagraphStyle("pc", fontName="NS", fontSize=8, leading=11,
                                  textColor=HexColor("#555555"), alignment=TA_CENTER)

th_s    = ParagraphStyle("th", fontName="NSB", fontSize=9, leading=12, textColor=white, alignment=TA_CENTER)
td_c_s  = ParagraphStyle("tc", fontName="NSB", fontSize=9, leading=13, textColor=C_HEADER, alignment=TA_CENTER)
td_b_s  = ParagraphStyle("tb", fontName="NS",  fontSize=9, leading=13, textColor=C_HEADER)


def heading(text):
    return [Paragraph(text, heading_s),
            HRFlowable(width="100%", thickness=1, color=C_LINE, spaceAfter=3 * mm)]


def styled_table(rows, col_widths, alt_from=1):
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), C_TH_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.8, C_LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(alt_from, len(rows)):
        if (i - alt_from) % 2 == 1:
            cmds.append(("BACKGROUND", (0, i), (-1, i), C_ROW_ALT))
    tbl.setStyle(TableStyle(cmds))
    return tbl


def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=16 * mm, rightMargin=16 * mm,
        topMargin=15 * mm, bottomMargin=15 * mm,
    )
    story = []

    # ── ヘッダー ──
    header_left = [
        [Paragraph("工作教室　制作内容・予算のご提案", title_s)],
        [Paragraph("令和8年度　東北地区里親研修会　岩手大会　子ども企画（19日）", sub_s)],
    ]
    header_right = [
        [Paragraph("岩手県里親会事務局", label_s)],
        [Paragraph("川崎　舞美　様", label_s)],
    ]
    header_tbl = Table(
        [[Table(header_left, colWidths=[120 * mm]),
          Table(header_right, colWidths=[58 * mm])]],
        colWidths=[120 * mm, 58 * mm],
    )
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, C_LINE),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph(
        "ご参加児童12名が確定したとのご連絡をいただきましたので、制作内容と予算についてご提案いたします。"
        "内容にご了承いただけましたら、このまま準備を進めさせていただきます。",
        body_s))
    story.append(Spacer(1, 5 * mm))

    # ── 1. 企画概要 ──
    story += heading("1. 企画概要：レイヤーアート水族館をつくろう！")
    story.append(Paragraph(
        "透明フィルムやセロファンなどを重ねて、後景・中景・前景の3枚のカードをつくり、"
        "木製スタンドに差し込んで完成させる「レイヤーアート水族館」です。"
        "見る角度によって表情が変わる、奥行きのある作品になります。",
        body_s))
    story.append(Spacer(1, 4 * mm))

    img_front = Image(os.path.join(ASSET_DIR, "20260619_photo_里親大会工作サンプル_正面.jpg"),
                       width=75 * mm, height=75 * mm)
    img_parts = Image(os.path.join(ASSET_DIR, "20260619_photo_里親大会工作サンプル_バラバラ.jpg"),
                       width=75 * mm, height=75 * mm)
    photo_tbl = Table(
        [[img_front, img_parts],
         [Paragraph("完成イメージ", photo_caption_s),
          Paragraph("材料を重ねる前（パーツ）のイメージ", photo_caption_s)]],
        colWidths=[83 * mm, 83 * mm],
    )
    photo_tbl.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(photo_tbl)
    story.append(Spacer(1, 4 * mm))

    overview_rows = [
        [Paragraph("項目", th_s), Paragraph("内容", th_s)],
        [Paragraph("対象", td_b_s), Paragraph("参加児童12名（4歳〜15歳　付添1名含む）", td_b_s)],
        [Paragraph("制作時間", td_b_s), Paragraph("9:30〜11:30（実質約2時間）", td_b_s)],
        [Paragraph("講師体制", td_b_s), Paragraph("新田紗希（とうめいしっぽ）　※施設職員の方がお子さま一人ひとりに付き添われるとのことですので、制作のお手伝いをお願いしたいです", td_b_s)],
    ]
    story.append(styled_table(overview_rows, [40 * mm, 138 * mm]))
    story.append(Spacer(1, 5 * mm))

    # ── 2. 参加児童について ──
    story += heading("2. 参加児童の年齢構成と当日の配慮")
    age_rows = [
        [Paragraph("区分", th_s), Paragraph("人数", th_s), Paragraph("当日の対応", th_s)],
        [Paragraph("幼児（4〜6歳）", td_b_s), Paragraph("4名", td_c_s), Paragraph("簡単な図案を用意します", td_b_s)],
        [Paragraph("小学生（7〜11歳）", td_b_s), Paragraph("6名", td_c_s), Paragraph("通常の図案で、自分のペースで制作", td_b_s)],
        [Paragraph("中学生（15歳）", td_b_s), Paragraph("1名", td_c_s), Paragraph("通常の図案で対応", td_b_s)],
        [Paragraph("大学生（21歳・付添者）", td_b_s), Paragraph("1名", td_c_s), Paragraph("制作補助のサポート役として参加可能", td_b_s)],
        [Paragraph("合計", td_b_s), Paragraph("12名", td_c_s), Paragraph("", td_b_s)],
    ]
    story.append(styled_table(age_rows, [42 * mm, 20 * mm, 116 * mm]))
    story.append(Spacer(1, 3 * mm))
    for b in [
        "図案は「簡単・ふつう・むずかしめ」の3段階を用意し、年齢や得意・不得意に合わせて自由に選べるようにします。",
        "初めての参加で不安を感じやすい子や、個別の配慮が必要な子については、付き添いの職員の方に寄り添っていただけますと助かります。",
        "工作材料に食品は使用しないため、食事面での配慮事項は工作教室自体には影響しません。",
    ]:
        story.append(Paragraph("・" + b, bullet_s))
    story.append(Spacer(1, 5 * mm))

    # ── 3. 当日タイムライン ──
    story += heading("3. 当日タイムライン")
    timeline_rows = [
        [Paragraph("時間", th_s), Paragraph("内容", th_s)],
        [Paragraph("9:00〜9:30", td_c_s), Paragraph("会場設営・材料準備（新田のみ）", td_b_s)],
        [Paragraph("9:30〜9:40", td_c_s), Paragraph("オープニング・完成見本を見せながら工程説明", td_b_s)],
        [Paragraph("9:40〜10:00", td_c_s), Paragraph("台座づくり（全員で同じ工程）", td_b_s)],
        [Paragraph("10:00〜11:00", td_c_s), Paragraph("各パーツの制作（付き添いの職員の方にお子さまごとのお手伝いをお願いします）", td_b_s)],
        [Paragraph("11:00〜11:15", td_c_s), Paragraph("台座に差し込んで完成・仕上げ", td_b_s)],
        [Paragraph("11:15〜11:30", td_c_s), Paragraph("片付け・鑑賞タイム・記念撮影", td_b_s)],
    ]
    story.append(styled_table(timeline_rows, [32 * mm, 146 * mm]))
    story.append(Spacer(1, 5 * mm))

    # ── 4. 予算 ──
    story += heading("4. 予算")
    budget_rows = [
        [Paragraph("項目", th_s), Paragraph("金額", th_s)],
        [Paragraph("材料費（500円　×　12名）", td_b_s), Paragraph("6,000円", td_c_s)],
        [Paragraph("講師謝礼", td_b_s), Paragraph("4,000円", td_c_s)],
        [Paragraph("合計", td_b_s), Paragraph("10,000円", td_c_s)],
    ]
    story.append(styled_table(budget_rows, [110 * mm, 48 * mm]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "・材料はすべて新田が事前に準備し、当日持参いたします。",
        note_s))
    story.append(Spacer(1, 5 * mm))

    # ── 5. ご確認・ご協力のお願い ──
    story += heading("5. ご確認・ご協力をお願いしたい点")
    for b in [
        "上記の内容・予算でよろしければ、このまま準備を進めさせていただきます。",
        "施設職員の方には、お子さま一人ひとりの制作のお手伝い（図案選びや作業の補助など）をお願いできますと幸いです。",
        "当日、長机（12名分の作業スペース）のご準備をお願いいたします。",
        "完成品をラミネート加工するため、小型のラミネート機を持参予定です。電源を1か所ご確保いただけますと助かります。",
        "参加児童について、当日までに追加でお伝えいただきたい配慮事項がございましたら、お知らせください。",
    ]:
        story.append(Paragraph("・" + b, bullet_s))
    story.append(Spacer(1, 8 * mm))

    # ── フッター ──
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_LINE))
    story.append(Spacer(1, 3 * mm))
    footer_s = ParagraphStyle("ft", fontName="NS", fontSize=8.5, textColor=HexColor("#555555"), alignment=2)
    story.append(Paragraph("2026年6月19日　工作教室講師　新田紗希（おもちゃと遊び企画舎「とうめいしっぽ」代表）", footer_s))

    doc.build(story)
    print(f"生成完了: {output_path}")


if __name__ == "__main__":
    out = os.path.join(OUT_DIR, "20260619_doc_里親大会工作内容予算提案_draft_v1.pdf")
    generate_pdf(out)