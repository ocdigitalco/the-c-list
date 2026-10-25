CREATE TABLE `break_listings` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`source` text DEFAULT 'ebay' NOT NULL,
	`set_id` integer NOT NULL,
	`item_id` text NOT NULL,
	`seller` text,
	`seller_feedback_pct` real,
	`title` text NOT NULL,
	`price_cents` integer,
	`currency` text DEFAULT 'USD' NOT NULL,
	`buying_option` text,
	`format_guess` text,
	`matched_player_ids` text,
	`item_url` text,
	`item_web_url` text,
	`image_url` text,
	`listed_at` text,
	`first_seen_at` text,
	`fetched_at` text NOT NULL,
	`active` integer DEFAULT 1 NOT NULL,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `break_listings_set_item_unq` ON `break_listings` (`set_id`,`item_id`);
--> statement-breakpoint
CREATE INDEX `break_listings_set_idx` ON `break_listings` (`set_id`,`active`);
--> statement-breakpoint
CREATE TABLE `break_refresh_state` (
	`set_id` integer PRIMARY KEY NOT NULL,
	`last_fetched_at` text,
	`last_result_count` integer,
	`last_error` text,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action
);
