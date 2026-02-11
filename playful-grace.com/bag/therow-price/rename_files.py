import os
import glob

# 現在のディレクトリのパスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# ファイル名の対応関係を定義
rename_map = {
    'rakkokeyword_headlines': '00_01.csv',
    'rakkokeyword_suggestKeywords': '00_02.csv',
    'rakkokeyword_relatedKeywords': '00_03.csv',
    'rakkokeyword_otherKeywords': '00_04.csv'
}

def rename_files():
    """指定されたパターンに一致するファイルを新しい名前に変更する"""
    
    # 各パターンについて処理
    for pattern, new_name in rename_map.items():
        # パターンに一致するCSVファイルを検索
        search_pattern = os.path.join(current_dir, f'*{pattern}*.csv')
        matching_files = glob.glob(search_pattern)
        
        if not matching_files:
            print(f'警告: "{pattern}" を含むファイルが見つかりませんでした')
            continue
        
        if len(matching_files) > 1:
            print(f'警告: "{pattern}" に一致するファイルが複数見つかりました:')
            for f in matching_files:
                print(f'  - {os.path.basename(f)}')
            print(f'  最初のファイルのみを "{new_name}" に変更します')
        
        # 最初に見つかったファイルを変更
        old_path = matching_files[0]
        new_path = os.path.join(current_dir, new_name)
        
        # 新しいファイル名が既に存在するかチェック
        if os.path.exists(new_path):
            print(f'エラー: "{new_name}" は既に存在します。スキップします。')
            continue
        
        try:
            os.rename(old_path, new_path)
            print(f'成功: "{os.path.basename(old_path)}" → "{new_name}"')
        except Exception as e:
            print(f'エラー: "{os.path.basename(old_path)}" の変更に失敗しました: {e}')

if __name__ == '__main__':
    print('ファイル名変更を開始します...\n')
    rename_files()
    print('\n処理が完了しました。')
