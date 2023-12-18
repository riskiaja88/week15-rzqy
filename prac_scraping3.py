from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.get("https://www.google.com")
url = "https://www.spacex.com/launches/"
driver.get(url)
sleep(5)

sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(10)

req = driver.page_source
driver.quit()
soup = BeautifulSoup(req, 'html.parser')

images = soup.select('img')
for image in images:
    print(image['src'])