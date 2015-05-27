BEGIN TRANSACTION;
CREATE TABLE `users` (
	`nickname`	TEXT,
	`password`	TEXT NOT NULL,
	PRIMARY KEY(nickname)
);
INSERT INTO `users` VALUES ('robi','robi');
CREATE TABLE `songs` (
	`name`	TEXT,
	`byArtist`	TEXT,
	`datePublished`	INTEGER,
	`duration`	INTEGER NOT NULL,
	`sid`	INTEGER,
	PRIMARY KEY(sid),
	FOREIGN KEY (byArtist) REFERENCES artists(legalName)
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

CREATE TABLE "artists" (
	`legalName`	TEXT,
	`foundingLocation`	TEXT,
	`language`	TEXT,
	`genre`	TEXT,
	`foundingDate`	INTEGER,
	PRIMARY KEY(legalName)
);
INSERT INTO `artists` VALUES ('Placebo','England','English','alt-rock',1996);
COMMIT;
