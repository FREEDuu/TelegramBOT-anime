from selenium_util.utils import setup_chromium_with_adblock, scrape_years, scrape_endpoint

if __name__ == "__main__":

    driver = setup_chromium_with_adblock()
    #scrape_years(driver, 'https://streamingcommunity.lu/archivio?type=movie&year=', 2000, 2025)
    scrape_endpoint(driver)