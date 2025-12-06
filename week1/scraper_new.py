from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def fetch_website_contents_dynamic(url):
    """Fetch content from JavaScript-rendered websites using Selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else "No title found"
        
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""
        return (title + "\n\n" + text)[:2_000]
    finally:
        driver.quit()

def fetch_website_links_dynamic(url):
    """Fetch links from JavaScript-rendered websites using Selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        links = [link.get("href") for link in soup.find_all("a")]
        return [urljoin(url, link) for link in links if link]
    finally:
        driver.quit()
