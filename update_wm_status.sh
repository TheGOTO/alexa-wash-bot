#set -x

is_running_wm=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - is_running 2) 
is_running_t=$(cat /home/pi/devel/wash-bot-alexa-skill/smartmeter.py | ssh raspberry python - is_running 1)

echo $is_running_wm
echo $is_running_t

sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "UPDATE waschmaschine SET value = '$is_running_wm' WHERE key = 'is_running';"
sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "UPDATE trockner SET value = '$is_running_t' WHERE key = 'is_running';"


#sqlite3 /var/log/wash-bot-alexa-skill/wash-bot.sqlite  "select * from waschmaschine;"

curl -v -X POST 'https://z1f5iy7b31.execute-api.eu-central-1.amazonaws.com/default/Waschmaschine' -H 'content-type: application/json' -H "x-api-key:3W4yJDJfKKhMP4Q7BZfK43kzaEEztxT9GjVkVDZf" -H 'day: Thursday'  -d '{ "wm_is_running": "'$is_running_wm'","t_is_running": "'$is_running_t'" }'


#set +x
