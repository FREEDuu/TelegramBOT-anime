import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.webdriver.chrome.service import Service

def setup_chromium_with_adblock():
    # Path to ChromeDriver (verify with `which chromedriver`)
    chromedriver_path = "/usr/bin/chromedriver"

    # Path to Brave browser binary
    brave_path = "/usr/bin/brave-browser"

    # Configure Selenium to use Brave
    options = Options()
    options.binary_location = brave_path  # Set Brave as the browser
    options.add_argument("--start-maximized")  # Open browser maximized
    options.add_argument("--incognito")  # Open in incognito mode
    options.add_argument("--no-sandbox")  # Bypass sandbox issues
    options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker
    options.add_argument("--disable-gpu")  # Disable GPU rendering (useful for headless mode)

    # Start the WebDriver service
    service = Service(chromedriver_path)

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver
def scrape_website(urls):
    """Scrapes titles, descriptions, and genres from a list of URLs and saves the data to a JSON file."""

    driver = setup_chromium_with_adblock()  # Or any other browser driver you prefer
    all_data = []
    count = 0
    for url, img in urls.items():
        try:
            print(f"\n🔹 ({count}/{len(urls)}) Trying URL: {url}")
            driver.get(url)
            count+= 1
            
            try:
                leggi_tutto_span = driver.find_element(By.CLASS_NAME,"read-more")
                leggi_tutto_span.click()
            except Exception as e:
                print(f"⚠️ 'Read More' button not found or clickable: {e}")
            try:
                text_specs = ''
                specs = driver.find_element(By.CLASS_NAME,"features")
                for child in specs.find_elements(By.XPATH, ".//*"): # Select all the children of the div, including nested ones
                #for child in div.find_elements(By.CSS_SELECTOR, "*"): # Select all the children of the div, including nested ones
                    text = child.text.strip()
                    if text:  # Add the text only if it's not empty after stripping whitespace
                        text_specs += text
                print('\n specifiche :' , text_specs)
            except Exception as e:
                print(f"⚠️ 'Read More' button not found or clickable: {e}")

            title = url
            description = "[EMPTY]"

            try:
                div_title=driver.find_element(By.CLASS_NAME, "title")
                title = div_title.find_element(By.TAG_NAME, "h1").text.strip()
                print(f"🎬 Title: {title}")
            except Exception as e:
                print(f"⚠️ Error getting title: {e}")

            try:
                div_descr=driver.find_element(By.CLASS_NAME, "plot")
                description = div_descr.find_element(By.TAG_NAME, "p").text.strip()
                print(f"📜 Description: {description}")
            except Exception as e:
                print(f"⚠️ Error getting description: {e}")

            try:
                genre_app = ''
                span_genre=driver.find_elements(By.CLASS_NAME, "genre")
                for genre_tag in span_genre:

                    genre_app +=' ' + genre_tag.find_element(By.TAG_NAME, "a").text.strip()
                print(f"🎭 Genre: {genre_app}")
            except Exception as e:
                print(f"⚠️ Error getting genre: {e}")

            all_data.append({"url": url, "title": title, "description": description, "genre": genre_app, "specs": text_specs})
            genre_app = ''
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")


    driver.quit()  # Close the browser after processing all URLs
    write_json(all_data, "scraped_Films.json") # Call the function to write data to JSON
    print("Data saved to scraped_data.json")


def write_json(data, filename):
    """Writes the scraped data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # Use ensure_ascii=False for proper UTF-8 encoding


    


def get_parent_hrefs_with_current_src(json_file):
    """
    Reads a JSON file, extracts 'parentHref' and 'currentSrc' from each object,
    and returns them in a dictionary where keys are parentHref and values are currentSrc.
    """

    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file}'.")
        return None

    result = {}
    for item in data:
        parent_href = item.get("parentHref")
        current_src = item.get("currentSrc")

        if parent_href and current_src:  # Ensure both exist before adding
            result[parent_href] = current_src

    return result

# Esempio di utilizzo:
percorso_file = "imgFilm.json"  # Sostituisci con il percorso del tuo file

lista_url = get_parent_hrefs_with_current_src(percorso_file)

if lista_url:  # Check if the list is not None
    print("URL trovati:")
else:
    print("Nessun URL trovato o errore durante la lettura del file.")

# Example of how to use the returned list in another function
def process_urls(urls):
    if urls:
        print("Processing URLs...")
        scrape_website(urls)
    else:
        print("No URLs to process.")

process_urls(lista_url)

