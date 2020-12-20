# alexa-wash-bot
Alexa endpoint for a wash machine bot. The bot detects if the wash machine ist running based on the power consumption of the wash machine.


used sqllite queries:
create table waschmaschine_tae(id integer primary key AUTOINCREMENT, dt datetime default current_timestamp, tae INTEGER NOT NULL);
create table trockner_tae(id integer primary key AUTOINCREMENT, dt datetime default current_timestamp, tae INTEGER NOT NULL);
