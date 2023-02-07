# telegram-bot


<b>git clone https://github.com/ramo828/telegram-bot.git</b><br/>
<b> cd telegram-bot </b><br/>
<b>vim setting.py</b><br/>
Open the file and add your own settings. <br/>

<b>pip install -r requirements.txt </b><br/>
Run the code to install the required packages.<br/>
<b>python3 bot.py</b><br/>
To update linux automatic dns.<br/>
<b>chmod +x init_ip.sh</b><br/>
<b>crontab -e </b><br/>
Then add the following line.<br/>
<b> */5 * * * * ~/telegram-bot/init_ip.sh> /dev/null 2>&1 </b><br/>

With this command dns will be updated every 5 minutes.<br/>