#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import csv
from io import StringIO
from datetime import datetime
from collections import defaultdict

# Google Sheets設定
SHEET_ID = '1sId2LudYD-AwjE2BQdYMdMin4p2gV_sOIWv1rTFnAu0'
SHEET_GID = '1294449581'
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}'

def fetch_sheet_data():
    """Google SheetsからCSVデータを取得"""
    try:
        response = requests.get(CSV_URL, timeout=30)
        response.raise_for_status()
        # バイト列をUTF-8でデコード
        return response.content.decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def parse_csv_data(csv_data):
    """CSVデータを解析して縦一列のデータに変換"""
    reader = csv.reader(StringIO(csv_data))
    rows = list(reader)
    
    if len(rows) < 2:
        return []
    
    # ヘッダー行をスキップ
    data_rows = rows[1:]
    
    # すべてのデータを統合
    all_items = []
    
    for row in data_rows:
        # A-D列（0-3）
        if len(row) > 3 and row[0].strip():
            all_items.append({
                '名称': row[0].strip(),
                'URL': row[1].strip() if len(row) > 1 else '',
                'ジャンル': row[2].strip() if len(row) > 2 else '',
                '部署': row[3].strip() if len(row) > 3 else ''
            })
        
        # F-I列（5-8）
        if len(row) > 8 and row[5].strip():
            all_items.append({
                '名称': row[5].strip(),
                'URL': row[6].strip() if len(row) > 6 else '',
                'ジャンル': row[7].strip() if len(row) > 7 else '',
                '部署': row[8].strip() if len(row) > 8 else ''
            })
        
        # K-N列（10-13）
        if len(row) > 13 and row[10].strip():
            all_items.append({
                '名称': row[10].strip(),
                'URL': row[11].strip() if len(row) > 11 else '',
                'ジャンル': row[12].strip() if len(row) > 12 else '',
                '部署': row[13].strip() if len(row) > 13 else ''
            })
        
        # P-S列（15-18）
        if len(row) > 18 and row[15].strip():
            all_items.append({
                '名称': row[15].strip(),
                'URL': row[16].strip() if len(row) > 16 else '',
                'ジャンル': row[17].strip() if len(row) > 17 else '',
                '部署': row[18].strip() if len(row) > 18 else ''
            })
    
    return all_items

def group_by_category(items):
    """ジャンル（カテゴリ）でグループ化"""
    grouped = defaultdict(list)
    for item in items:
        category = item['ジャンル'] if item['ジャンル'] else 'その他'
        grouped[category].append(item)
    return dict(grouped)

