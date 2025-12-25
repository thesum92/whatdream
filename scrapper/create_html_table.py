import json
import argparse


def load_database(filename='dreams_database.json'):
    """Load the dreams database from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []
    except Exception as e:
        print(f"Error loading database: {e}")
        return []


def create_html_table(database):
    """Create an HTML page with a table of topics and content."""
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تفسير الأحلام - Dream Interpretations</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .stats {
            text-align: center;
            margin-bottom: 20px;
            font-size: 18px;
            color: #666;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            text-align: right;
            font-size: 18px;
            position: sticky;
            top: 0;
        }
        td {
            padding: 15px;
            border-bottom: 1px solid #ddd;
            text-align: right;
            vertical-align: top;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .topic-cell {
            font-weight: bold;
            color: #2196F3;
            width: 200px;
            min-width: 150px;
        }
        .content-cell {
            line-height: 1.6;
            white-space: pre-wrap;
        }
        .index {
            color: #999;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>قاعدة بيانات تفسير الأحلام</h1>
    <div class="stats">عدد المواضيع: """ + str(len(database)) + """</div>
    <table>
        <thead>
            <tr>
                <th>الموضوع (Topic)</th>
                <th>المحتوى (Content)</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for i, dream in enumerate(database, 1):
        topic = dream.get('topic', 'N/A')
        content = dream.get('content', 'N/A')
        
        # Escape HTML special characters
        topic = topic.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        html += f"""            <tr>
                <td class="topic-cell">
                    <span class="index">[{i}]</span><br>
                    {topic}
                </td>
                <td class="content-cell">{content}</td>
            </tr>
"""
    
    html += """        </tbody>
    </table>
</body>
</html>
"""
    
    return html


def main():
    """Main function to create HTML file."""
    parser = argparse.ArgumentParser(description='Create HTML table from dreams database JSON file')
    parser.add_argument('--input', '-i', default='dreams_database.json',
                        help='Input JSON file (default: dreams_database.json)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: auto-generated from input)')
    
    args = parser.parse_args()
    
    json_file = args.input
    
    print(f"Loading database from: {json_file}")
    database = load_database(json_file)
    
    if not database:
        print("No data found in database.")
        return
    
    print(f"Found {len(database)} topics")
    print("Creating HTML file...")
    
    html_content = create_html_table(database)
    
    # Create output filename from input base name
    if args.output:
        output_file = args.output
    else:
        # Extract base name without extension
        import os
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        output_file = f"{base_name}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Successfully created {output_file}")
    print("Open it in your browser to view the table.")


if __name__ == "__main__":
    main()
