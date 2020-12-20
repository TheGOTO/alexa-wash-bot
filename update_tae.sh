
tae_wm=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - TAE 2) 
tae_t=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - TAE 1)

#echo "$tae_wm"

sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "INSERT INTO waschmaschine_tae (tae) values ('$tae_wm');"
sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "INSERT INTO trockner_tae (tae) values ('$tae_t');"


sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "select * from waschmaschine_tae;"
sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "select * from trockner_tae;"


