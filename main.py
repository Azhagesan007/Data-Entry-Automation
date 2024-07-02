from bs4 import BeautifulSoup
import requests
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfoREQ8bgB2J6QEGzihBeluEAkq-xNOPnI4QjGSokybIwBi-w/viewform?usp=sf_link"

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,ta;q=0.8"
}

rent_url = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.84757638973728%2C%22east%22%3A-122.3179730546875%2C%22south%22%3A37.70293677465982%2C%22west%22%3A-122.5486859453125%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"

response = requests.get(url=rent_url, headers=header)
data = response.text
# print("data", data)
soup = BeautifulSoup(data, "lxml")
# print("soup",soup.text)
price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine-srp-8-102-0__sc-16e8gqd-1 vjmXt")
price_data = []
for i in price:
    # print(i.text)
    text = i.text
    k = text.strip().split("+")
    lenk = len(k)
    if lenk == 1:
        j = k[0].split("/")
        price_data.append(j[0])
    else:
        price_data.append(k[0])

new_price_data = [j.replace(",", "") for j in price_data]
print(new_price_data)

address = soup.find_all(name="a", class_="StyledPropertyCardDataArea-c11n-8-102-0__sc-10i1r6-0 klMkvj property-card-link")
# print(len(address))
address_data = [a.text for a in address]
print(address_data)
print(len(address_data))

link = []
for n in address:
    href = n["href"]
    if href[0] == "/":
        href = "https://www.zillow.com" + href
        link.append(href)

    else:
        link.append(href)


length = len(link)

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url=form_url)

input1 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
input2 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
input3 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
submit = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')
for g in range(length):
    input1 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input2 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input3 = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div')

    # input1.click()
    input1.send_keys(address_data[g])
    # input2.click()
    input2.send_keys(price_data[g])
    # input3.click()
    input3.send_keys(link[g])
    submit.click()

    another = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another.click()
    sleep(1)

input()
