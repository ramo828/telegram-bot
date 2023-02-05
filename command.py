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

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.router = Router()
    
    def initCommand(self, command_type, chat_id, chat_type):
        self.command_type = command_type
        self.chat_id = chat_id
        self.chat_type = chat_type

    def getCommand(self, command):
        if(self.command_type == 'document'):
            self.documentFile(command["document"])
        elif(self.command_type == 'text'):
            print(f"Command: {command['text']}")
            self.set_command(command["text"])

    def set_command(self, command):
        if(command == "/start"):
            self.bot.sendMessage(self.chat_id, str("ip\nzaman\nresim\nmuzik"))
        elif(command == "ip"):
            ipadd = requests.get('https://checkip.amazonaws.com').text.strip()
            self.bot.sendMessage(self.chat_id, str(ipadd))
        elif(command == "time"):
            self.bot.sendMessage(self.chat_id, str(datetime.datetime.now()))
        elif command == 'resim':
            self.bot.sendPhoto(self.chat_id, photo="https://images.all-free-download.com/images/graphicwebp/girl_posing_208124.webp")
        elif command == 'dosya':
            self.bot.sendDocument(self.chat_id, document=open('video.mp4'))
        elif command == 'muzik':
            self.bot.sendAudio(self.chat_id, audio=open('test.wav', 'rb'))
        elif(command == "logImage"):
            self.bot.sendPhoto(self.chat_id, photo=open("image.png", "rb"))
        elif(command == "log"):
            self.bot.sendVideo(self.chat_id, document=open("log.txt", "r"))
        elif(command == "real ip"):
            self.router.getIp()
            ip = self.router.IP()
            self.bot.sendMessage(self.chat_id, str(ip))
        elif command == 'video':
            self.router.getIp()
            ip = self.router.IP()
            self.bot.sendDocument(self.chat_id, video=f'http://{ip}/sex.mp4')
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
        cordinate = pageSource.find("Address")
        self.realIP = pageSource[cordinate:].split("\n")[0].split(":")[1]
        print(pageSource[cordinate:].split("\n")[0].split(":")[1])
        self.driver.save_screenshot("image.png")

    def IP(self):
        return self.realIP