def generate_html(items):
    """カテゴリ別に分類されたHTMLを生成"""
    grouped_items = group_by_category(items)
    
    # カテゴリを並び替え（アルファベット順）
    categories = sorted(grouped_items.keys())
    
    # カテゴリごとのHTML生成
    categories_html = ''
    tables_html = ''
    
    for category in categories:
        category_id = category.replace(' ', '_').replace('/', '_')
        item_count = len(grouped_items[category])
        
        # カテゴリボタン
        categories_html += f'''
            <button class="category-btn" data-category="{category_id}">
                {category} <span class="badge">{item_count}</span>
            </button>
        '''
        
        # カテゴリテーブル
        rows_html = ''
        for item in grouped_items[category]:
            url_display = f'<a href="{item["URL"]}" target="_blank">{item["URL"]}</a>' if item['URL'] else ''
            rows_html += f'''
                <tr>
                    <td>{item['名称']}</td>
                    <td>{url_display}</td>
                    <td>{item['部署']}</td>
                </tr>
            '''
        
        tables_html += f'''
            <div class="category-section" id="category-{category_id}">
                <h2>📁 {category}</h2>
                <table>
                    <thead>
                        <tr>
                            <th>名称</th>
                            <th>URL</th>
                            <th>部署</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        '''
    
    # 最終更新時刻
    last_update = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    
    html_template = f'''<!DOCTYPE html>
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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }}
        
        .last-update {{
            opacity: 0.9;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .controls {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .search-box {{
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #667eea;
            border-radius: 50px;
            outline: none;
            transition: all 0.3s;
        }}
        
        .search-box:focus {{
            border-color: #764ba2;
            box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.1);
        }}
        
        .categories {{
            padding: 20px 30px;
            background: #fff;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .category-btn {{
            padding: 10px 20px;
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .category-btn:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
        }}
        
        .category-btn.active {{
            background: #764ba2;
            color: white;
            border-color: #764ba2;
        }}
        
        .badge {{
            background: rgba(255,255,255,0.3);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .category-btn:hover .badge,
        .category-btn.active .badge {{
            background: rgba(255,255,255,0.5);
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .category-section {{
            margin-bottom: 40px;
            animation: fadeIn 0.5s;
        }}
        
        .category-section h2 {{
            color: #764ba2;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        a {{
            color: #667eea;
            text-decoration: none;
            transition: color 0.3s;
            word-break: break-all;
        }}
        
        a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}
        
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
            font-size: 1.2em;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .controls {{
                padding: 20px;
            }}
            
            .categories {{
                padding: 15px 20px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            table {{
                font-size: 14px;
            }}
            
            th, td {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 スロ天重要まとめシート</h1>
            <div class="last-update">最終更新: {last_update}</div>
        </div>
        
        <div class="controls">
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 検索...（名称、URL、部署など）">
        </div>
        
        <div class="categories">
            <button class="category-btn active" data-category="all">
                すべて <span class="badge">{len(items)}</span>
            </button>
            {categories_html}
        </div>
        
        <div class="content" id="content">
            {tables_html}
        </div>
    </div>
    
    <script>
        // 検索機能
        const searchInput = document.getElementById('searchInput');
        const categoryBtns = document.querySelectorAll('.category-btn');
        const categorySections = document.querySelectorAll('.category-section');
        
        let currentCategory = 'all';
        
        // カテゴリフィルタ
        categoryBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                categoryBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentCategory = btn.dataset.category;
                filterContent();
            }});
        }});
        
        // 検索機能
        searchInput.addEventListener('input', filterContent);
        
        function filterContent() {{
            const searchTerm = searchInput.value.toLowerCase();
            let visibleCount = 0;
            
            categorySections.forEach(section => {{
                const categoryId = section.id.replace('category-', '');
                const rows = section.querySelectorAll('tbody tr');
                let sectionHasVisibleRows = false;
                
                // カテゴリフィルタ
                if (currentCategory !== 'all' && categoryId !== currentCategory) {{
                    section.style.display = 'none';
                    return;
                }}
                
                rows.forEach(row => {{
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {{
                        row.style.display = '';
                        sectionHasVisibleRows = true;
                        visibleCount++;
                    }} else {{
                        row.style.display = 'none';
                    }}
                }});
                
                section.style.display = sectionHasVisibleRows ? 'block' : 'none';
            }});
            
            // 結果なしメッセージ
            const content = document.getElementById('content');
            let noResults = content.querySelector('.no-results');
            
            if (visibleCount === 0) {{
                if (!noResults) {{
                    noResults = document.createElement('div');
                    noResults.className = 'no-results';
                    noResults.textContent = '😔 該当する項目が見つかりませんでした';
                    content.appendChild(noResults);
                }}
            }} else {{
                if (noResults) {{
                    noResults.remove();
                }}
            }}
        }}
    </script>
</body>
</html>'''
    
    return html_template

def main():
    print("Google Sheetsからデータを取得中...")
    csv_data = fetch_sheet_data()
    
    if not csv_data:
        print("❌ データの取得に失敗しました")
        return
    
    print("データを解析中...")
    items = parse_csv_data(csv_data)
    
    if not items:
        print("❌ データの解析に失敗しました")
        return
    
    print(f"✓ {len(items)}件のデータを取得しました")
    
    print("HTMLを生成中...")
    html_content = generate_html(items)
    
    # HTMLファイルを保存
    with open('links.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ links.html を生成しました")

if __name__ == '__main__':
    main()
