CREATE TABLE `ebay_box_offers` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`set_id` integer NOT NULL,
	`format` text NOT NULL,
	`query` text,
	`fetched_at` text,
	`offers` text,
	`result_count` integer,
	`error` text,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `ebay_box_offers_set_format_unq` ON `ebay_box_offers` (`set_id`,`format`);
