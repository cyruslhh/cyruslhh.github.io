BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "responses" (
	"user_id"	INTEGER NOT NULL,
	"learning_mode"	INTEGER NOT NULL,
	"word"	TEXT,
	"actual_definition"	TEXT,
	"user_definition"	TEXT
);
CREATE TABLE IF NOT EXISTS "words" (
	"id"	INTEGER,
	"word"	TEXT,
	"definition"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER UNIQUE,
	"name"	TEXT,
	"email"	TEXT,
	"referral_code"	TEXT,
	"referral_index"	INTEGER,
	"tickets"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "words" VALUES (1,'Abrogate','Revoke Formally');
INSERT INTO "words" VALUES (2,'Abscond','Run away, often taking something or somebody along');
INSERT INTO "words" VALUES (3,'Adumbrate','Describe roughly or give a summary of');
INSERT INTO "words" VALUES (4,'Aggrandize','Increase the scope, power, or importance of');
INSERT INTO "words" VALUES (5,'Alacrity','Liveliness and eagerness');
INSERT INTO "words" VALUES (6,'Approbation','Official acceptance or agreement');
INSERT INTO "words" VALUES (7,'Blandishment','Flattery for persuading');
INSERT INTO "words" VALUES (8,'Cavort','Play boisterously');
INSERT INTO "words" VALUES (9,'Circumlocution','Indirect way of expressing something');
INSERT INTO "words" VALUES (10,'Concomitant','Following or accompanying as a consequence');
INSERT INTO "words" VALUES (11,'Conflagration','Intense and uncontrolled fire');
INSERT INTO "words" VALUES (12,'Corpulence','Excessively fat');
INSERT INTO "words" VALUES (13,'Demagogue','leader who seeks support by appealing to popular passions');
INSERT INTO "words" VALUES (14,'Didactic','instructive, especially excessively');
INSERT INTO "words" VALUES (15,'Fetter','A shackle for the feet or ankles');
INSERT INTO "words" VALUES (16,'Forebearance','good-natured tolerance of delay or incompetence');
INSERT INTO "words" VALUES (17,'Garrulous','full of trivial conversation');
INSERT INTO "words" VALUES (18,'grandiloquent','lofty in style');
INSERT INTO "words" VALUES (19,'impecunious','undue haste and lack of thought');
INSERT INTO "words" VALUES (20,'inimical','not friendly');
INSERT INTO "words" VALUES (21,'interlocutor','a person who takes part in a conversation');
INSERT INTO "words" VALUES (22,'knell','the sound of a bell rung slowly for announcing a death');
INSERT INTO "words" VALUES (23,'laconic','brief and to the point');
INSERT INTO "words" VALUES (24,'largesse','liberality in bestowing gifts');
INSERT INTO "words" VALUES (25,'licentious','lacking moral discipline');
INSERT INTO "words" VALUES (26,'mendacious','given to lying');
INSERT INTO "words" VALUES (27,'morass','a soft wet area of low-lying land that sinks underfoot');
INSERT INTO "words" VALUES (28,'mores','the conventions embodying the fundamental values of a group');
INSERT INTO "words" VALUES (29,'nadir','lowest point of anything');
INSERT INTO "words" VALUES (30,'neophyte','any new participant in some activity');
INSERT INTO "words" VALUES (31,'noisome','offesnively malodorous');
INSERT INTO "words" VALUES (32,'obdurate','stubbornly persistent in wrongdoing');
INSERT INTO "words" VALUES (33,'obstreperous','noisily and stubbornly defiant');
INSERT INTO "words" VALUES (34,'officious','intrusive in a meddling or offensive manner');
INSERT INTO "words" VALUES (35,'palliate','lessen or try to lessen the seriousness or extent of');
INSERT INTO "words" VALUES (36,'paucity','insufficient quantity or number');
INSERT INTO "words" VALUES (37,'pejorative','expressing disapproval');
INSERT INTO "words" VALUES (38,'penurious','excessively unwilling to spend');
INSERT INTO "words" VALUES (39,'pernicious','exceedingly harmful');
INSERT INTO "words" VALUES (40,'pertinacious','stubbornly unyielding');
INSERT INTO "words" VALUES (41,'phlegmatic','showing little emotion');
INSERT INTO "words" VALUES (42,'plaudit','enthusiastic approval');
INSERT INTO "words" VALUES (43,'portent','a sign of something about to happen');
INSERT INTO "words" VALUES (44,'predilection','a predisposition in favor of something');
INSERT INTO "words" VALUES (45,'preponderance','exceeding in heaviness');
INSERT INTO "words" VALUES (46,'profligate','unrestrained by convention or morality');
INSERT INTO "words" VALUES (47,'puerile','displaying a lack of maturity');
INSERT INTO "words" VALUES (48,'pugnacious','ready and able to resort to force or violence');
INSERT INTO "words" VALUES (49,'pulchritude','physical beauty especially for a woman');
INSERT INTO "words" VALUES (50,'punctilious','marked by precise accordance with details');
INSERT INTO "words" VALUES (51,'quixotic','not sensible about practical matters');
INSERT INTO "words" VALUES (52,'quandary','stat eof uncertainty in a choice between unfavorable options');
INSERT INTO "words" VALUES (53,'recalcitrant','stubbornly resistant to authority or control');
INSERT INTO "words" VALUES (54,'sanctimonious','excessively or hypocritically pious');
INSERT INTO "words" VALUES (55,'scurrilous','expressing offensive, insulting, or scandalous criticism');
INSERT INTO "words" VALUES (56,'semaphore','apparatus for visual signaling');
INSERT INTO "words" VALUES (57,'solipsism','philosophical theory that the self is all that exists');
INSERT INTO "words" VALUES (58,'spurious','plausible but false');
INSERT INTO "words" VALUES (59,'staid','characterized by dignity and propriety');
INSERT INTO "words" VALUES (60,'stolid','having/revealing little emotion or sensibility');
INSERT INTO "words" VALUES (61,'toady','a person who tries to pleace someone to gain an advantage');
INSERT INTO "words" VALUES (62,'trenchant','having keenness and forcefulness and penetration in thought');
INSERT INTO "words" VALUES (63,'umbrage','a feeling of anger caused by being offended');
INSERT INTO "words" VALUES (64,'vicissitude','variation in circumstances or fortune');
INSERT INTO "words" VALUES (65,'vituperate','spread negative information about');
COMMIT;
