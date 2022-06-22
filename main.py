import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os


def get_data_follower(card):
    try:
        name = card.find_element_by_xpath('.//span').text
    except:
        return None
    link = card.find_element_by_xpath('.//a[@role="link"]').get_attribute('href')
    result = (name, link)
    return result


username = input('Enter write a nickname, whom the subscribers need to parse: ')

options = webdriver.ChromeOptions()
# options.add_argument("headless")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.maximize_window()
driver.get('https://twitter.com/i/flow/login')
time.sleep(2)

email_input = driver.find_element_by_xpath('//input[@autocomplete="username"]')
email_input.send_keys(os.environ.get('twitter_email'))
email_input.send_keys(Keys.RETURN)
time.sleep(1)

try:
    name_input = driver.find_element_by_xpath('//input[@name="text"]')
    name_input.send_keys(os.environ.get('twitter_username'))
    name_input.send_keys(Keys.RETURN)
    time.sleep(1)
except:
    pass

password_input = driver.find_element_by_xpath('//input[@name="password"]')
password_input.send_keys(os.environ.get('twitter_password'))
password_input.send_keys(Keys.RETURN)
time.sleep(1)

search_input = driver.find_element_by_xpath('//input[@data-testid="SearchBox_Search_Input"]')
search_input.send_keys(username)
time.sleep(1)

driver.find_elements_by_xpath('//div[@data-testid="typeaheadResult"]')[1].click()
time.sleep(2)

driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]'
                             '/div/div/div/div/div[4]/div[2]/a').click()
time.sleep(2)

followers_ids = list()
result = list()
last_position = driver.execute_script('return window.pageYOffset;')

with open('result.csv', mode='w', newline='', errors='ignore') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        (
            'username',
            'link'
        )
    )

while True:
    cards = driver.find_elements_by_xpath('//div[@data-testid="cellInnerDiv"]')
    for card in cards:
        data = get_data_follower(card)
        if data is None:
            continue
        else:
            follower_id = ''.join(data)
            if follower_id not in followers_ids:
                with open('result.csv', mode='a', newline='', errors='ignore') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        (
                            data[0],
                            data[1]
                        )
                    )
                followers_ids.append(follower_id)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    curr_position = driver.execute_script('return window.pageYOffset;')
    if curr_position == last_position:
        break
    else:
        last_position = curr_position

driver.close()
