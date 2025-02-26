from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from data_util.utils import save_image_data_to_json, get_parent_hrefs_with_current_src, write_json
from selenium.webdriver.common.by import By
import os

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

def scroll_and_wait(driver, max_scrolls):  # Customizable parameters
    """Scrolls down the page, waits for content to load, and repeats."""

    for _ in range(max_scrolls):  # Limit the number of scrolls to prevent infinite loop
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scrape_url(driver, url, year):
    try:
        driver.get(url+year)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_and_wait(driver, 100)
        print(f'scraping . . . ')

        divs = driver.find_elements(By.CLASS_NAME, "slider-item")
        print('divs', divs, len(divs))
        Tv_series_list = []

        
        for index, div in enumerate(divs):
            try:
                a_tag = div.find_element(By.TAG_NAME, "a")  # Find the first 'a' tag
                href = a_tag.get_attribute("href")
                print('\nScarping . . .', href)
                Tv_series_list.append(href)
                try:
                    # Find the image within the current 'a' tag.  There are several ways to do this:
                    # 1. If the image is a direct child of the <a> tag:
                    img_tag = a_tag.find_element(By.TAG_NAME, "img")

                    # 2. If the image is nested deeper within the <a> tag (e.g., inside another div):
                    # img_tag = a_tag.find_element(By.CSS_SELECTOR, "div.image-container img")  # Example CSS selector
                    # img_tag = a_tag.find_element(By.XPATH, "//div[@class='image-container']//img") # Example XPATH selector

                    # 3. If the image has a specific class or ID:
                    # img_tag = a_tag.find_element(By.CLASS_NAME, "show-poster") # Example class selector
                    # img_tag = a_tag.find_element(By.ID, "poster-image") # Example id selector



                    image_src = img_tag.get_attribute("src")  # Get the 'src' attribute of the image
                    print("Image Source:", image_src)

                except Exception as e:
                    print(e)
            except:
                print("No <a> tag found.")
        


        images = driver.execute_script("""
            return Array.from(document.getElementsByTagName('img')).map(img => ({
        src: img.src,
        currentSrc: img.currentSrc,
        naturalWidth: img.naturalWidth,
        complete: img.complete,
        parentHref: img.closest('a')?.href || 'No parent link'
        }));
        """)
        save_image_data_to_json(images, year+"TV.json")
        # Print image info
    except Exception as e:
        print(e)
            
def scrape_years(driver, url, year_start, year_end):
    try:
        for year in range(year_start, year_end+1):
            scrape_url(driver, url, str(year))
    except Exception as e:
        print(e)

def scrape_website(driver, urls, file):
    """Scrapes titles, descriptions, and genres from a list of URLs and saves the data to a JSON file."""

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
            print(file)
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")

    write_json(all_data, '/home/francesco/Desktop/temp/TelegramBOT-anime/data-cleaned/TV-series/'+file)
    print("Data saved")

def scrape_endpoint(driver):

    directory_path = '/home/francesco/Desktop/temp/TelegramBOT-anime/data/TV-series/'
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    for file in files:
        urls = get_parent_hrefs_with_current_src('/home/francesco/Desktop/temp/TelegramBOT-anime/data/TV-series/'+file)
        scrape_website(driver, urls, file)