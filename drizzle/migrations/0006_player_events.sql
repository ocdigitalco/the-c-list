CREATE TABLE `player_events` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`player_id` integer NOT NULL REFERENCES `players`(`id`),
	`event_type` text NOT NULL,
	`created_at` integer NOT NULL
);
--> statement-breakpoint
CREATE INDEX `player_events_player_id_idx` ON `player_events` (`player_id`);
--> statement-breakpoint
CREATE INDEX `player_events_created_at_idx` ON `player_events` (`created_at`);
--> statement-breakpoint
CREATE INDEX `player_events_type_created_idx` ON `player_events` (`event_type`, `created_at`);
