from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def buyOculusBestBuy(email, password, delay=30, latest=True):
    """
    Scrapes LS for the readings at any time of day ;)
​
    Parameters
    ----------
    netid : (str)
        Your BYU NetID...
​
    password : (str)
        Your password...
​
    duocode : (str)
        One time use duocode (selenium opens a fresh browser w/o cookies,
        so you'll need this). Two ways of getting these:
​
            1) Open the duo mobile app and click on the BYU banner; it should
                expand and there will be one code there (again, these are single use)
​
            2) If you clear your cookies so that you must duo-authenticate,
                you can select the option to enter a passcode, then at the bottom
                it will have a button to send you new codes. Click that and you will
                get 10 codes, each good for one use.
​
    delay : (int)
        Number of seconds to wait before getting the readings. For example, if
        you want to pull at 2am and it is currently 10pm, you would enter 4*3600=14400.
​
    latest : (bool, default True)
        If False, will pull *all* of the *textbook* readings (this should never
        try pulling the other things). If True, *should* just grab the latest reading available.
    """
    try:
        # start chrome driver, request LS
        driver = webdriver.Chrome()
        # Test adding case to cart
        driver.get('https://www.bestbuy.com/site/travel-case-for-oculus-quest-black/6342916.p?skuId=6342916')
        # Actual Oculus Quest url
        # driver.get('https://www.bestbuy.com/site/oculus-quest-all-in-one-vr-gaming-headset-64gb-black/6342914.p?skuId=6342914')
        time.sleep(5) 

        driver.switch_to_window(driver.current_window_handle)

        # while True:
        # How often you want to check if available and buy if possible
        time.sleep(delay)

        # buttons/fields for login
        add_to_cart_button = driver.find_element_by_class_name('btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button')

        # Click add to cart
        add_to_cart_button.click()
    finally:
        driver.close()