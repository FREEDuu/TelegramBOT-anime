from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from save_tvjson import save_urls_to_json

def save_image_data_to_json(data, filename):
    """Saves 'parentHref' and 'currentSrc' from image data to a JSON file."""

    extracted_data = []
    for item in data:
        extracted_data.append({
            "parentHref": item.get("parentHref"),  # Use .get() to handle missing keys
            "currentSrc": item.get("currentSrc")
        })

    try:
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(extracted_data, outfile, indent=4, ensure_ascii=False)
        print(f"Image data saved to '{filename}'.")
    except Exception as e:
        print(f"Error writing to output file: {e}")


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

def scroll_and_wait(max_scrolls):  # Customizable parameters
    """Scrolls down the page, waits for content to load, and repeats."""

    for _ in range(max_scrolls):  # Limit the number of scrolls to prevent infinite loop
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for content to load (using a better approach than time.sleep())
        
            # If you want to stop scrolling if the element is not found, uncomment the next line:
            # break  # Exit the loop if the element isn't found
        time.sleep(0.2)
        # Small pause between scrolls (optional, adjust as needed)


driver = setup_chromium_with_adblock()
# Navigate to the webpage
url = "https://streamingcommunity.paris/archivio?sort=views&type=movie"  # Replace with the target URL
try:
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    scroll_and_wait(100)
    print(f'scraping . . . ')

    divs = driver.find_elements(By.CLASS_NAME, "slider-item")
    print('divs', divs, len(divs))
    Tv_series_list = []

    """
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
    """


    images = driver.execute_script("""
        return Array.from(document.getElementsByTagName('img')).map(img => ({
    src: img.src,
    currentSrc: img.currentSrc,
    naturalWidth: img.naturalWidth,
    complete: img.complete,
    parentHref: img.closest('a')?.href || 'No parent link'
    }));
    """)
    save_image_data_to_json(images, "imgFilm.json")
    # Print image info
except Exception as e:
    print(e)
        
finally:
    # Quit the driver
    driver.quit()