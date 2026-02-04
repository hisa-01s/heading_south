import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import os

def get_page_content(url):
    """URLからページの本文を取得する"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 不要な要素を削除
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 
                         'aside', 'form', 'iframe', 'noscript']):
            tag.decompose()
        
        # 本文を取得（優先順位: article > main > body）
        content = soup.find('article') or soup.find('main') or soup.find('body')
        
        if content:
            text = content.get_text(separator='\n', strip=True)
            # 連続する空行を1つにまとめる
            text = re.sub(r'\n{3,}', '\n\n', text)
            return text
        return "本文を取得できませんでした。"
    
    except requests.RequestException as e:
        return f"エラー: {e}"

def sanitize_filename(url):
    """URLから安全なファイル名を生成"""
    parsed = urlparse(url)
    name = parsed.netloc + parsed.path
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:50] + '.txt'

URLS = [
    "https://www.charleskeith.jp/jp/bags/workwear",
    "https://www.nissen.co.jp/s/shoes/AC18SP103/?srsltid=AfmBOor409dNBiN6GkPXLdTcsHUImD9L6QOb8Tzg0AWAeREO10Nmrs4j",
    "https://search.rakuten.co.jp/search/mall/%E9%80%9A%E5%8B%A4%E3%83%90%E3%83%83%E3%82%B0+%E3%83%AC%E3%83%87%E3%82%A3%E3%83%BC%E3%82%B9/",
    "https://mitsui-shopping-park.com/ec/feature/womens-businessbag",
    "https://voi.0101.co.jp/voi/content/01/sp/topics/column/column_245.html",
    "https://my-best.com/6797",
    "https://www.buyma.com/contents/work-bag/?srsltid=AfmBOoo67O75sB3khHxUdlVwjn9IjoKqFDbHb76iNXA2iORxRBADBoD_",
    "https://zozo.jp/women-category/bag/?p_keyv=%92%CA%8B%CE&srsltid=AfmBOoq5-0GFcmTIoj6uTny8rwiNzdpEQnMPRCBfjiuQo2DQLSoEQfji",
    "https://cooga-store.jp/c/column/ladies-bag/business-bag-brand?srsltid=AfmBOopLmSnXRkU_pqKZbuXSYPnSL1gS1drUEHCLl_Bgv_Yemh3gNUZx"
]

def main():
    print("=" * 50)
    print("URL本文抽出ツール（リスト指定版）")
    print("=" * 50)
    print(f"{len(URLS)}件のURLを処理中...")
    output_dir = "extracted_texts"
    os.makedirs(output_dir, exist_ok=True)
    for i, url in enumerate(URLS, 1):
        print(f"[{i}/{len(URLS)}] {url[:60]}...")
        content = get_page_content(url)
        filename = os.path.join(output_dir, f"{i:02d}_{sanitize_filename(url)}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
        print(f"  → 保存: {filename}")
    print(f"\n完了！{output_dir}フォルダに保存しました。")

if __name__ == "__main__":
    main()
