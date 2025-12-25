# Dream Interpretation Scraper Scripts

This folder contains Python scripts for scraping and cleaning Arabic dream interpretation data from various sources.

## 📁 Scripts Overview

### 1. `scrapper_v2.py`
**Purpose**: Main scraper for extracting dream interpretation topics from the complete Arabic alphabet.

**Features**:
- Scrapes dream interpretations organized by Arabic letters (حرف الألف to حرف الياء)
- Extracts topics from 28 letter pages covering the entire Arabic alphabet
- Cleans content by removing navigation headers and footers
- Handles Arabic text encoding (windows-1256)
- Saves data to `dreams_database.json`

**Usage**:
```bash
python scrapper_v2.py
# OR with specific Python environment:
D:\anaconda3\envs\torch\python.exe scrapper_v2.py
```

**Output Format**:
```json
[
  {
    "topic": "Dream topic title",
    "url": "https://mktbtk.com/dir/nab/...",
    "content": "Dream interpretation content..."
  }
]
```

---

### 2. `Ibnsereen_scrapper.py`
**Purpose**: Specialized scraper for Ibn Sirin (ابن سيرين) dream interpretations.

**Features**:
- Scrapes dream interpretations attributed to Ibn Sirin
- Includes content cleaning specific to Ibn Sirin's formatting
- Handles Arabic letters navigation (28 letters)
- Removes duplicates and navigation elements
- Saves data to `dreams_database_ibnsereen.json`

**Usage**:
```bash
python Ibnsereen_scrapper.py
```

---

### 3. `Ibnshahin_scrapper.py`
**Purpose**: Specialized scraper for Ibn Shaheen (ابن شاهين) dream interpretations.

**Features**:
- Scrapes dream interpretations attributed to Ibn Shaheen
- Removes "موسوعة تفسير الرؤى والأحلام" prefix from topics
- Handles Ibn Shaheen-specific content formatting
- Extracts Quranic verse interpretations
- Saves data to `dreams_database_ibnshahin.json`

**Usage**:
```bash
python Ibnshahin_scrapper.py
```

---

### 4. `clean_database.py`
**Purpose**: Post-processing script to clean scraped data.

**Features**:
- Removes navigation headers (حرف الألف, حرف الباء, etc.)
- Strips footer information (ahlam.NoorDubai.Tv, Tafserahlam.com, Mktbtk.com)
- Removes year markers (2026, etc.)
- Cleans Quranic verse references
- Processes JSON database files

**Usage**:
```bash
python clean_database.py
```

**Default Behavior**:
- Reads: `dreams_database.json`
- Outputs: `dreams_database_cleaned.json`

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install requests beautifulsoup4
```

### Running the Scrapers

1. **Scrape all dreams** (recommended):
   ```bash
   python scrapper_v2.py
   ```

2. **Scrape specific scholar**:
   ```bash
   python Ibnsereen_scrapper.py
   # OR
   python Ibnshahin_scrapper.py
   ```

3. **Clean the database**:
   ```bash
   python clean_database.py
   ```

---

## 📊 Data Structure

All scrapers output JSON files with the following structure:

```json
[
  {
    "topic": "Dream symbol or topic",
    "url": "Source URL",
    "content": "Interpretation text in Arabic"
  }
]
```

---

## 🔧 Technical Details

### Encoding
- All scripts use `windows-1256` encoding for proper Arabic text handling
- Output files use UTF-8 encoding

### Rate Limiting
- Scripts include delays between requests (0.5-1 second)
- Prevents server overload and ensures polite scraping

### Error Handling
- Timeout: 15 seconds per request
- User-Agent header to avoid blocking
- Graceful error messages for failed requests

---

## 📝 Notes

- **scrapper_v2.py** is the most comprehensive and recommended for general use
- Each scraper targets a specific source or scholar's interpretations
- The clean_database.py script should be run after scraping to remove unwanted headers/footers
- All scripts create separate JSON files to avoid overwriting data

---

## 🐛 Troubleshooting

**Issue**: Script hangs or times out
- **Solution**: Check internet connection, the website might be down

**Issue**: Encoding errors in output
- **Solution**: Ensure you're viewing the JSON file with UTF-8 encoding

**Issue**: Missing topics
- **Solution**: Re-run the scraper, some topics might have been skipped due to network issues

---

## 📜 Generated Files

- `dreams_database.json` - Output from scrapper_v2.py
- `dreams_database_ibnsereen.json` - Output from Ibnsereen_scrapper.py
- `dreams_database_ibnshahin.json` - Output from Ibnshahin_scrapper.py
- `dreams_database_cleaned.json` - Cleaned version after running clean_database.py

---

**Last Updated**: December 2025
