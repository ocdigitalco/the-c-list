CREATE TABLE `appearance_co_players` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`appearance_id` integer NOT NULL REFERENCES `player_appearances`(`id`),
	`co_player_id` integer NOT NULL REFERENCES `players`(`id`)
);
