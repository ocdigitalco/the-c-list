CREATE TABLE `sold_comps` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`set_id` integer NOT NULL,
	`insert_set_id` integer NOT NULL,
	`card_number` text NOT NULL,
	`player_id` integer NOT NULL,
	`grade_filter` text DEFAULT 'raw' NOT NULL,
	`keyword` text,
	`last_sold_price_cents` integer,
	`last_sold_at` text,
	`last_sold_url` text,
	`last_sold_type` text,
	`median_30d_cents` integer,
	`count_30d` integer,
	`low_30d_cents` integer,
	`high_30d_cents` integer,
	`raw_items_json` text,
	`fetched_at` text,
	`source` text DEFAULT 'sold-comps' NOT NULL,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`insert_set_id`) REFERENCES `insert_sets`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`player_id`) REFERENCES `players`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `sold_comps_key_unq` ON `sold_comps` (`set_id`,`insert_set_id`,`card_number`,`player_id`,`grade_filter`);
--> statement-breakpoint
CREATE TABLE `sold_comps_usage` (
	`day` text PRIMARY KEY NOT NULL,
	`calls` integer DEFAULT 0 NOT NULL,
	`credits_used_estimate` integer DEFAULT 0 NOT NULL,
	`last_x_usage_json` text
);
--> statement-breakpoint
CREATE TABLE `sold_comps_requests` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`ip_hash` text NOT NULL,
	`requested_at` text NOT NULL,
	`cache_key` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX `sold_comps_requests_time_idx` ON `sold_comps_requests` (`requested_at`);
--> statement-breakpoint
CREATE INDEX `sold_comps_requests_ip_idx` ON `sold_comps_requests` (`ip_hash`);
