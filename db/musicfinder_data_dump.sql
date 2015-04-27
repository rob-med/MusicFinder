DROP TABLE IF EXISTS "artists";
CREATE TABLE "artists" (
	`name`	TEXT,
	`country`	TEXT,
	`language`	TEXT,
	`genre`	TEXT,
	`formed_in`	INTEGER,
	PRIMARY KEY(name)
);
INSERT INTO "artists" VALUES('Placebo','England','English','alt-rock',1996);
INSERT INTO "artists" VALUES('Editors',NULL,NULL,'Indie Rock',NULL);
INSERT INTO "artists" VALUES('Foals',NULL,NULL,'Indie Rock',NULL);
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
INSERT INTO "users" VALUES('robi','robi',88,'BOH',NULL);
