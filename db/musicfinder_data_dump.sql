DROP TABLE IF EXISTS "artists";
CREATE TABLE "artists" (
	`name`	TEXT,
	`country`	TEXT,
	`language`	TEXT,
	`genre`	TEXT,
	`formed_in`	INTEGER,
	PRIMARY KEY(name)
);
INSERT INTO "artists" VALUES('Placebo','England','English','Alternative Rock',1996);
INSERT INTO "artists" VALUES('Editors','England','English','Indie Rock',2004);
INSERT INTO "artists" VALUES('Foals',NULL,NULL,'Indie Rock',NULL);
INSERT INTO "artists" VALUES('Cranberries',NULL,NULL,'Rock',1990);
INSERT INTO "artists" VALUES('Muse','England','English','Rock',1992);
INSERT INTO "artists" VALUES('OneRepublic','USA','English','Pop',2002);
INSERT INTO "artists" VALUES('Eddie Vedder','USA','English','Grunge',NULL);
INSERT INTO "artists" VALUES('Fritz Kalkbrenner','Germany',NULL,'Techno',NULL);
INSERT INTO "artists" VALUES('Paul Kalkbrenner','Germany',NULL,'Techno',NULL);
INSERT INTO "artists" VALUES('Sting','England','English','Pop',NULL);
INSERT INTO "artists" VALUES('Coldplay','England','English','Pop',1997);
INSERT INTO "artists" VALUES('Kavinsky','France',NULL,'House',NULL);
INSERT INTO "artists" VALUES('John Legend','USA','English','Soul',NULL);
INSERT INTO "artists" VALUES('Empire of the sun','Australia','English','Indie Rock',2008);
INSERT INTO "artists" VALUES('Imagine Dragons','USA','English','Alternative Rock',2008);
INSERT INTO "artists" VALUES('Mana','Mexico','Spanish','Rock',1986);
INSERT INTO "artists" VALUES('Green day','USA','English','Punk',1986);
INSERT INTO "artists" VALUES('Sanni','Finland','Finnish','Pop',NULL);
INSERT INTO "artists" VALUES('Radiohead','England','English','Alternative Rock',1992);
INSERT INTO "artists" VALUES('Dream Theater','USA','English','Heavy Metal',1985);

DROP TABLE IF EXISTS "favorites";
CREATE TABLE `favorites` (
	`song`	INTEGER,
	`user`	TEXT,
	PRIMARY KEY(song,user),
	FOREIGN KEY (song) REFERENCES songs(sid),
	FOREIGN KEY (user) REFERENCES users(nickname)
);
DROP TABLE IF EXISTS "playlists";
CREATE TABLE "playlists" (
	`name`	TEXT,
	`user`	TEXT,
	`created_on`	INTEGER,
	PRIMARY KEY(name,user),
	FOREIGN KEY(`user`) REFERENCES users ( nickname )
);
INSERT INTO "playlists" VALUES('Posted','robi',1427901320);
DROP TABLE IF EXISTS "song_in_playlist";
CREATE TABLE "song_in_playlist" (
	`song`	INTEGER,
	`pl_name`	TEXT,
	`pl_user`	TEXT,
	`added_on`	INTEGER,
	PRIMARY KEY(song,pl_name,pl_user),
	FOREIGN KEY(`song`) REFERENCES songs ( sid )
);
INSERT INTO "song_in_playlist" VALUES(1,'Prima','robi',1426608888);
INSERT INTO "song_in_playlist" VALUES(2,'Posted','robi',1430155183);
DROP TABLE IF EXISTS "songs";
CREATE TABLE `songs` (
	`title`	TEXT,
	`artist`	TEXT,
	`year`	INTEGER,
	`length`	INTEGER NOT NULL,
	`sid`	INTEGER,
	PRIMARY KEY(sid),
	FOREIGN KEY (artist) REFERENCES artists(name)
);
INSERT INTO "songs" VALUES('I know','Placebo',1996,'3:41',1);
INSERT INTO "songs" VALUES('Pierrot the clown','Placebo',NULL,'4:23',2);
INSERT INTO "songs" VALUES('Zombie','Cranberries',1994,'5:21',6);
INSERT INTO "songs" VALUES('We are the people','Empire of the sun',2008,'4:17',7);
INSERT INTO "songs" VALUES('Counting stars','OneRepublic',2013,'4:23',8);
INSERT INTO "songs" VALUES('Radioactive','Imagine Dragons',2012,'3:07',9);
INSERT INTO "songs" VALUES('2080-Luvulla','Sanni',2015,'4:18',10);
INSERT INTO "songs" VALUES('Wes','Fritz Kalkbrenner',2011,'7:16',11);
INSERT INTO "songs" VALUES('Fields of gold','Sting',1993,'3:39',12);
INSERT INTO "songs" VALUES('Dirty paws','Of monster and men',2011,'4:38',13);
INSERT INTO "songs" VALUES('Yellow','Coldplay',2000,'4:30',14);
INSERT INTO "songs" VALUES('Just breathe','Pearl jam',2009,'3:36',15);
INSERT INTO "songs" VALUES('Pacific coast highway','Kavinsky',2010,'5:44',16);
INSERT INTO "songs" VALUES('All of me','John Legend',2013,'4:30',17);
INSERT INTO "songs" VALUES('Rainbow girl','Giana factory',2010,'3:17',18);
INSERT INTO "songs" VALUES('Beautiful day','U2',1993,'4:06',19);
INSERT INTO "songs" VALUES('Blackout','Muse',2003,'4:22',20);
INSERT INTO "songs" VALUES('Karma police','Radiohead',1997,'4:22',21);
INSERT INTO "songs" VALUES('Porcelain','Moby',1999,'4:01',22);
INSERT INTO "songs" VALUES('Starlight','Muse',2006,'4:00',23);

DROP TABLE IF EXISTS "users";
CREATE TABLE "users" (
	`nickname`	TEXT,
	`password`	TEXT NOT NULL,
	`age`	INTEGER,
	`country`	TEXT,
	`gender`	TEXT,
	PRIMARY KEY(nickname)
);
INSERT INTO "users" VALUES('Robi','pass',18,'Italy','Male');
INSERT INTO "users" VALUES('Joshua','oerae',34,'Austalia','Male');
INSERT INTO "users" VALUES('Clayton','ampsy',18,'USA','Male');