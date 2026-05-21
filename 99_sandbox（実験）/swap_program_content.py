import re, os

BASE = r'D:\Obsidian_Sync\リモート保管庫1\02_Notes\幼児教室プログラム\月別ノート'

def process(fname):
    path = os.path.join(BASE, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # ⑤おもちゃ・自由遊びの概要を取得
    m5 = re.search(r'\| ⑤おもちゃ・自由遊び[^|]*\|[^|]*\|([^|]*)\|', content)
    p5 = m5.group(1).strip() if m5 else ''

    # ④プログラムの概要を⑤の内容に置き換え
    content = re.sub(
        r'(\| ④プログラム[^|]*\|[^|]*\|)[^|]*(\|)',
        lambda m: m.group(1) + (' ' + p5 + ' ' if p5 else '  ') + m.group(2),
        content
    )

    # ⑤おもちゃ・自由遊びの概要を空に
    content = re.sub(
        r'(\| ⑤おもちゃ・自由遊び[^|]*\|[^|]*\|)[^|]*(\|)',
        lambda m: m.group(1) + '  ' + m.group(2),
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}  (p5="{p5}")')

FILES = ['04月.md','06月.md','07月.md','08月.md','09月.md',
         '10月.md','11月.md','12月.md','01月.md','02月.md','03月.md']

for f in FILES:
    process(f)

print('done')