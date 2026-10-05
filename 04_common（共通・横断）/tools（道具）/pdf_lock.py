# PDFにパスワード（開くときに必要）をかけるスクリプト
# ・中身（文章）は読まない。ファイルを鍵付きで保存し直すだけ
# ・元ファイルはそのまま残し、横に「◯◯_pw.pdf」を作る
# ・パスワードは画面に表示されない入力で受け取る（ログにも残さない）
# 使い方：pdf_lock.bat に PDF をドラッグ＆ドロップ、または
#        python pdf_lock.py "ファイル1.pdf" "ファイル2.pdf" ...

import sys
from getpass import getpass
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def ask_password():
    # 打ち間違い防止のため2回入力してもらう
    while True:
        pw1 = getpass("つけたいパスワードを入力（画面には表示されません）: ")
        if len(pw1) < 4:
            print("  → 短すぎるわ。4文字以上にしてね。\n")
            continue
        pw2 = getpass("確認のため、もう一度入力: ")
        if pw1 != pw2:
            print("  → 1回目と2回目が違うわ。もう一度ね。\n")
            continue
        return pw1


def lock_pdf(src: Path, password: str) -> bool:
    dst = src.with_name(src.stem + "_pw.pdf")
    # 鍵付きが既にある場合：元ファイルの方が新しければ（修正後なら）作り直す
    if dst.exists():
        if dst.stat().st_mtime >= src.stat().st_mtime:
            print(f"[スキップ] 最新の鍵付きが既にあります: {dst.name}")
            return False
        print(f"[作り直し] 元ファイルが修正されているため上書きします: {dst.name}")

    reader = PdfReader(src)
    if reader.is_encrypted:
        print(f"[スキップ] すでに鍵がかかっています: {src.name}")
        return False

    writer = PdfWriter(clone_from=reader)
    writer.encrypt(user_password=password, owner_password=None, algorithm="AES-256")
    with open(dst, "wb") as f:
        writer.write(f)

    # 本当に鍵がかかったか確認（パスワードで開けるか試す）
    check = PdfReader(dst)
    if not check.is_encrypted or not check.decrypt(password):
        print(f"[失敗] 鍵の確認ができませんでした: {dst.name}")
        dst.unlink(missing_ok=True)
        return False

    print(f"[完了] {dst.name}")
    return True


def main():
    files = [Path(a) for a in sys.argv[1:]]
    if not files:
        print("PDFファイルを指定してね（pdf_lock.bat にドラッグ＆ドロップでもOK）")
        return 1

    for f in files:
        if not f.is_file() or f.suffix.lower() != ".pdf":
            print(f"[エラー] PDFが見つかりません: {f}")
            return 1

    print(f"{len(files)}件のPDFに同じパスワードをかけます。\n")
    password = ask_password()
    print()

    ok = 0
    for f in files:
        try:
            if lock_pdf(f, password):
                ok += 1
        except Exception as e:
            print(f"[エラー] {f.name}: {e}")

    print(f"\n{ok} / {len(files)} 件 完了。元のファイルはそのまま残っています。")
    return 0


if __name__ == "__main__":
    code = main()
    input("\nEnterキーで閉じます")
    sys.exit(code)
