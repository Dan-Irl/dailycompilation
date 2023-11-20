from selenium import webdriver
import time

def bypass_cloudflare_with_selenium(url):
    # Initialize the WebDriver (example using Chrome)
    driver = webdriver.Chrome()

    # Go to the URL
    driver.get(url)

    # Wait for Cloudflare's anti-bot page (adjust the time as needed)
    # time.sleep(10)

    # Now you can scrape the page or interact with it as needed
    content = driver.page_source

    # Close the WebDriver
    driver.quit()

    return content

url = "https://webscraper.io/test-sites/e-commerce/allinone/product/620"
content = bypass_cloudflare_with_selenium(url)
print(content)
