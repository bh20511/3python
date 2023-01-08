
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 引入送出按鍵
from selenium.webdriver.common.keys import Keys
import time
import os
import wget


driver_path = 'chromedriver.exe'
url = 'https://www.instagram.com/'
driver = webdriver.Chrome(driver_path)
driver.get(url)

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)

password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

username.clear()
password.clear()

username.send_keys('ig帳號')
password.send_keys('ig密碼')
login = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div')
login.click()

search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input'))
)
keywords = '#貓'
search.send_keys(keywords)
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(1)
search.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))
)
imgs = driver.find_elements_by_class_name('FFVAD')

path = os.path.join(keywords)
os.mkdir(path)

# if not os.path.exists(path):
#     os.mkdir(keyswords)
count = 0
for img in imgs:
    save_as = os.path.join(path, keywords+str(count)+'.jpg')
    print(img.get_attribute("src"))
    wget.download(img.get_attribute("src"), save_as)
    count += 1
