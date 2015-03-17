BEGIN TRANSACTION;
CREATE TABLE `users` (
	`nickname`	TEXT,
	`password`	TEXT NOT NULL,
	PRIMARY KEY(nickname)
);
INSERT INTO `users` VALUES ('robi','robi');
CREATE TABLE `songs` (
	`title`	TEXT,
	`artist`	TEXT,
	`year`	INTEGER,
	`length`	INTEGER NOT NULL,
	`sid`	INTEGER,
	PRIMARY KEY(sid),
	FOREIGN KEY (artist) REFERENCES artists(name)
);
INSERT INTO `songs` VALUES ('I know','Placebo',1996,'3:41',1);
CREATE TABLE "song_in_playlist" (
	`song`	INTEGER,
	`pl_name`	TEXT,
	`pl_user`	TEXT,
	`added_on`	INTEGER,
	PRIMARY KEY(song,pl_name,pl_user),
	FOREIGN KEY(`song`) REFERENCES songs ( sid )
);
INSERT INTO `song_in_playlist` VALUES (1,'Prima','robi',1426608888);
CREATE TABLE "playlists" (
	`name`	TEXT,
	`user`	TEXT,
	`created_on`	INTEGER,
	PRIMARY KEY(name,user),
	FOREIGN KEY(`user`) REFERENCES users ( nickname )
);
INSERT INTO `playlists` VALUES ('Prima','robi',1426608869);
CREATE TABLE `favorites` (
	`song`	INTEGER,
	`user`	TEXT,
	PRIMARY KEY(song,user),
	FOREIGN KEY (song) REFERENCES songs(sid),
	FOREIGN KEY (user) REFERENCES users(nickname)
);
CREATE TABLE "artists" (
	`name`	TEXT,
	`country`	TEXT,
	`language`	TEXT,
	`genre`	TEXT,
	`formed_in`	INTEGER,
	PRIMARY KEY(name)
);
INSERT INTO `artists` VALUES ('Placebo','England','English','alt-rock',1996);
COMMIT;
