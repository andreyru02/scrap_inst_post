from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import random
from bs4 import BeautifulSoup as bs
import json
import sys

import config


class Inst:
    def __init__(self, url_inst, login, password):
        self.url = url_inst
        self.login = login
        self.password = password
        self.data = {'data': {'items': []}}
        self.driver = webdriver.Firefox()

    def auth_inst(self):
        print(datetime.today().strftime(f'%H:%M:%S | Выполняется авторизация в Instagram.'))
        self.driver.get(self.url)
        time.sleep(random.randrange(3, 5))
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
        self.driver.find_element_by_name('username').send_keys(self.login)
        passwd = self.driver.find_element_by_name('password')
        passwd.send_keys(self.password)
        passwd.send_keys(Keys.ENTER)
        time.sleep(5)
        try:
            self.driver.find_element_by_class_name('gmFkV')
        except NoSuchElementException:
        	try:
        		err = self.driver.find_element_by_class_name('eiCW-').text
        		self.driver.quit()
        		sys.exit(err + '\nРабота завершена с ошибкой.')
        	except NoSuchElementException:
        		err = self.driver.find_element_by_class_name('O4QwN').text
        		self.driver.quit()
        		sys.exit(err + '\nРабота завершена с ошибкой.')
        		

        time.sleep(10)
        print(datetime.today().strftime(f'%H:%M:%S | Авторизация в Instagram выполнена.'))

    def scrap_post(self, url, user_count):
        self.driver.get(url)
        soup = bs(self.driver.page_source, 'html.parser')
        time.sleep(5)
        count = 0
        post_links = []

        for elem in soup.select('.ySN3v'):
            for el in elem.find_all('a'):
                link = el.get('href')
                post_links.append(config.URL + link)

        for post in post_links:
            user_dict = {}
            self.driver.get(post)
            time.sleep(3)
            soup = bs(self.driver.page_source, 'html.parser')

            if soup.find('video', class_='tWeCl') is not None:
                count += 1
                print('Пост видео, пропускаем.')
                if count == user_count:
                    break
                continue

            # img
            img = soup.find('img', class_='FFVAD').get('src')

            # title
            title = soup.find('div', class_='C4VMK').find_all('span')[-1].text

            # like
            find_like = soup.find_all('a', class_='zV_Nj')
            like = find_like[-1].find('span').text

            user_dict['url'] = url
            user_dict['img'] = img
            user_dict['title'] = title
            user_dict['like'] = like
            self.write_json(user_dict)

            count += 1
            if count == user_count:
                break

    def close_browser(self):
        print('Работа завершена.')
        self.driver.quit()

    def write_json(self, info):
        self.data['data']['items'].append(info)
        with open('data.json', 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
