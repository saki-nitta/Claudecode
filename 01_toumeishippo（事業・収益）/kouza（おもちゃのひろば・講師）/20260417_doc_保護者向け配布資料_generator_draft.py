# 保護者向け配布資料 PDF生成スクリプト
# とうめいしっぽ 工作教室用
# 出力先: 20260417_doc_保護者向け配布資料_final.pdf

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─────────────────────────────────────
# フォント登録
# ─────────────────────────────────────
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("NotoSerif",     os.path.join(FONT_DIR, "NotoSerifJP-VF.ttf")))
pdfmetrics.registerFont(TTFont("NotoSerifBold", os.path.join(FONT_DIR, "yumindb.ttf")))  # 太字見出し用

# ─────────────────────────────────────
# 2色パレット（白黒印刷対応）
# ─────────────────────────────────────
INK    = HexColor("#2B2B2B")  # ほぼ黒：本文・見出し
ACCENT = HexColor("#7A6352")  # ブラウングレー：罫線・装飾（白黒印刷でグレーになる）

# ─────────────────────────────────────
# レイアウト定数
# ─────────────────────────────────────
LM       = 18 * mm   # 左マージン
RM_OFFSET = 18 * mm  # 右マージン
LH_BODY  = 7.2 * mm  # 本文行高（ゆったり）
LH_HINT  = 8.0 * mm  # ヒント行高
PG       = 5.0 * mm  # 段落間
BODY_SIZE = 9.5      # 本文フォントサイズ

# ─────────────────────────────────────
# ユーティリティ
# ─────────────────────────────────────

def wrap_lines(c, text, font, size, max_w):
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if c.stringWidth(test, font, size) > max_w:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def para_height(c, text, font, size, max_w, lh):
    """段落の高さを計算"""
    return len(wrap_lines(c, text, font, size, max_w)) * lh


def draw_para(c, text, x, y, font, size, color, max_w, lh):
    """段落描画。次のY座標を返す"""
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_lines(c, text, font, size, max_w):
        c.drawString(x, y, line)
        y -= lh
    return y


def section_heading(c, x, y, label, tw):
    """左アクセントバー＋テキスト＋下線の見出し。占有高さを返す"""
    bar_h = 8 * mm
    c.setFillColor(ACCENT)
    c.rect(x, y - bar_h + 6*mm, 3*mm, bar_h, fill=1, stroke=0)
    c.setFont("NotoSerifBold", 13)
    c.setFillColor(INK)
    c.drawString(x + 5*mm, y, label)
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.line(x, y - 3*mm, x + tw, y - 3*mm)
    return 9 * mm  # 見出し占有高さ（呼び出し元でY減算に使う）


# ─────────────────────────────────────
# コンテンツ定義
# ─────────────────────────────────────
PARAS_SEC1 = [
    "この教室では、市販の「キット」は使いません。",
    "材料を渡して、自分の頭で考えながらつくることを大切にしています。",
    "なぜかというと、ゼロから何かをつくる経験の中に、大切なことがたくさん詰まっているからです。",
    "「なんでこうなるんだろう？」と考えながら手を動かすことで、モノのしくみが自然と身についていきます。",
    "そして自分でつくり上げたときの「できた！」という気持ちは、何にも代えがたいものです。",
    "使う材料は、紙コップ・輪ゴム・ストローなど、百円均一で買えておうちにもストックしやすいものが中心です。",
    "「こんな身近なものが、おもちゃになるんだ！」という発見を楽しんでほしいという思いがあります。",
    "教室でやったことを、おうちでもう一度試したり、自分なりにアレンジしてみてくれたら嬉しいです。",
]
PARAS_SEC2 = [
    "つくった作品は、ぜひしばらくおうちに飾ってあげてください。",
    "ただ、赤ちゃんやペットがいるなど、ご家庭の環境はさまざまだと思います。",
    "そんなときにおすすめしたいのが、写真に撮ってあげることです。",
    "写真を撮ってもらえると、お子さんは「ちゃんと見てもらえた」と感じます。",
    "記録にも残るので、後で処分するときにもスムーズなことが多いです。",
    "手早くつくったものが壊れてしまうこともありますが、それも立派な経験のひとつです。",
]
LEADS_SEC3 = [
    "この教室は、子どもたちが自分を表現したり、気持ちを発散したりできる場所でもあります。",
    "帰ってきたら、こんなふうに話しかけてみてください。",
]
SEC3_CLOSING = "工作を通して、\u201cつくる\u201d ことの楽しさと奥深さを、お子さんと一緒に感じていただけたら嬉しいです。"
HINTS = [
    "どんなところを工夫したの？",
    "気に入っているところはどこ？",
    "むずかしかったところはあった？",
]

# ─────────────────────────────────────
# メイン描画
# ─────────────────────────────────────

