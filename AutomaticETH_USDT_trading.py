from os import mkdir, name,environ
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep,time,ctime
from selenium.webdriver.common.keys import Keys
from termcolor import colored
import datetime
from numpy import sign
def TimeStamp():
    return ctime(time())
#-------------------------------------------------------------------------------------------------------------
def Minute():
    return datetime.datetime.now().minute
#-------------------------------------------------------------------------------------------------------------
def wait_until_15m():
    global last_decision,sell_count,buy_count
    print(colored('[+] {} waiting for 15th m'.format(TimeStamp()),'white'))
    count=0
    while True:
        global bc_p
        Min=Minute()
        if Min%15==0:
            break
        elif Min%15==14 and count==0:
            count+=1
            bc=extract_box_color()
            if last_decision=='buy' and bc=='r' and buy_count>0:
                print(colored('\t[+] {} compensating for mistake of buying during red'.format(TimeStamp()),'yellow'))
                sell()
            elif last_decision=='sell' and bc=='g' and sell_count>0:
                print(colored('\t[+] {} compensating for mistake of selling during green'.format(TimeStamp()),'yellow'))
                buy()
            bc_p=bc # check for the previous box color from reliable stable form
    print(colored('[+] {} waiting for 15th m done'.format(TimeStamp()),'white'))
#-------------------------------------------------------------------------------------------------------------
def init():
    global driver,value,canvas, Q1l_x_o, Q3h_x_c, change_x_c
    driver=webdriver.Chrome()
    # driver=webdriver.Chrome('/usr/bin/google-chrome')
    driver.get('https://www.binance.com/en/trade/ETH_USDT?layout=basic&theme=dark&type=spot')
    # driver.maximize_window() # For maximizing window
    driver.implicitly_wait(20)
    # searchbox.send_keys('')


    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, closeTutorial))
    #     )
    # finally:
    #     pass
    driver.maximize_window() # For maximizing window

    cross_x='/html/body/div[3]/div[2]/div[1]'
    try:
        cross=driver.find_element_by_xpath(cross_x)
        cross.click()
    except:
        print(colored('[!] click to close tutorial. couldnt do it automatic','red'))
        input('did you?')
    Login=driver.find_element_by_xpath('//*[@id="header_login"]')
    Login.click()

    Email=driver.find_element_by_xpath('//*[@id="__APP"]/div[2]/main/div/div/div[3]/div[2]/form/div/div[1]/div[2]/div/input')
    Email.send_keys(environ.get('EMAIL_ARASH_1'))

    Password=driver.find_element_by_xpath('//*[@id="__APP"]/div[2]/main/div/div/div[3]/div[2]/form/div/div[2]/div[2]/div/input')
    Password.send_keys(environ.get('PASS_MN'))

    Login=driver.find_element_by_xpath('//*[@id="click_login_submit"]')
    Login.click()

    print(colored('[!] click the capchta','red'))
    input('did you?')
    try:
        click_to_get_code_x='//*[@id="__APP"]/div[2]/main/div/div[2]/div[2]/div[1]/div/div/div'
        click_to_get_code=driver.find_element_by_xpath(click_to_get_code_x)
        click_to_get_code.click()
    except:
        print('[~] anyway')

    print(colored('[!] enter code','red'))
    input('did you?')
    
    # try:    
    #     submit_button_x='//*[@id="__APP"]/div[2]/main/div/div[2]/div[3]/button'
    #     submit_button=driver.find_element_by_xpath(submit_button_x)
    #     submit_button.click()
    # except:
    #     print('[~] never mind')

    m15=driver.find_element_by_xpath('//*[@id="15m"]')
    m15.click()


    value=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[2]/div/div[3]/div[2]/div[1]')
    canvas=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/canvas[4]')
    Q1l_x_o='//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/span[3]'
    Q3h_x_c='//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/span[9]'
    change_x_c='//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/span[11]'
#-------------------------------------------------------------------------------------------------------------
def clear_entry(entry):
    entry.send_keys(Keys.CONTROL + "a")
    entry.send_keys(Keys.DELETE)
#-------------------------------------------------------------------------------------------------------------
def extract_price_color():
    value=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[2]/div/div[3]/div[2]/div[1]')
    value_text=value.get_attribute('innerHTML')
    price=value_text[0:value_text.index('<')]
    if "status" in value_text:
        color=value_text[value_text.index('status')+len('status'):value_text.index('status')+len('status')+max(len('-sell'),len('-green'))]
    else: color='w'
    if 'green' in color: color='g'
    elif 'sell' in color: color='r'
    price=float(price.replace(',',''))
    return price,color
