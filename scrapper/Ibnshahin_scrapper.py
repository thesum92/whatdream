import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time
import re


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


def clean_ibnshahin_content(content):
    """Remove Ibn Shahin specific headers from content."""
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip the encyclopedia header line
        if line.startswith('موسوعة تفسير الرؤى والأحلام |'):
            continue
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def clean_topic_name(topic_name):
    """Remove encyclopedia prefix from topic name."""
    if not topic_name:
        return topic_name
    
    # Remove the encyclopedia prefix
    prefix = 'موسوعة تفسير الرؤى والأحلام | '
    if topic_name.startswith(prefix):
        topic_name = topic_name[len(prefix):]
    
    return topic_name.strip()


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
    """Get all main topic URLs with their names from the index page."""
    index_url = "https://www.mktbtk.com/dir/Ibnshahin.htm"
    base_url = "http://www.mktbtk.com/dir/ish/"
    
    print(f"Fetching main topics from: {index_url}")
    soup = fetch_page(index_url)
    
    topics = []
    
    if soup:
        # Find all <a> tags inside <p> tags
        for p_tag in soup.find_all('p'):
            for link in p_tag.find_all('a', href=True):
                href = link['href']
                title = link.get_text(strip=True)
                
                # Look for sa-X.htm pattern
                match = re.search(r'sa-(\d+)\.htm', href)
                if match:
                    topic_number = int(match.group(1))
                    full_url = href if href.startswith('http') else urljoin(index_url, href)
                    
                    topics.append({
                        'main_url': full_url,
                        'topic_number': topic_number,
                        'main_topic_name': title
                    })
        
        # Sort by topic number
        topics.sort(key=lambda x: x['topic_number'])
    
    # If parsing failed, fall back to generating URLs
    if not topics:
        print("⚠ Failed to parse index, generating URLs 1-78...")
        for i in range(1, 79):
            url = f"{base_url}sa-{i}.htm"
            topics.append({
                'main_url': url,
                'topic_number': i,
                'main_topic_name': f"Topic {i}"
            })
    
    return topics


def get_subtopics_from_main_page(main_url, topic_number):
    """Extract all subtopic links from a main topic page."""
    soup = fetch_page(main_url)
    if not soup:
        return []
    
    subtopics = []
    seen_urls = set()
    
    # Find all links on the page
    for link in soup.find_all('a', href=True):
        href = link['href']
        title = link.get_text(strip=True)
        
        # Look for subtopic links containing the topic number folder
        # Example: https://mktbtk.com/dir/ish/16/d-0001.htm
        if f'/ish/{topic_number}/' in href and '/d-' in href:
            # Use the full URL from href
            full_url = href if href.startswith('http') else urljoin(main_url, href)
            
            # Skip duplicates
            if full_url in seen_urls:
                continue
            
            seen_urls.add(full_url)
            subtopics.append({
                'url': full_url,
                'title': title
            })
        # Also check for relative paths like "16/d-0001.htm"
        elif re.match(rf'{topic_number}/d-\d+\.htm', href):
            full_url = f"http://www.mktbtk.com/dir/ish/{href}"
            
            if full_url in seen_urls:
                continue
            
            seen_urls.add(full_url)
            subtopics.append({
                'url': full_url,
                'title': title
            })
    
    return subtopics


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
    
    # Clean Ibn Shahin specific headers
    content = clean_ibnshahin_content(content)
    
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
    
    # Clean the topic name
    topic_title = clean_topic_name(topic_title)
    
    return topic_title, content


def scrape_ibnshahin():
    """Main scraping function."""
    print("="*70)
    print("Ibn Shahin Dream Interpretation Scraper")
    print("="*70)
    
    print("\nGenerating main topic URLs (sa-1 to sa-78)...")
    main_topics = get_all_topic_urls()
    print(f"✓ Total main topics: {len(main_topics)}")
    
    output_file = 'ibnshahin_dreams.json'
    total_subtopics = 0
    
    # Initialize empty JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('[\n')
    
    # Process each main topic
    for i, topic_info in enumerate(main_topics, 1):
        main_url = topic_info['main_url']
        topic_number = topic_info['topic_number']
        main_topic_name = topic_info.get('main_topic_name', f"Topic {topic_number}")
        
        print(f"\n{'='*70}")
        print(f"[Main Topic {i}/{len(main_topics)}] {main_topic_name}")
        print(f"{'='*70}")
        print(f"Fetching subtopics from: {main_url}")
        
        # Get all subtopics for this main topic
        subtopic_urls = get_subtopics_from_main_page(main_url, topic_number)
        
        if not subtopic_urls:
            print(f"  ⚠ No subtopics found for topic {topic_number}")
            continue
        
        print(f"✓ Found {len(subtopic_urls)} subtopics")
        
        # Process each subtopic
        for j, subtopic_info in enumerate(subtopic_urls, 1):
            subtopic_url = subtopic_info['url']
            subtopic_title = subtopic_info['title']
            
            print(f"  [{j}/{len(subtopic_urls)}] {subtopic_url.split('/')[-1]}: {subtopic_title[:40]}...", end='')
            
            # Get subtopic content
            topic_title, content = get_topic_title_and_content(subtopic_url)
            
            # Use the title from the link if content extraction fails
            if not topic_title:
                topic_title = subtopic_title if subtopic_title else f"Topic {subtopic_url.split('/')[-1]}"
            
            # Clean the topic title from link as well
            topic_title = clean_topic_name(topic_title)
            
            if not content:
                print(" - ⚠ No content, skipping")
                continue
            
            print(" - ✓")
            
            # Create entry
            entry = {
                'topic': topic_title,
                'url': subtopic_url,
                'main_topic': main_topic_name,
                'main_topic_number': topic_number,
                'content': content
            }
            
            # Write entry to file
            with open(output_file, 'a', encoding='utf-8') as f:
                if total_subtopics > 0:
                    f.write(',\n')
                json.dump(entry, f, ensure_ascii=False, indent=2)
                
                # Flush every 10 subtopics for safety
                if (total_subtopics + 1) % 10 == 0:
                    f.flush()
            
            total_subtopics += 1
            
            # Be polite: wait between requests
            time.sleep(0.5)
        
        print(f"✓ Completed topic sa-{topic_number}: {len(subtopic_urls)} subtopics scraped")
    
    # Close JSON array
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('\n]')
    
    return total_subtopics


def display_preview(output_file='ibnshahin_dreams.json', num_entries=3):
    """Display a preview of the scraped data."""
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n" + "="*70)
        print(f"PREVIEW: First {min(num_entries, len(data))} entries")
        print("="*70)
        
        for i, entry in enumerate(data[:num_entries], 1):
            print(f"\n[{i}] Topic: {entry['topic']}")
            print(f"URL: {entry['url']}")
            print(f"Content preview: {entry['content'][:200]}...")
            print("-" * 70)
        
    except FileNotFoundError:
        print("No data to show")
    except json.JSONDecodeError:
        print("Error reading JSON file")


def main():
    """Main function."""
    try:
        total = scrape_ibnshahin()
        
        print("\n" + "="*70)
        print("✓ SCRAPING COMPLETE!")
        print(f"✓ Total subtopics scraped: {total}")
        print(f"✓ Output file: ibnshahin_dreams.json")
        print("="*70)
        
        # Display preview
        display_preview()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
        print("✓ Progress has been saved to ibnshahin_dreams.json")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
