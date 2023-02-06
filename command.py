"""
    Developper: Ramiz Mammadli
"""
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import settings as sett

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()
    
    def initCommand(self, command_type, chat_id, chat_type):
        self.command_type = command_type
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.ip = ""
        self.dns_api = sett.duckdns_api
        self.dns_domain = sett.duckdns_domain_name
        self.dns_ip = ""
        self.info = ""
        self.history = open("history.txt","a+")
        self.history_read = open("history.txt","r")


    def getCommand(self, command):
        if(self.command_type == 'document'):
            self.documentFile(command["document"])
        elif(self.command_type == 'text'):
            print(f"Command: {command['text']}")
            self.set_command(command["text"])

    def set_command(self, command):
        self.historyCommand(command)
        if(self.filter(command) == "/start"):
            self.bot.sendMessage(self.chat_id, str("ip\nzaman\nresim\nmuzik"))
        elif(self.filter(command) == "ip"):
            ipadd = requests.get('https://checkip.amazonaws.com').text.strip()
            self.bot.sendMessage(self.chat_id, str(ipadd))
        elif(self.filter(command) == "time"):
            self.bot.sendMessage(self.chat_id, str(datetime.datetime.now()))
        elif self.filter(command) == 'resim':
            self.bot.sendPhoto(self.chat_id, photo="https://images.all-free-download.com/images/graphicwebp/girl_posing_208124.webp")
        elif self.filter(command) == 'dosya':
            self.bot.sendDocument(self.chat_id, document=open('video.mp4'))
        elif self.filter(command) == 'muzik':
            self.bot.sendAudio(self.chat_id, audio=open('test.wav', 'rb'))
        elif(self.filter(command) == "log image"):
            self.bot.sendPhoto(self.chat_id, photo=open("image.png", "rb"))
        elif(self.filter(command) == "log"):
            self.router.getIp()
            self.bot.sendDocument(self.chat_id, document=open("log.txt", "rb"))
            self.router.tearDown()
        elif(self.filter(command) == "real ip"):
            self.router.getIp()
            self.ip = self.router.IP()
            self.bot.sendMessage(self.chat_id, str(self.ip))
            self.router.tearDown()
        elif self.filter(command) == 'video':
            self.router.getIp()
            self.ip = self.router.IP()
            self.bot.sendDocument(self.chat_id, video=f'http://{self.ip}/video.mp4')
            self.router.tearDown()
        elif self.filter(command) == 'history':
            hist = self.historyRead()
            self.bot.sendMessage(self.chat_id, str(hist))
        elif self.filter(command) == 'history file':
            self.bot.sendDocument(self.chat_id, document=open("history.txt", "rb"))
        elif(self.filter(command) == 'init dns'):
            self.router.getIp()
            self.ip = self.router.IP()
            self.dns_ip = self.ip
            dns = Dns()
            dns.init_dns(domain=self.dns_domain, ip = self.dns_ip, api=self.dns_api)
            status = dns.run()
            if(status == 1):
                self.info = f"DNS: {self.dns_domain}.duckdns.org\nIP: {self.dns_ip}"
                self.bot.sendMessage(self.chat_id, str(self.info))
            else:
                self.bot.sendMessage(self.chat_id, str("Bir xəta baş verdi!"))
            self.router.tearDown()

        else:
            self.bot.sendMessage(self.chat_id, str("Əmr yanlışdır!"))

    def textFile(self, file):
        pass
    def documentFile(self, file):
        print(file)
    def imageFile(self, file):
        pass
    def soundFile(self, file):
        pass
    def filter(self, inp = ""):
        return inp.lower()
    def historyCommand(self, command):
        date = datetime.datetime.now()
        date = str(date)
        self.history.write(f"{date[:-7]} - {command}\n")
    def historyRead(self):
        hist = str(self.history_read.read())
        return hist


class Router:
    def __init__(self):
                
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.logFile = open("log.txt", "w")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 25)    
        self.realIP = ""
    def getIp(self):
        self.driver.get(f'http://{sett.modem_url}')
        username = self.wait.until(EC.presence_of_element_located((By.NAME, "Login_Name")))
        password = self.wait.until(EC.presence_of_element_located((By.NAME, "Login_Pwd")))
        username.send_keys(sett.modem_login)
        password.send_keys(sett.modem_pass)
        password.send_keys(Keys.ENTER)
        sleep(0.5)
        self.driver.get(f"http://{sett.modem_url}/status/syslog.log")
        pageSource = self.driver.page_source
        self.logFile.write(pageSource)
        cordinate = pageSource.find("Address")
        self.realIP = pageSource[cordinate:].split("\n")[0].split(":")[1]
        self.driver.save_screenshot("image.png")
        # self.logFile.close() 
        """
            Xetaya sebeb olur
        """


    def IP(self):
        print(self.realIP)
        return self.realIP
    def tearDown(self):
        self.driver.delete_all_cookies()
        
        # self.driver.quit()
        """
            Xetaya sebeb olur
        """
class Dns:
    def __init__(self):
        self.dns_api = ""
        self.dns_domain = ""
        self.dns_ip = ""

    def init_dns(self, api,domain, ip):
        self.dns_api = api
        self.dns_domain = domain
        self.dns_ip = ip
    
    def run(self):
            self.api = requests.get(f"https://www.duckdns.org/update?domains={self.dns_domain}&token={self.dns_api}&ip={self.dns_ip}")
            if(self.api.status_code == 200):
                return 1
            else:
                return 0