#-------------------------------------------------------------------------------------------------------------
def extract_box_color():
    color_indicator=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/span[7]')
    color_indicator_color=color_indicator.get_attribute("style")
    CIC=color_indicator_color[color_indicator_color.index('rgb(')+len('rgb('):color_indicator_color.index(')')]
    if CIC=='2, 192, 118': box_color='g'
    else: box_color='r'
    return box_color
#-------------------------------------------------------------------------------------------------------------
def sell():
    global last_decision,sell_count
    sell_count+=1
    price,_=extract_price_color()

    sell_button=driver.find_element_by_xpath('//*[@id="orderformSellBtn"]')
    amount=driver.find_element_by_xpath('//*[@id="FormRow-SELL-quantity"]')

    Price_entry=driver.find_element_by_xpath('//*[@id="FormRow-SELL-price"]')
    clear_entry(Price_entry)
    Price_entry.send_keys(str(price))

    total_eth=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[5]/div/div[3]/div[2]/div/div[2]/span')
    total_eth=float(total_eth.get_attribute("innerHTML").replace(' ETH',''))

    amount2Bsold=total_eth # for 100%
    clear_entry(amount)
    print(colored('total_eth {},price {},amount2Bsold {}'.format(total_eth,price,amount2Bsold)),'red')
    amount.send_keys(str(amount2Bsold))

    sell_button.click()

    with open(dirname+'/'+'sell '+TimeStamp().replace(':','_')+'.png','wb') as f:
        f.write(canvas.screenshot_as_png)

    driver.get_screenshot_as_file(dirname+'/'+'sell driver '+TimeStamp().replace(':','_')+'.png')
    last_decision='sell'
#-------------------------------------------------------------------------------------------------------------
def buy():
    global last_decision,buy_count
    buy_count+=1
    price,_=extract_price_color()

    buy_button=driver.find_element_by_xpath('//*[@id="orderformBuyBtn"]')
    amount=driver.find_element_by_xpath('//*[@id="FormRow-BUY-quantity"]')
    
    Price_entry=driver.find_element_by_xpath('//*[@id="FormRow-BUY-price"]')
    clear_entry(Price_entry)
    Price_entry.send_keys(str(price))
    
    total_usdt=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[5]/div/div[3]/div[1]/div/div[2]/span')
    total_usdt=float(total_usdt.get_attribute("innerHTML").replace(' USDT',''))

    # amount2Bbougth=total_usdt/price # for 100%
    # amount2Bbougth=11/price # for 100%
    amount2Bbougth=10.5/price # for 100%

    print(colored('total_usdt {},price {},amount2Bsold {}'.format(total_usdt,price,amount2Bbougth)),'green')
    clear_entry(amount)
    amount.send_keys(str(amount2Bbougth))

    buy_button.click()

    with open(dirname+'/'+'buy '+TimeStamp().replace(':','_')+'.png','wb') as f:
        f.write(canvas.screenshot_as_png)    
    
    driver.get_screenshot_as_file(dirname+'/'+'buy driver '+TimeStamp().replace(':','_')+'.png')

    last_decision='buy'
