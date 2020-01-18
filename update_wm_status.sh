
is_running=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python -) 

#echo $is_running
sqlite3 /home/pi/devel/wash-bot-alexa-skill/wash-bot.sqlite  "UPDATE waschmaschine SET value = '$is_running' WHERE key = 'is_running';"
sqlite3 /home/pi/devel/wash-bot-alexa-skill/wash-bot.sqlite  "select * from waschmaschine;"

