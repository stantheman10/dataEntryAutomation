from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


FORM_URL = "https://forms.gle/YxN1Bkei29dbYxkF9"
WEBSITE_URL = "https://appbrewery.github.io/Zillow-Clone/"


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


response = requests.get(WEBSITE_URL)
response.raise_for_status()
website_data = response.text

# print(website_data)


soup = BeautifulSoup(website_data, "html.parser")
# print(soup)

properties_prices = soup.find_all(
    name="span", class_="PropertyCardWrapper__StyledPriceLine"
)

for property in properties_prices:
    property = property.text.split("+")[0].split("/")[0].strip()
    # print(property)

property_links = [
    link["href"]
    for link in soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
]

# print(property_links)

property_address = [add.text.strip() for add in soup.find_all(name="address")]

# print(property_address)

driver.get(FORM_URL)
time.sleep(2)

enter_email = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
enter_email.send_keys("YOUR EMAIL" + Keys.ENTER)
time.sleep(2)

pass_enter_email = driver.find_element(
    By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
)
pass_enter_email.send_keys("YOURPASS" + Keys.ENTER)
time.sleep(5)

for i in range(len(properties_prices)):

    address_input = driver.find_element(
        By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )

    price_input = driver.find_element(
        By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )

    link_input = driver.find_element(
        By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )

    address_input.send_keys(property_address[i])
    price_input.send_keys(properties_prices[i])
    link_input.send_keys(property_links[i])

    btn = driver.find_element(
        By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
    )
    btn.click()
    time.sleep(2)
    sbmit_another = driver.find_element(
        By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a"
    )
    sbmit_another.click()
    time.sleep(2)
