#!/usr/bin/env python3
"""
Google SpreadsheetsからデータをCSV形式で取得してHTMLファイルを生成するスクリプト
"""

import requests
import csv
from io import StringIO
from datetime import datetime

# Google SheetsのID
SHEET_ID = "1sId2LudYD-AwjE2BQdYMdMin4p2gV_sOIWv1rTFnAu0"
# シートのGID（リンク一覧）
SHEET_GID = "1294449581"

# CSV形式でエクスポートするURL
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"

def fetch_sheet_data():
    """Google SheetsからCSVデータを取得"""
    try:
        response = requests.get(CSV_URL, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def generate_html(csv_data):
    """CSVデータからHTMLを生成"""
    reader = csv.reader(StringIO(csv_data))
    rows = list(reader)
    
    if not rows:
        return None
    
    # ヘッダー行を取得
    headers = rows[0] if rows else []
    data_rows = rows[1:] if len(rows) > 1 else []
    
    # HTML生成
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>スロ天重要まとめシート - リンク一覧</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .update-time {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .search-container {{
            padding: 20px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        #searchInput {{
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            transition: border-color 0.3s;
        }}
        
        #searchInput:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .table-container {{
            overflow-x: auto;
            padding: 20px 30px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        
        thead {{
            background: #f8f9fa;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        th {{
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #667eea;
            white-space: nowrap;
        }}
        
        td {{
            padding: 12px 10px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        a {{
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.2em;
        }}
        
        footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 スロ天重要まとめシート</h1>
            <p class="update-time">最終更新: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </header>
        
        <div class="search-container">
            <input type="text" id="searchInput" placeholder="🔍 検索...（名称、URL、カテゴリなど）">
        </div>
        
        <div class="table-container">
            <table id="dataTable">
                <thead>
                    <tr>
"""
    
    # ヘッダー行を追加
    for header in headers:
        html += f"                        <th>{header if header else ''}</th>\n"
    
    html += """                    </tr>
                </thead>
                <tbody>
"""
    
    # データ行を追加
    for row in data_rows:
        html += "                    <tr>\n"
        for i, cell in enumerate(row):
            # URLカラム（列B、インデックス1）の場合はリンクとして表示
            if i == 1 and cell and (cell.startswith('http://') or cell.startswith('https://')):
                html += f'                        <td><a href="{cell}" target="_blank">{cell}</a></td>\n'
            else:
                html += f"                        <td>{cell if cell else ''}</td>\n"
        # 行の長さが足りない場合は空のセルを追加
        for _ in range(len(headers) - len(row)):
            html += "                        <td></td>\n"
        html += "                    </tr>\n"
    
    html += """                </tbody>
            </table>
            <div id="noResults" class="no-results" style="display: none;">
                検索結果が見つかりませんでした
            </div>
        </div>
        
        <footer>
            <p>自動更新システム | 毎日更新</p>
            <p><a href="https://docs.google.com/spreadsheets/d/1sId2LudYD-AwjE2BQdYMdMin4p2gV_sOIWv1rTFnAu0/edit" target="_blank">元のスプレッドシートを開く</a></p>
        </footer>
    </div>
    
    <script>
        // 検索機能
        const searchInput = document.getElementById('searchInput');
        const table = document.getElementById('dataTable');
        const tbody = table.querySelector('tbody');
        const noResults = document.getElementById('noResults');
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = tbody.querySelectorAll('tr');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // 検索結果がない場合
            if (visibleCount === 0) {
                table.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                table.style.display = 'table';
                noResults.style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""
    
    return html

def main():
    """メイン処理"""
    print("Google Sheetsからデータを取得中...")
    csv_data = fetch_sheet_data()
    
    if not csv_data:
        print("データの取得に失敗しました")
        return False
    
    print("HTMLを生成中...")
    html = generate_html(csv_data)
    
    if not html:
        print("HTMLの生成に失敗しました")
        return False
    
    # HTMLファイルを保存
    output_file = "links.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ {output_file} を生成しました")
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
