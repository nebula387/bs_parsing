from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

# START_URL = 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA'
START_URL = 'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki'
html = ''

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

driver.get(START_URL)
driver.implicitly_wait(100)
driver.maximize_window()

page = 1
# Для того, чтоб подгрузить все карточки, нужно проскроллить до самого низу, что не сделаешь через bs4

def scrollDownToButton():
    height = driver.execute_script("return document.body.offsetHeight")
    y = 1000
    while y <= height:
        sleep(1)
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 1000
    return
try:
    while True:
        # Нужно поставить насильно sleep, т.к без него сильно быстро происходит пролистывание страниц
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-card-list")))
        scrollDownToButton()
        cards = driver.find_elements(By.CSS_SELECTOR, "article.product-card")
        for card in cards:
            html += card.get_attribute("outerHTML")

        buttonNext = driver.find_element(By.CSS_SELECTOR, ".pagination-next")
        if not buttonNext:
            break

        actions.move_to_element(buttonNext)
        actions.perform()
        buttonNext.click()
        page += 1
except Exception as ex:
    print(ex)

sleep(5)
print('Exit url: ', driver.current_url)
driver.quit()

with open('wildberries-noutbuk_1.html', 'w', encoding='utf-8') as f:
    f.write(html)
# buttonNext.click()