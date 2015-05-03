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