from termcolor import colored
from sys import version
print(colored(version,'red'))
from os import mkdir, name,environ
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep,time,ctime
from selenium.webdriver.common.keys import Keys
import datetime
from numpy import sign
from playsound import playsound
import pyttsx3
from selenium.webdriver.chrome.options import Options


def TimeStamp():
    return ctime(time())
#-------------------------------------------------------------------------------------------------------------
def Minute():
    return datetime.datetime.now().minute
#-------------------------------------------------------------------------------------------------------------
def Second():
    return datetime.datetime.now().second
#-------------------------------------------------------------------------------------------------------------
def wait_until_15m():
    global last_decision,sell_count,buy_count,bc_p
    print(colored('[+] {} waiting for 15th m'.format(TimeStamp()),'white'))
    count=0
    while True:
        Min=Minute()
        Sec=Second()
        if Min%15==0:
            break
        elif Min%15==14 and count==0 and Sec>=40 :
            count+=1
            bc_p=extract_box_color() # check for the previous box color from reliable stable form
    print(colored('[+] {} waiting for 15th m done'.format(TimeStamp()),'white'))
#-------------------------------------------------------------------------------------------------------------
def speaker_init():
    global speak_engine
    speak_engine = pyttsx3.init()

    """ RATE"""
    rate = speak_engine.getProperty('rate')   # getting details of current speaking rate
    # print ("rate", rate)                        #printing current voice rate
    speak_engine.setProperty('rate', 100)     # setting up new voice rate


    """VOLUME"""
    volume = speak_engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    # print ("volume", volume)                          #printing current volume level
    speak_engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = speak_engine.getProperty('voices')       #getting details of current voice
    #speak_engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    speak_engine.setProperty('voice', 'english')   #changing index, changes voices. 1 for female

    speak_engine.say("Hello World!")
    speak_engine.runAndWait()
    speak_engine.stop()
#-------------------------------------------------------------------------------------------------------------
def init():
    global driver,value,canvas, Q1l_x_o, Q3h_x_c, change_x_c
    speaker_init()
    driver=webdriver.Chrome()
    # driver=webdriver.Chrome('/usr/bin/google-chrome')
    driver.get('https://www.binance.com/en/trade/ETH_USDT?layout=basic&theme=dark&type=spot')
    driver.implicitly_wait(20)
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
    """     
    try:    
        submit_button_x='//*[@id="__APP"]/div[2]/main/div/div[2]/div[3]/button'
        submit_button=driver.find_element_by_xpath(submit_button_x)
        submit_button.click()
    except:
        print('[~] never mind')

    """
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
    global last_decision,sell_count,allow_sound
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
    print(colored('[+] Sell total_eth {},price {},amount2Bsold {}'.format(total_eth,price,amount2Bsold),'red'))
    amount.send_keys(str(amount2Bsold))

    sell_button.click()

    # with open(dirname+'/'+TimeStamp().replace(':','_')+' sell '+'.png','wb') as f:
    #     f.write(canvas.screenshot_as_png)

    driver.get_screenshot_as_file(dirname+'/'+TimeStamp().replace(':','_')+' sell driver '+'.png')
    last_decision='sell'

    if allow_sound:
        playsound('treasure sound.mp3')
        speak_engine.say("Sold with price " + str(price))
        speak_engine.runAndWait()
        playsound('treasure sound.mp3')