#-------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    init()
    bc=''
    bc_p=''
    wait_time=5*60 #7.5*60
    bcl=[]
    sold_price =0
    bought_price=0
    sampling_duration=4*60
    sampling_rate=1
    dirname=TimeStamp().replace(':','_')
    os.mkdir(dirname)
    pass_margin=10
    last_decision='sell' # start with usdt at hand so first we will buy eth at lowest
    diff_counter_thresh=10
    buy_count=0
    sell_count=0
    while True:
        print(colored('\n---------------------------------------------------------\n','blue'))
        wait_until_15m()

        Q1l_element=driver.find_element_by_xpath(Q1l_x_o)
        Q1l=float(Q1l_element.get_attribute('innerHTML'))

        Q3h_element=driver.find_element_by_xpath(Q3h_x_c)
        Q3h=float(Q3h_element.get_attribute('innerHTML'))

        # change_element=driver.find_element_by_xpath(change_x_c)
        # change=float(change_element.get_attribute('innerHTML').replace('%',''))
        print(colored('[+] {} gathering sample bc_p {}'.format(TimeStamp(),bc_p),'white'))


        bcl=[]
        for _ in range(sampling_duration):
            bcl.append(extract_box_color())
            sleep(sampling_rate)
        bcl=bcl[3*len(bcl)//4:] # choose the last piece of data
        bc='g' if bcl.count('g')==max(bcl.count('g'),bcl.count('r')) else 'r'



        # margin_counter=0
        # t1=time()
        # while True:
        #     Q3h=float(Q3h_element.get_attribute('innerHTML'))
        #     Q1l=float(Q1l_element.get_attribute('innerHTML'))

        #     if abs(Q1l-Q3h)<pass_margin:
        #         margin_counter-=1
        #     else:
        #         margin_counter+=1

        #     if time()-t1>sampling_duration: 
        #         no_decision=True
        #         break 
        #     elif margin_counter>=diff_counter_thresh:
        #         no_decision=False
        #         bc=extract_box_color()
        #         break
        print(colored('[+] {} gathering sample done bc {}'.format(TimeStamp(),bc),'white'))


        Q3h=float(Q3h_element.get_attribute('innerHTML'))
        Q1l=float(Q1l_element.get_attribute('innerHTML'))
        print(colored('[+] {} Q1l-Q3h {} '.format(TimeStamp(),Q1l-Q3h),'yellow'))

        if abs(Q1l-Q3h)<pass_margin:
        # if no_decision:
            print(colored('[+] {} passed change is small {} '.format(TimeStamp(),Q1l-Q3h),'yellow'))

        elif bc==bc_p:
            print(colored('[+] {} box color is still {}'.format(TimeStamp(),bc),'yellow'))

        elif bc_p=='g' and bc=='r' and last_decision=='buy':
            print(colored('[+] {} SELL {} --> {}'.format(TimeStamp(),bc_p,bc),'red'))
            
            sold_price,_=extract_price_color()
            
            if sold_price >= bought_price:
                sell()
            else:
                print(colored('[+] {} better not sell sold_price {} bought_price {}'.format(TimeStamp(),sold_price,bought_price),'red'))
        
        elif bc_p=='r' and bc=='g' and last_decision=='sell':
            print(colored('[+] {} BUY {} --> {}'.format(TimeStamp(),bc_p,bc),'green'))

            buy()

            bought_price,_=extract_price_color()

            # if bought_price >= sold_price:
            #     buy()
            # else:
            #     pass
        else:
            print(colored('[-] {} no if case happened bc_p {} bc {} last_decision {} sold_price {} bought_price {}'\
                .format(TimeStamp(),bc_p,bc,last_decision,sold_price,bought_price),'blue'))
        # bc_p=bc
        # sleep(wait_time)


print('hi')

""" 
value_html=value.get_attribute('innerHTML')
price=value_html[0:value_html.index('<')]
value_html[value_html.index('status')+len('status'):value_html.index('status')+len('status')+max(len('-sell'),len('-green'))]

def extract_price_color(S):
    price=S[0:value_html.index('<')]
    color=value_html[S.index('status')+len('status'):S.index('status')+len('status')+max(len('-sell'),len('-green'))]
    return price,color 
    

def extract_price_color():
    value=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[2]/div/div[3]/div[2]/div[1]')
    value_text=value.get_attribute('innerHTML')
    price=value_text[0:value_text.index('<')]
    if "status" in value_text:
        color=value_text[value_text.index('status')+len('status'):value_text.index('status')+len('status')+max(len('-sell'),len('-green'))]
    else: color='w'
    if 'green' in color: color='g'
    elif 'sell' in color: color='r'
    price=float(price.replace(',',''))
    return price,color

with open('x.png','wb') as f:
    f.write(canvas.screenshot_as_png)
color_indicator=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[3]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/span[7]')
color_indicator_color=color_indicator.get_attribute("style")
color_indicator_color[color_indicator_color.index('rgb(')+len('rgb('):color_indicator_color.index(')')]
green='2, 192, 118'

def extract_box_color(color_indicator):
    color_indicator_color=color_indicator.get_attribute("style")
    CIC=color_indicator_color[color_indicator_color.index('rgb(')+len('rgb('):color_indicator_color.index(')')]
    print(CIC)
    if CIC=='2, 192, 118': box_color='g'
    else: box_color='r'
    return box_color

Keys.CONTROL + "a"
Price_entry.send_keys(Keys.DELETE)
""" 