def generate_pdf(output_path):
    width, height = A4
    c = canvas.Canvas(output_path, pagesize=A4)

    RM = width - RM_OFFSET
    TW = RM - LM  # テキスト幅

    # 外枠なし

    # ─────────────────────────────────────
    # 高さ事前計算（セクション間の余白を均等配分するため）
    # ─────────────────────────────────────
    TITLE_H   = 12 * mm + 8 * mm            # タイトル行 + サブタイトル
    HEADING_H = 9 * mm + 5 * mm            # 見出し + 見出し後の隙間

    def sec_text_h(paras):
        return sum(para_height(c, p, "NotoSerif", BODY_SIZE, TW, LH_BODY) for p in paras)

    sec1_h = HEADING_H + sec_text_h(PARAS_SEC1)
    sec2_h = HEADING_H + sec_text_h(PARAS_SEC2)
    lead_h = len(LEADS_SEC3) * LH_BODY + PG
    hints_h = len(HINTS) * LH_HINT
    closing_h = PG + LH_BODY
    sec3_h = HEADING_H + lead_h + hints_h + closing_h
    FOOTER_H = 5*mm + 10*mm  # 区切り線上余白 + 署名

    CONTENT_H = TITLE_H + LH_BODY + sec1_h + sec2_h + sec3_h + FOOTER_H  # タイトル後の追加1行分込み
    USABLE_H  = height - 24*mm - 6*mm  # 外枠内の使用可能高さ（上下余白込み）

    # 3つのセクション間 + タイトル後 + フッター前 = 5箇所に余白を均等配分
    leftover  = USABLE_H - CONTENT_H
    SG        = max(6*mm, leftover / 5)  # セクション間余白（最低6mm）

    # ─────────────────────────────────────
    # ① タイトル
    # ─────────────────────────────────────
    ty = height - 18 * mm

    c.setFont("NotoSerifBold", 20)
    c.setFillColor(INK)
    c.drawCentredString(width / 2, ty, "工作教室にご参加くださる保護者の皆さまへ")

    ty -= 12 * mm
    c.setFont("NotoSerif", 11)
    c.setFillColor(ACCENT)
    c.drawCentredString(width / 2, ty,
                        "\u301c\u300c\u3064\u304f\u308b\u300d\u3063\u3066\u3001\u3059\u3054\u3044\u3053\u3068\u301c")

    ty -= SG + LH_BODY  # タイトル後は1行分多めに空ける

    # ─────────────────────────────────────
    # ② セクション1
    # ─────────────────────────────────────
    section_heading(c, LM, ty, "この教室のねらいについて", TW)
    ty -= HEADING_H

    for p in PARAS_SEC1:
        ty = draw_para(c, p, LM, ty, "NotoSerif", BODY_SIZE, INK, TW, LH_BODY)

    ty -= SG

    # ─────────────────────────────────────
    # ③ セクション2
    # ─────────────────────────────────────
    section_heading(c, LM, ty, "作品のこと", TW)
    ty -= HEADING_H

    for p in PARAS_SEC2:
        ty = draw_para(c, p, LM, ty, "NotoSerif", BODY_SIZE, INK, TW, LH_BODY)

    ty -= SG

    # ─────────────────────────────────────
    # ④ セクション3
    # ─────────────────────────────────────
    section_heading(c, LM, ty, "おうちでの声かけのヒント", TW)
    ty -= HEADING_H

    c.setFont("NotoSerif", BODY_SIZE)
    c.setFillColor(INK)
    for line in LEADS_SEC3:
        c.drawString(LM, ty, line)
        ty -= LH_BODY
    ty -= PG

    for hint in HINTS:
        c.setFillColor(ACCENT)
        c.rect(LM + 4*mm, ty - 3*mm, 1.5*mm, LH_HINT - 1*mm, fill=1, stroke=0)
        c.setFont("NotoSerif", 10.5)
        c.setFillColor(INK)
        c.drawString(LM + 8*mm, ty, hint)
        ty -= LH_HINT

    ty -= PG
    c.setFont("NotoSerif", BODY_SIZE)
    c.setFillColor(INK)
    c.drawString(LM, ty, SEC3_CLOSING)
    ty -= LH_BODY

    ty -= SG

    # ─────────────────────────────────────
    # ⑤ フッター
    # ─────────────────────────────────────
    c.saveState()
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.line(LM, ty, RM, ty)
    c.restoreState()

    ty -= 7 * mm
    c.setFont("NotoSerif", 8.5)
    c.setFillColor(ACCENT)
    c.drawRightString(RM, ty,
                      "工作教室講師　新田紗希（おもちゃと遊び企画舎「とうめいしっぽ」代表）")

    c.save()
    print(f"PDF生成完了: {output_path}")


# ─────────────────────────────────────
if __name__ == "__main__":
    out_dir = r"D:\toumei.shippo\01_toumeishippo（事業・収益）\event"
    output_path = os.path.join(out_dir, "20260417_doc_保護者向け配布資料_final.pdf")
    generate_pdf(output_path)
