PRAGMA foreign_keys=OFF;
--> statement-breakpoint
DROP TABLE IF EXISTS `player_appearances`;
--> statement-breakpoint
DROP TABLE IF EXISTS `players`;
--> statement-breakpoint
CREATE TABLE `players` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`set_id` integer NOT NULL,
	`name` text NOT NULL,
	`unique_cards` integer DEFAULT 0 NOT NULL,
	`total_print_run` integer DEFAULT 0 NOT NULL,
	`one_of_ones` integer DEFAULT 0 NOT NULL,
	`insert_set_count` integer DEFAULT 0 NOT NULL,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `players_set_name_unique` ON `players` (`set_id`, `name`);
--> statement-breakpoint
CREATE TABLE `player_appearances` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`player_id` integer NOT NULL,
	`insert_set_id` integer NOT NULL,
	`card_number` text NOT NULL,
	`team` text NOT NULL,
	`is_rookie` integer DEFAULT false NOT NULL,
	`subset_tag` text,
	FOREIGN KEY (`player_id`) REFERENCES `players`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`insert_set_id`) REFERENCES `insert_sets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
PRAGMA foreign_keys=ON;
