CREATE TABLE `athletes` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`slug` text NOT NULL,
	`name` text NOT NULL,
	`sport` text NOT NULL,
	`subject_role` text NOT NULL,
	`page_kind` text NOT NULL,
	`aliases` text,
	`set_count` integer DEFAULT 0 NOT NULL,
	`card_count` integer DEFAULT 0 NOT NULL,
	`first_year` integer,
	`rookie_year` integer,
	`created_at` text
);
--> statement-breakpoint
CREATE UNIQUE INDEX `athletes_slug_unq` ON `athletes` (`slug`);--> statement-breakpoint
ALTER TABLE `players` ADD `athlete_id` integer REFERENCES `athletes`(`id`);--> statement-breakpoint
CREATE INDEX `players_athlete_idx` ON `players` (`athlete_id`);
