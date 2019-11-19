BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "music" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"file_id"	TEXT,
	"right_answer"	TEXT,
	"wrong_answers"	TEXT
);
INSERT INTO "music" VALUES (1,'AwADAgADgQQAAvcPoUp5rgABTKiyXQcWBA','Imagine Dragons - Radioactive','Mans Zelmerlow - Heroes,Imagine Dragons - Darkness,Coldplay - Paradise');
INSERT INTO "music" VALUES (2,'AwADAgADjwQAAkihoUouj1VHe1lngxYE','Arctic Monkeys - Do I Wanna Know','Lana Del Rey - Sad Girl,Fall Out Boy - Irresistible,Melanie Martinez - Carousel');
INSERT INTO "music" VALUES (3,'AwADAgADkAQAAkihoUpnHkEUlyGgzRYE','The Pixies - Where Is My Mind','The Toxic Avenger - In The Meantime Run,Feelms - Little Forest,Depeche Mode - The Darkest Star');
INSERT INTO "music" VALUES (4,'AwADAgADggQAAvcPoUqsJNEJSkPiRRYE','The Black Eyed Peas - Dum Diddly','Travis Scott - Blocka La Flame,Future - Jordan Diddy,Ja Rule - Race Against Time');
INSERT INTO "music" VALUES (5,'AwADAgADkQQAAkihoUq0BM5-B5ssBBYE','Arabesque - In the Heat Of A Disco Night','Frank Duwalle - Touch My Soul,Ottawan - Disco,ABBA - Gimme Gimme Gimme');
COMMIT;
