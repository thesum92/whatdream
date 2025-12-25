import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time


def fetch_page(url):
    """Fetch a webpage and return BeautifulSoup object."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers)
        response.encoding = 'windows-1256'  # Arabic encoding
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_all_letter_pages():
    """Return all letter pages for complete Arabic alphabet."""
    # Complete list of Arabic letters with their page numbers
    letters = [
        {'letter': 'حرف الألف', 'page': 1},
        {'letter': 'حرف الباء', 'page': 2},
        {'letter': 'حرف التاء', 'page': 3},
        {'letter': 'حرف الثاء', 'page': 4},
        {'letter': 'حرف الجيم', 'page': 5},
        {'letter': 'حرف الحاء', 'page': 6},
        {'letter': 'حرف الخاء', 'page': 7},
        {'letter': 'حرف الدال', 'page': 8},
        {'letter': 'حرف الذال', 'page': 9},
        {'letter': 'حرف الراء', 'page': 10},
        {'letter': 'حرف الزاى', 'page': 11},
        {'letter': 'حرف السين', 'page': 12},
        {'letter': 'حرف الشين', 'page': 13},
        {'letter': 'حرف الصاد', 'page': 14},
        {'letter': 'حرف الضاد', 'page': 15},
        {'letter': 'حرف الطاء', 'page': 16},
        {'letter': 'حرف الظاء', 'page': 17},
        {'letter': 'حرف العين', 'page': 18},
        {'letter': 'حرف الغين', 'page': 19},
        {'letter': 'حرف الفاء', 'page': 20},
        {'letter': 'حرف القاف', 'page': 21},
        {'letter': 'حرف الكاف', 'page': 22},
        {'letter': 'حرف اللام', 'page': 23},
        {'letter': 'حرف الميم', 'page': 24},
        {'letter': 'حرف النون', 'page': 25},
        {'letter': 'حرف الهاء', 'page': 26},
        {'letter': 'حرف الواو', 'page': 27},
        {'letter': 'حرف الياء', 'page': 28},
    ]
    
    base_url = "https://mktbtk.com/dir/nab/"
    letter_pages = []
    
    for letter_info in letters:
        url = f"{base_url}na-{letter_info['page']}.htm"
        letter_pages.append({
            'letter': letter_info['letter'],
            'url': url,
            'page_num': letter_info['page']
        })
    
    return letter_pages


def get_topics_from_letter_page(letter_url, letter_name):
    """Extract all topic links from a letter page."""
    soup = fetch_page(letter_url)
    if not soup:
        return []
    
    topics = []
    seen_urls = set()
    
    # Find all links on the page
    for link in soup.find_all('a', href=True):
        href = link['href']
        topic_title = link.get_text(strip=True)
        
        # Skip navigation and index links
        if not href or href.startswith('#') or href == 'index.htm':
            continue
        
        # Skip letter navigation links (na-X.htm pattern)
        if href.startswith('na-') and href.endswith('.htm'):
            continue
        
        # Skip if title is empty or too short (navigation elements)
        if not topic_title or len(topic_title) < 2:
            continue
        
        # Skip if title looks like a letter name (navigation)
        if 'حرف' in topic_title:
            continue
        
        # Build full URL
        full_url = urljoin(letter_url, href)
        
        # Skip duplicates
        if full_url in seen_urls:
            continue
        
        seen_urls.add(full_url)
        topics.append({
            'title': topic_title,
            'url': full_url
        })
    
    return topics


def clean_content(content):
    """Remove the navigation header text and footer from content."""
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


def get_topic_content(url):
    """Extract content from a topic page."""
    soup = fetch_page(url)
    if not soup:
        return ""
    
    # Remove script, style, and other non-content elements
    for element in soup(['script', 'style', 'nav', 'header', 'footer']):
        element.decompose()
    
    # Get all text content
    text = soup.get_text(separator='\n')
    
    # Clean up text: remove extra whitespace and empty lines
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)
    
    content = '\n'.join(lines)
    
    # Clean the navigation header
    content = clean_content(content)
    
    return content


def scrape_all_dreams():
    """Main scraping function."""
    print("="*70)
    print("Dream Interpretation Scraper - Complete Arabic Alphabet")
    print("="*70)
    
    # Get all letter pages (28 Arabic letters)
    letter_pages = get_all_letter_pages()
    print(f"\nProcessing {len(letter_pages)} Arabic letters (الألف to الياء)")
    
    database = []
    total_topics = 0
    
    # Process each letter
    for i, letter_page in enumerate(letter_pages, 1):
        print(f"\n[{i}/{len(letter_pages)}] Processing: {letter_page['letter']}")
        print(f"URL: {letter_page['url']}")
        
        # Get all topics for this letter
        topics = get_topics_from_letter_page(
            letter_page['url'], 
            letter_page['letter']
        )
        
        if not topics:
            print(f"  ⚠ No topics found for {letter_page['letter']}")
            continue
        
        print(f"  ✓ Found {len(topics)} topics")
        
        # Process each topic
        for j, topic in enumerate(topics, 1):
            print(f"    [{j}/{len(topics)}] {topic['title']}")
            
            # Get content
            content = get_topic_content(topic['url'])
            
            # Add to database in the exact format required
            database.append({
                'topic': topic['title'],
                'url': topic['url'],
                'content': content
            })
            
            total_topics += 1
            
            # Be polite to the server
            time.sleep(0.5)
        
        # Pause between letters
        time.sleep(1)
    
    # Save to JSON file
    output_file = 'dreams_database.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print(f"✓ SCRAPING COMPLETE!")
    print(f"✓ Total topics scraped: {total_topics}")
    print(f"✓ Letters processed: {len(letter_pages)}")
    print(f"✓ Output file: {output_file}")
    print("="*70)
    
    return database


def show_sample(database, num_samples=5):
    """Display sample entries from the database."""
    if not database:
        print("No data to show")
        return
    
    print(f"\n📋 Sample entries (first {num_samples}):\n")
    for i, entry in enumerate(database[:num_samples], 1):
        print(f"{i}. Topic: {entry['topic']}")
        print(f"   URL: {entry['url']}")
        print(f"   Content preview: {entry['content'][:100]}...")
        print()


def main():
    """Entry point."""
    try:
        database = scrape_all_dreams()
        show_sample(database)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()