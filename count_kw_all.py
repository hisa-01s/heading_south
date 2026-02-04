import csv
import re
from collections import Counter
import os
import sys

# 除外ワード
EXCLUDE = set([
    '千社札', 'とは', 'の', 'が', 'に', 'を', 'は', 'と', 'で', 'も', 'や', 'から', 'まで', 'より', 'へ',
    'そして', 'また', 'または', 'など', 'その', 'この', 'あの', 'それ', 'これ', 'あれ', 'ため', 'ので', 'が'
])

# ファイルのBOMやバイナリ先頭を見てエンコーディング自動判別
def auto_open(filename):
    with open(filename, 'rb') as f:
        raw = f.read(4096)
    if raw.startswith(b'\xff\xfe'):
        enc = 'utf-16'
    elif raw.startswith(b'\xfe\xff'):
        enc = 'utf-16'
    elif raw.startswith(b'\xef\xbb\xbf'):
        enc = 'utf-8-sig'
    else:
        try:
            raw.decode('utf-8')
            enc = 'utf-8'
        except Exception:
            try:
                raw.decode('cp932')
                enc = 'cp932'
            except Exception:
                enc = 'shift-jis'
    return open(filename, encoding=enc)

# ディレクトリ指定（引数 or カレント）
def main(target_dir):
    os.chdir(target_dir)
    # キーワード抽出
    keywords = set()
    for fname in ['00_02.csv', '00_03.csv', '00_04.csv']:
        if not os.path.exists(fname):
            continue
        with auto_open(fname) as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                for col in row:
                    for word in re.split(r'[\s　]+', col.replace('"', '')):
                        if word and word not in EXCLUDE and not word.isdigit():
                            keywords.add(word)
    # 00_01.csvから見出し・本文列を抽出
    headline_list = []
    if os.path.exists('00_01.csv'):
        with auto_open('00_01.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                for col in row:
                    headline_list.append(col)
    # キーワードごとにカウント
    counter = Counter()
    for kw in keywords:
        for headline in headline_list:
            counter[kw] += headline.count(kw)
    # 結果を01_01.csvに出力
    with open('01_01.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['キーワード', 'カウント'])
        for kw, cnt in sorted(counter.items(), key=lambda x: -x[1]):
            writer.writerow([kw, cnt])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python count_kw_all.py <target_dir>')
