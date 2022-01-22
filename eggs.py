from selenium import webdriver
import requests
import json
import time
import playsound
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

image = 2

url = "https://axieinfinity.com/graphql-server-v2/graphql"
payload = {
    "operationName": "GetAxieBriefList",
    "variables": {
        "from": 0,
        "size": 10,
        "sort": "Latest",
        "auctionType": "Sale",
        "owner": None,
        "criteria": {
            "region": None,
            "parts": None,
            "bodyShapes": None,
            "classes": None,
            "stages": [1],
            "numMystic": None,
            "pureness": None,
            "title": None,
            "breedable": None,
            "breedCount": None,
            "hp": [],
            "skill": [],
            "speed": [],
            "morale": []
        }
    },
    "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
}

#START OF THE BOT
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=/home/max/.config/google-chrome/AxieProfiles/1")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
chrome_prefs = {}
options.add_experimental_option("prefs", chrome_prefs)
chrome_prefs["profile.default_content_settings"] = {"images": 1}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 1}
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')
#options.headless = headless
driver = webdriver.Chrome(executable_path=r'/home/max/Documents/PythonProjects/requestAixieBot/chromedriver_linux64/chromedriver', options=options)

desiredPrice = .03
sort = False
def bot(desiredPrice, sort):
    try: #initiates the bot (login and pull up ronin + market)
        time.sleep(2)
        driver.get("chrome-extension://fnjhmkhhmkbjkkabndcnnogagogbneec/popup.html#/unlock")
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        driver.find_element_by_id("password-input").send_keys("Snortingjo@1" + Keys.RETURN)
        time.sleep(1)
        payment = driver.current_window_handle
        driver.execute_script("window.open('https://marketplace.axieinfinity.com/axie','_blank');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(6)
        market = driver.current_window_handle
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[6]/div/a[5]').click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/button").click()
        driver.switch_to.window(payment)
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div[2]/div/button[2]').click()
        driver.switch_to.window(market)
    except:
        pass
    playsound.playsound('/home/max/Documents/PythonProjects/requestAixieBot/Notification.wav', False)
    loop = True
    driver.switch_to.window(market)
    while(loop):
        try:
            response = requests.post(url, json=payload) #sends request for axie information to their server
            data = json.loads(json.dumps(response.json()))
            axies = data['data']['axies']['results']
            for i in range(5): #goes through recieved axies
                axiePrice = int(axies[i]['auction']['currentPrice']) / 1000000000000000000 #grabs price in ETH format
                if axiePrice <= desiredPrice:
                    clickCount = 0
                    playsound.playsound('/home/max/Documents/PythonProjects/requestAixieBot/Notification.wav', False)
                    driver.switch_to.window(market)
                    driver.get("https://marketplace.axieinfinity.com/axie/" + axies[i]['id']) #goes to axie page in marketplace
                    coun = 0
                    while(coun < 220 and clickCount < 5): #80
                        coun = coun + 1
                        try:
                            driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[4]/div/button").click()
                            cont = True
                        except:
                            cont = False
                        if not cont:
                            try:
                                driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[3]/div/button").click()
                                cont = True
                            except:
                                cont = False
                        if cont:
                            driver.switch_to.window(payment)
                            loopcheck = True
                            count = 0
                            price = ""
                            while (loopcheck and count < 350):
                                try:
                                    price = (driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div[2]/div[9]/div[2]/div/div/span[1]').text).replace(' WETH', "").replace("-", "")
                                    loopcheck = False
                                except:
                                    count = count + 1
                            if float(price) <= desiredPrice: #checks if the final price is still less than the desired price you want to pay
                                loop5 = 0
                                clicked = False
                                while(not clicked and loop5 < 250):
                                    try:
                                        driver.find_element_by_xpath("/html/body/section/div/div/div[2]/div/div[3]/button[2]").click()
                                        clickCount = clickCount + 1
                                    except Exception as e:
                                        loop5 = loop5 + 1
                                        print(e)
                            else: #if the final price is more, cancel the transaction
                                open = True
                                while(open):
                                    time.sleep(.5)
                                    try:
                                        driver.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div[3]/button[1]').click()
                                        clickCount = clickCount + 5
                                        open = False
                                    except Exception as e:
                                        open = True
                                        print(e)
                            driver.switch_to.window(market)
                            time.sleep(.5)
                            try:
                                driver.find_element_by_xpath(
                                    '/html/body/div[8]/div/div[2]/div[2]/div[2]/button').click()
                            except:
                                pass
                            try:
                                driver.find_element_by_xpath(
                                    '/html/body/div[9]/div/div[2]/div[2]/div/div/button').click()
                            except:
                                pass
                    driver.switch_to.window(market)
        except:
            loop = True
while(True):
    bot(desiredPrice, sort)
    print("Loop")
