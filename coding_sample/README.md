# lipi-swap

I have used this Python script to scrape data from an Indian administrative database, where names of entities like Panchayats and Blocks are often written in Hindi (Devanagari script). This script uses web scraping techniques to collect data and leverages the `unidecode` library to transliterate Hindi names into English, ensuring compatibility when saved to a CSV file.

This script is built to scrape hierarchical data from Indian datasets (e.g., states, districts, blocks, and panchayats) using `requests` and `BeautifulSoup`. It handles non-Roman scripts like Devanagari by converting them to English equivalents with `unidecode`. The scraped data, including monthly figures, is organized into a structured CSV file using `pandas`. English names remain unchanged, while Hindi names are transliterated for readability and compatibility.

When dealing with datasets containing Devanagari script (e.g., Hindi names), saving them directly to a CSV can result in encoding issues or unreadable characters on systems not configured for non-Roman scripts. Transliteration solves this by converting Hindi characters to their closest English (Roman) equivalents, making the data portable and usable across different platforms.

## Installation

To run **lipi-swap**, you'll need the following Python libraries:

- `requests` - For making HTTP requests
- `beautifulsoup4` - For parsing HTML content
- `pandas` - For handling data and CSV output
- `unidecode` - For transliterating Hindi to English

Install them using pip:

```bash
pip install requests beautifulsoup4 pandas unidecode
```

## Transliteration Example
Here's a simple example of how `unicode` works
```bash
from unidecode import unidecode
print(unidecode("पंचायत"))  # Output: panchayat
```
In the above python script, this has been embedded into a scraping code. 

---
Fun stuff: The word `lipi (लिपि)` refers to `script`; and `swap` refers to translation. Hence, the repo name!

### Other references
[Unicode by takluvyer](https://github.com/takluyver/Unidecode) - Check this out in case you want to know more about the usage of `unicode`. 
