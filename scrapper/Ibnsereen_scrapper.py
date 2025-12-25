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


def clean_content(content):
    """Remove the header text and footer from content."""
    # Split by lines
    lines = content.split('\n')
    
    # Keywords to identify the header section and navigation
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


def get_all_topic_urls():
    """Generate all topic URLs from d-0001.htm to d-0073.htm."""
    base_url = "http://www.mktbtk.com/dir/ser/"
    topics = []
    
    for i in range(1, 74):  # 1 to 73 inclusive
        url = f"{base_url}d-{i:04d}.htm"  # Formats as d-0001, d-0002, etc.
        topics.append(url)
    
    return topics


def get_topic_title_and_content(url):
    """Extract title and content from a topic page."""
    soup = fetch_page(url)
    if not soup:
        return None, ""
    
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
    
    # Clean the navigation header and footer
    content = clean_content(content)
    
    # Try to extract topic title (usually the first meaningful line after cleaning)
    topic_title = None
    if content:
        content_lines = content.split('\n')
        # First non-empty line is usually the topic
        for line in content_lines:
            if line and len(line) > 2:
                topic_title = line
                break
    
    if not topic_title:
        topic_title = f"Topic {url.split('/')[-1]}"
    
    return topic_title, content


def scrape_ibnsereen():
    """Main scraping function."""
    print("="*70)
    print("Ibn Sirin Dream Interpretation Scraper")
    print("="*70)
    
    print(f"\nGenerating topic URLs (d-0001 to d-0073)...")
    topic_urls = get_all_topic_urls()
    print(f"✓ Total topics to scrape: {len(topic_urls)}\n")
    
    output_file = 'ibnsereen_dreams.json'
    total_topics = 0
    
    # Initialize empty JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('[\n')
    
    # Process each topic
    for i, url in enumerate(topic_urls, 1):
        topic_title, content = get_topic_title_and_content(url)
        
        if topic_title is None:
            print(f"[{i}/{len(topic_urls)}] ⚠ Failed to fetch {url}")
            continue
        
        print(f"[{i}/{len(topic_urls)}] {topic_title}")
        
        # Create entry
        entry = {
            'topic': topic_title,
            'url': url,
            'content': content
        }
        
        # Append to file immediately
        with open(output_file, 'a', encoding='utf-8') as f:
            if total_topics > 0:
                f.write(',\n')
            json.dump(entry, f, ensure_ascii=False, indent=2)
            # Flush every 10 topics
            if total_topics % 10 == 9:
                f.flush()
        
        total_topics += 1
        
        # Be polite to the server
        time.sleep(0.5)
    
    # Close JSON array
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('\n]')
    
    # Print summary
    print("\n" + "="*70)
    print(f"✓ SCRAPING COMPLETE!")
    print(f"✓ Total topics scraped: {total_topics}")
    print(f"✓ Output file: {output_file}")
    print("="*70)
    
    return total_topics


def show_sample(num_samples=5):
    """Display sample entries from the database."""
    try:
        with open('ibnsereen_dreams.json', 'r', encoding='utf-8') as f:
            database = json.load(f)
        
        if not database:
            print("No data to show")
            return
        
        print(f"\n📋 Sample entries (first {min(num_samples, len(database))}):\n")
        for i, entry in enumerate(database[:num_samples], 1):
            print(f"{i}. Topic: {entry['topic']}")
            print(f"   URL: {entry['url']}")
            print(f"   Content preview: {entry['content'][:100]}...")
            print()
    except:
        pass


def main():
    """Entry point."""
    try:
        total = scrape_ibnsereen()
        show_sample()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
