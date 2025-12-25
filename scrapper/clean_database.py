import json
import re


def clean_content(content):
    """Remove the header text and footer from content."""
    # Split by lines
    lines = content.split('\n')
    
    # Keywords to identify the header section
    header_keywords = [
        'قاموس تفسير كلمات الأحلام',
        'حرف الألف',
        'حرف الباء',
        'حرف التاء',
        'حرف الثاء',
        'حرف الجيم',
        'حرف الحاء',
        'حرف الخاء',
        'حرف الدال',
        'حرف الذال',
        'حرف الراء',
        'حرف الزاى',
        'حرف السين',
        'حرف الشين',
        'حرف الصاد',
        'حرف الضاد',
        'حرف الطاء',
        'حرف الظاء',
        'حرف العين',
        'حرف الغين',
        'حرف الفاء',
        'حرف القاف',
        'حرف الكاف',
        'حرف اللام',
        'حرف الميم',
        'حرف النون',
        'حرف الهاء',
        'حرف الواو',
        'حرف الياء',
        'سور القرآن الكريم',
        'تفسير الأحلام لابن سيرين',
        'تفسير الأحلام لابن شاهين'
    ]
    
    # Keywords to identify footer
    footer_patterns = [
        'ahlam.NoorDubai.Tv',
        'Tafserahlam.com',
        'Mktbtk.com'
    ]
    
    # Filter out header and footer lines
    cleaned_lines = []
    skip_mode = False
    
    for line in lines:
        line = line.strip()
        
        # Skip footer lines
        if any(pattern in line for pattern in footer_patterns):
            continue
        
        # Skip if it's just a year (2026, etc.)
        if line.isdigit() and len(line) == 4:
            continue
        
        # Skip if line matches any header keyword
        if any(keyword in line for keyword in header_keywords):
            skip_mode = True
            continue
        
        # After header, start collecting content
        if skip_mode and line and not any(keyword in line for keyword in header_keywords):
            skip_mode = False
        
        if not skip_mode and line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def clean_database(input_file, output_file):
    """Clean the entire database JSON file."""
    print(f"Loading {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
    
    print(f"Found {len(database)} entries")
    print("Cleaning content...")
    
    for i, entry in enumerate(database, 1):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(database)}")
        
        if 'content' in entry:
            entry['content'] = clean_content(entry['content'])
    
    print(f"Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Done! Cleaned database saved to {output_file}")


if __name__ == "__main__":
    clean_database('dreams_database.json', 'dreams_database_cleaned.json')
