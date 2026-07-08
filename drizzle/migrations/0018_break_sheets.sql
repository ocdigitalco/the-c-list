CREATE TABLE `break_sheets` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`created_at` integer NOT NULL,
	`set_slug` text NOT NULL,
	`sport` text NOT NULL,
	`break_unit` text NOT NULL,
	`quantity` integer NOT NULL,
	`cost` real,
	`total` real NOT NULL,
	`profit` real,
	`config` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `break_sheet_prices` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`sheet_id` integer NOT NULL,
	`subject_name` text NOT NULL,
	`subject_type` text NOT NULL,
	`price` real NOT NULL,
	FOREIGN KEY (`sheet_id`) REFERENCES `break_sheets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE INDEX `break_sheets_created_at_idx` ON `break_sheets` (`created_at`);
--> statement-breakpoint
CREATE INDEX `break_sheet_prices_sheet_id_idx` ON `break_sheet_prices` (`sheet_id`);
