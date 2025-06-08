from playwright.sync_api import sync_playwright, Playwright, Page
import time
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph
import json
from bs4 import BeautifulSoup
import ollama
from langchain.output_parsers import PydanticOutputParser


# Utility function to get text safely
def safe_text(el):
    return el.text.strip() if el else ""


def open_google_maps(page: Page):
    """Opens Google Maps."""
    page.goto("https://www.google.com/maps", timeout=60000)
    page.wait_for_selector("id=searchbox")
    return page

def scroll_results_feed(page: Page, max_scrolls: int = 30, wait_time: float = 1.5):
    print("📜 Scrolling inside the listings feed panel...")

    last_count = 0
    stagnant_scrolls = 0

    for scroll_round in range(max_scrolls):
        # Count listings
        count = page.locator("div.TFQHme").count()
        print(f"🔁 Scroll {scroll_round+1}: {count} listings visible")

        # Scroll the feed container using JS
        page.evaluate("""
            () => {
                const feed = document.querySelector('[role="feed"]');
                if (feed) {
                    feed.scrollBy(0, feed.scrollHeight);
                }
            }
        """)

        time.sleep(wait_time)

        new_count = page.locator("div.TFQHme").count()
        if new_count == last_count:
            stagnant_scrolls += 1
            if stagnant_scrolls >= 3:
                print("✅ No new listings loaded after 3 scrolls. Done.")
                break
        else:
            stagnant_scrolls = 0
        last_count = new_count

    return new_count

def extract_ai_data(prompt: str, html_content: str):
    """Extracts data from HTML using AI."""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": html_content}
        ]
    )
    try:
        content = response['message']['content']
        if '```json' in content:
            json_content = content.split('```json')[1].split('```')[0]
        else:
            json_content = content
        return json_content
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON response")
        return None

def parse_overview_data(page: Page, df: pd.DataFrame):
    """Parses the overview data from the page."""
    print("This functionality parses and scrapes the overview data from the page including scrolls") 
    all_queries_data = []
    # for each row in df, scrape the overview data, after each search clear the search box and then search for the next query
    for index, row in df.iterrows():
        query = row['search_query']
        user_name = row['UserName']
        print(f"Searching: {index+1}:{query} ")
        open_google_maps(page)
        search_box = page.get_by_role("combobox")
        search_box.wait_for(state="visible", timeout=10000)
        search_box.click()
        search_box.fill(query)
        search_box.press("Enter")
        time.sleep(5)
        
        # fetch all the results from the loaded page and display count of results 
        print("📜 Scrolling to load all listings...")
        
        final_count = scroll_results_feed(page)        
        print(f"Final count of listings: {final_count}")
        
        # Fetch the html content of the page
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Find all business cards
        cards = soup.select('div.Nv2PK.THOPZb.CpccDe')
        print(f"📦 Found {len(cards)} business cards")
        for card in cards[:3]:
            # for each card using AI prompting, fetch the data 
            prompt = """
                    From the provided HTML of a Google Maps search result card, extract the following:
                    - name
                    - address
                    - rating
                    - number of reviews
                    - price range
                    - type of restaurant or service
                    - maps URL
                    
                    Return only JSON formatted object with these fields. Do not include any other text or comments.
                    """
            html_card = str(card)
            data = extract_ai_data(prompt, html_card)
            all_queries_data.append(data)
            
        # clear the search box
        search_box.clear()
        return all_queries_data

def scrape_google_maps(playwright: Playwright, query: str, headless: bool = False) -> str:
        """Searches Google Maps and returns page HTML for a given query."""

        browser = playwright.chromium.launch(headless=False, slow_mo=100,  executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        user_choice = 'overview'
        # create a df with search query and additional columns like 
        df = pd.DataFrame(columns=['search_query', 'UserName'])
        #provide sample values
        df.loc[0] = ['Vegetarian Restaurants near Bangalore, Bellandur', 'John Doe']        
        
        if user_choice == 'overview':
            data = parse_overview_data(page, df)
            print(data)
        else: 
            pass
        
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        html = scrape_google_maps(playwright, "Vegetarian Restaurants near Bangalore, Bellandur", headless=False)