#-------------------------------------------------------------------------------------------------------------
def buy():
    global last_decision,buy_count,allow_sound,bought_price
    buy_count+=1
    bought_price,_=extract_price_color()

    buy_button=driver.find_element_by_xpath('//*[@id="orderformBuyBtn"]')
    amount=driver.find_element_by_xpath('//*[@id="FormRow-BUY-quantity"]')
    
    Price_entry=driver.find_element_by_xpath('//*[@id="FormRow-BUY-price"]')
    clear_entry(Price_entry)
    Price_entry.send_keys(str(bought_price))
    
    total_usdt=driver.find_element_by_xpath('//*[@id="__APP"]/div/div/div[5]/div/div[3]/div[1]/div/div[2]/span')
    total_usdt=float(total_usdt.get_attribute("innerHTML").replace(' USDT',''))

    # amount2Bbougth=total_usdt/bought_price # for 100%
    # amount2Bbougth=11/bought_price # for 100%
    amount2Bbougth=10.5/bought_price # for 100%

    print(colored('[+] Bought total_usdt {},bought_price {},amount2Bsold {}'.format(total_usdt,bought_price,amount2Bbougth),'green'))
    clear_entry(amount)
    amount.send_keys(str(amount2Bbougth))

    buy_button.click()

    # with open(dirname+'/'+TimeStamp().replace(':','_')+' buy '+'.png','wb') as f:
    #     f.write(canvas.screenshot_as_png)    
    
    driver.get_screenshot_as_file(dirname+'/'+TimeStamp().replace(':','_')+' buy driver '+'.png')

    last_decision='buy'
    
    if allow_sound:
        playsound('coin sound.mp3')
        speak_engine.say("Bought with bought_price " + str(bought_price))
        speak_engine.runAndWait()
        playsound('coin sound.mp3')

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
    pass_margin=10//2
    last_decision='sell' # start with usdt at hand so first we will buy eth at lowest
    diff_counter_thresh=10
    buy_count=0
    sell_count=0
    allow_sound=True
    crash_count=0
    try:
        while True:
            try:

                wait_until_15m()
                print(colored('\n---------------------------------------------------------\n','blue'))

                Q1l_element=driver.find_element_by_xpath(Q1l_x_o)
                Q3h_element=driver.find_element_by_xpath(Q3h_x_c)

                # change_element=driver.find_element_by_xpath(change_x_c)
                # change=float(change_element.get_attribute('innerHTML').replace('%',''))
                print(colored('[+] {} gathering sample bc_p {}'.format(TimeStamp(),bc_p),'white'))


                bcl=[]
                bc='empty'
                """ 
                for _ in range(sampling_duration):
                    bcl.append(extract_box_color())
                    sleep(sampling_rate)
                    # if Q3h-Q1l<
                """
                t1=time()
                while True:
                    Q3h=float(Q3h_element.get_attribute('innerHTML'))
                    Q1l=float(Q1l_element.get_attribute('innerHTML'))
                    bcl.append(extract_box_color())

                    if time()-t1>= sampling_duration:
                        bcl=bcl[3*len(bcl)//4:] # choose the last piece of data
                        bc='g' if bcl.count('g')==max(bcl.count('g'),bcl.count('r')) else 'r'
                        print(colored('[+] {} gathering sample done TIME REACHED bc {}'.format(TimeStamp(),bc),'white'))        
                        break
                    elif abs(Q3h-Q1l)>= pass_margin:
                        bc=bcl[-1]
                        print(colored('[+] {} gathering sample done Q3h-Q1l is big {} bc {}'.format(TimeStamp(),Q3h-Q1l,bc),'white'))        
                        break



                price,_=extract_price_color()
                print(colored('[+] {} Q1l-Q3h {} '.format(TimeStamp(),round(Q1l-Q3h,2),price),'yellow'))

                """ 
                if abs(Q1l-Q3h)<pass_margin:
                    print(colored('[+] {} passed change is small {} '.format(TimeStamp(),Q1l-Q3h),'yellow'))
                """

                if  price<=bought_price+0.1 and last_decision=='buy':
                    print(colored('[+] {} COMPONSATE price<=bought_price+0.1 {} bought_price {}'.format(TimeStamp(),price,bought_price),'red'))
                    sell()

                elif bc==bc_p:
                    print(colored('[+] {} box color is still {}'.format(TimeStamp(),bc),'yellow'))

                elif (bc_p=='g' and bc=='r') and last_decision=='buy':
                    print(colored('[+] {} SELL {} --> {}'.format(TimeStamp(),bc_p,bc),'red'))
                    
                    if price >= bought_price:
                        sell()
                    else:
                        print(colored('[+] {} better not sell price {} bought_price {}'.format(TimeStamp(),price,bought_price),'red'))
                

                elif bc_p=='r' and bc=='g' and last_decision=='sell':
                    print(colored('[+] {} BUY {} --> {}'.format(TimeStamp(),bc_p,bc),'green'))
                    buy()
                else:
                    print(colored('[-] {} no if case happened bc_p {} bc {} last_decision {} price {} bought_price {}'\
                        .format(TimeStamp(),bc_p,bc,last_decision,price,bought_price),'blue'))
            except Exception as E_loop:
                speak_engine.say("Faliure Faliure Faliure Faliure")
                speak_engine.runAndWait()
                """ 
                if crash_count==0: # sell once to escapehaving money in ETH
                    sell()
                """
                crash_count+=1
                print(colored("[-] program crashed with error: "+E_loop),'red')
                driver.refresh()
    except Exception as E_major:
        print(colored("[-] program crashed and no escape with error: "+E_major),'red')
        sell()
        print('bye')

print('hix')
