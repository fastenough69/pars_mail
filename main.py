from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep, time
import threading
from os import getenv
from string import digits

def get_time(func):
    def out_func(*args):
        timer = time()
        func(*args)
        print(time() - timer)
    return out_func

def check_name_mail(name: str):
    flag = True
    if '_' in name or ' ' in name or name[0] in digits:
        flag = False
    return flag

def init_file(name: str, driver: webdriver.Chrome):
    username = getenv('USERNAME')
    adres = f'C:\\Users\\{username}\\OneDrive\\Рабочий стол\\out_file.txt'
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
    sleep(2.3)
    init_file(mail_name, driver)
    search.clear()

def window_gmail_first(data: list, driver: webdriver.Chrome, mid_num: int):
    driver = webdriver.Chrome()
    driver.get("https://products.aspose.app/email/ru/checker?email=&email=")
    for i in range(0, mid_num):
        name = data[i] + '@gmail.com'
        search(name, driver)
    driver.quit()

def window_gmail_last(data: list, mid_num: int):
    driver = webdriver.Chrome()
    driver.get("https://products.aspose.app/email/ru/checker?email=&email=")
    for i in range(len(data) - 1, mid_num - 1, -1):
        name = data[i] + '@gmail.com'
        search(name, driver)
    driver.quit()

def window_inbox_first(data: list, mid_num: int):
    driver = webdriver.Chrome()
    driver.get("https://products.aspose.app/email/ru/checker?email=&email=")
    for i in range(0, mid_num):
        name = data[i] + '@inbox.me'
        search(name, driver)
    driver.quit()
    
def window_inbox_last(data: list, mid_num: int):
    driver = webdriver.Chrome()
    driver.get("https://products.aspose.app/email/ru/checker?email=&email=")
    for i in range(len(data) - 1, mid_num - 1, -1):
        name = data[i] + '@inbox.me'
        search(name, driver)
    driver.quit()

@get_time
def main():
    functions = [window_gmail_first, window_gmail_last, window_inbox_first, window_inbox_last]
    name_file = input('Введите  полный/абсолютный путь к файлу с почтами: ')
    with open(name_file, 'r') as input_file:
        data = input_file.readlines()
        temp = [line.split('|')[1].strip() for line in data if line != '\n']
        for name in temp:
            if not check_name_mail(name):
                temp.remove(name)
        num = (len(temp) - 1) // 4
        new_data = [[temp[i] for i in range(num * j, num * (j + 1))] for j in range(4)]
        for last in range(num * 4, len(temp)):
            new_data[3].append(temp[last])
        mid_num = (len(temp) - 1) // 2
        threads = []
        for i in range(len(functions)):
            thread = threading.Thread(target=functions[i], args=(temp, mid_num))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    main()