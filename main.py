from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import threading
from os import getenv
from string import digits

def check_name_mail(data: list):
    for name in data:
        if '_' in name or ' ' in name or name[0] in digits:
            data.remove(name)
    return data

def init_file(name: str, driver: webdriver.Chrome):
    username = getenv('USERNAME') 
    adres = f'C:\\Users\\{username}\\Desktop\\out_file.txt'
    mesenge = driver.find_element('id', 'alertSuccess')
    chars = mesenge.text
    chars = chars.replace('\n', ' ')
    if chars == 'Адрес существует Электронная почта не одноразовая':
        out = 'valid'
    else:
        out = '-'
    with open(adres, '+a') as output:
        output.writelines(f'mail: {name}\tstatus: {out}\n')

def search(mail_name: str, driver: webdriver.Chrome):
    search = driver.find_element('class name', 'cd-input')
    search.send_keys(mail_name)
    btn = driver.find_element('id', 'uploadButton')
    acctions = ActionChains(driver)
    acctions.click(btn).perform()
    sleep(3)
    init_file(mail_name, driver)
    search.clear()

def window_gmail_first(data: list, driver: webdriver.Chrome, URL: str):
    driver.get(URL)
    mid_num = (len(data) - 1) // 2
    for i in range(0, mid_num):
        name = data[i] + '@gmail.com'
        search(name, driver)
    driver.quit()

def window_gmail_last(data: list, driver: webdriver.Chrome, URL: str):
    driver.get(URL)
    mid_num = (len(data) - 1) // 2
    for i in range(len(data) - 1, mid_num - 1, -1):
        name = data[i] + '@gmail.com'
        search(name, driver)
    driver.quit()

def window_inbox_first(data: list, driver: webdriver.Chrome, URL: str):
    driver.get(URL)
    mid_num = (len(data) - 1) // 2
    for i in range(0, mid_num):
        name = data[i] + '@inbox.me'
        search(name, driver)
    driver.quit()
    
def window_inbox_last(data: list, driver: webdriver.Chrome, URL: str):
    driver.get(URL)
    mid_num = (len(data) - 1) // 2
    for i in range(len(data) - 1, mid_num - 1, -1):
        name = data[i] + '@inbox.me'
        search(name, driver)
    driver.quit()

def create_matrix(data: list):
    num = (len(data) - 1) // 2
    new_data = [[data[i] for i in range(num * j, num * (j + 1))] for j in range(2)]
    for last in range(num * 2, len(data)):
        new_data[1].append(data[last])
    return new_data

def main():
    timer = time()
    functions = [window_gmail_first, window_gmail_last, window_inbox_first, window_inbox_last]
    URL = 'https://products.aspose.app/email/ru/checker?email=&email='
    name_file = input('Введите  полный/абсолютный путь к файлу с почтами: ')
    with open(name_file, 'r') as input_file:
        data = input_file.readlines()
        temp = [line.split('|')[1].strip() for line in data if line != '\n']
    new_data = create_matrix(check_name_mail(temp))
    drivers = []
    for _ in range(8):
        temp = webdriver.Chrome()
        drivers.append(temp)
    threads = []
    for index in range(len(drivers)):
        if index % 2 == 0: i = 0
        else: i = 1
        thread = threading.Thread(target=functions[index // 2], args=(new_data[i], drivers[index], URL))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    print(time() - timer)
    
if __name__ == '__main__':
    main()