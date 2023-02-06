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
from os import system
from os.path import exists

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()
    
    def initCommand(self, command_type, chat_id, chat_type):
        self.command_type = command_type
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.ip = ""
        self.dns_api = ""
        self.dns_domain = "opiaz"
        self.dns_ip = ""
        self.script = ""

    def getCommand(self, command):
        if(self.command_type == 'document'):
            self.documentFile(command["document"])
        elif(self.command_type == 'text'):
            print(f"Command: {command['text']}")
            self.set_command(command["text"])

    def set_command(self, command):
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
        elif(self.filter(command) == "real ip"):
            self.router.getIp()
            self.ip = self.router.IP()
            self.bot.sendMessage(self.chat_id, str(self.ip))
        elif self.filter(command) == 'video':
            self.router.getIp()
            self.ip = self.router.IP()
            self.bot.sendDocument(self.chat_id, video=f'http://{self.ip}/video.mp4')
        elif(self.filter(command) == 'init dns'):
            self.dns_ip = self.ip
            self.script = f'echo url="https://www.duckdns.org/update?domains={self.dns_domain}&token={self.dns_api}&ip={self.dns_ip}" | curl -k -o duck.log -K -'
            system(self.script)
            if(exists("duck.log")):
                self.bot.sendMessage(self.chat_id, str(f"{self.dns_domain}.duckdns.org"))
            else:
                self.bot.sendMessage(self.chat_id, str("Bir xəta baş verdi!"))

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


class Router:
    def __init__(self):
                
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.logFile = open("log.txt", "w")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 25)    
        self.realIP = ""
    def getIp(self):
        self.driver.get('http://192.168.1.1')
        username = self.wait.until(EC.presence_of_element_located((By.NAME, "Login_Name")))
        password = self.wait.until(EC.presence_of_element_located((By.NAME, "Login_Pwd")))
        username.send_keys("admin")
        password.send_keys("admin")
        password.send_keys(Keys.ENTER)
        sleep(0.5)
        self.driver.get("http://192.168.1.1/status/syslog.log")
        pageSource = self.driver.page_source
        self.logFile.write(pageSource)
        self.logFile.close()
        cordinate = pageSource.find("Address")
        self.realIP = pageSource[cordinate:].split("\n")[0].split(":")[1]
        self.driver.save_screenshot("image.png")

    def IP(self):
        print(self.realIP)
        return self.realIP
