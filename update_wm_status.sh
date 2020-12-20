
is_running_wm=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - is_running 2) 
is_running_t=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - is_running 1)

#echo $is_running

sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "UPDATE waschmaschine SET value = '$is_running_wm' WHERE key = 'is_running';"
sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "UPDATE trockner SET value = '$is_running_t' WHERE key = 'is_running';"


#sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "select * from waschmaschine;"

