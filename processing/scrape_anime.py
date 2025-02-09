from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser_options = ChromeOptions()
browser_options.headless = True
letters='QRSTUVWXYZ'
driver = Chrome(options=browser_options)
# Navigate to the webpage
url = "https://www.anisaturn.com/animelist"  # Replace with the target URL
try:
    for letter in letters:
        driver.get(url+f'?page=0&letter={letter}')
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        last_page = 0
        try:
            last_page = int(driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.CSS_SELECTOR, "*")[-1].text)
        except:
            pass
        try:
            for page_count in range(last_page+1):
                print(f'scraping letter {letter} at page {page_count} till {last_page}')
                driver.get(url+f'?page={page_count}&letter={letter}')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Find all <div> elements with the class "info-archivio"

                divs = driver.find_elements(By.CLASS_NAME, "info-archivio")

                anime_dict = {}

                for index, div in enumerate(divs):
                    # Find the first <a> tag and get its href
                    try:
                        a_tags = div.find_elements(By.TAG_NAME, "a")
                        href = a_tags[0].get_attribute("href")
                        anime_title = a_tags[0].text
                        genre = [ element.text for element in a_tags[1:-1] ]
                    except:
                        print("No <a> tag found.")

                    try:
                        p_tag = div.find_element(By.TAG_NAME, "p")
                        p_text = p_tag.text
                    except:
                        print("No <p> tag found.")
                    
                    anime_dict[href] = {
                        'title' : anime_title, 
                        'description' : p_text,
                        'link' : href,
                        'genre' : genre
                    }

                images = driver.execute_script("""
                    return Array.from(document.getElementsByTagName('img')).map(img => ({
                src: img.src,
                currentSrc: img.currentSrc,
                naturalWidth: img.naturalWidth,
                complete: img.complete,
                parentHref: img.closest('a')?.href || 'No parent link'
                }));
                """)
                # Print image info
                for i, img in enumerate(images):

                    if img['parentHref'] in anime_dict.keys():
                        temp = anime_dict[img['parentHref']]
                        temp['image'] = img['src']
                        anime_dict[img['parentHref']] = temp
                
                print(anime_dict)
        except Exception as e:
            print(e)
        
finally:
    # Quit the driver
    driver.quit()