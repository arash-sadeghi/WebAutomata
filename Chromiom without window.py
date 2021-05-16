from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# d = webdriver.Chrome('/home/PycharmProjects/chromedriver',chrome_options=chrome_options)
# d = webdriver.Chrome(chrome_options=chrome_options)

# d = webdriver.Chrome('/usr/bin/chromium-browser')
d = webdriver.Chrome('/usr/bin/chromium-browser')


d.get('https://www.google.nl/')

X='//*[@id="SIvCob"]'
x=d.find_element_by_xpath(X)
x.get_attribute('innerHTML')

# x=d.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')

print('hi')

