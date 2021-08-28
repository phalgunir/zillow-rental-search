import time
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

zillow_url = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.5929740805664%2C%22east%22%3A-122.2736839194336%2C%22south%22%3A37.71936832595496%2C%22north%22%3A37.831172311619135%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D'
google_form_url = 'YOUR GOOGLE FORM URL'
chrome_driver_path = '/Applications/chromedriver'


# TODO: scrape zillow data using BeautifulSoup to get rental addresses, prices and links
zillow_request_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
}
zillow_response = requests.get(zillow_url, headers=zillow_request_headers)
soup = BeautifulSoup(zillow_response.text, 'html.parser')

addresses = [address.getText().split(' | ')[-1] for address in soup.select('.list-card-addr')]
pprint(addresses)
prices = [price.getText().split('+')[0] for price in soup.select('.list-card-price')]
pprint(prices)
links = []
for link in soup.select('.list-card-info a'):
    url = link.get('href')
    if url[0] == '/':
        url = 'https://www.zillow.com' + url
    links.append(url)
pprint(links)


# TODO: fill google form using Selenium
driver = webdriver.Chrome(chrome_driver_path)
for i in range(len(addresses)):
    driver.get(google_form_url)
    time.sleep(2)

    address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[i])
    price_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices[i])
    link_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links[i])
    time.sleep(1)
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_button.click()
    time.sleep(2)

driver.quit()
