CREATE TABLE `set_alerts` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`email` text NOT NULL,
	`set_id` integer NOT NULL,
	`token` text NOT NULL,
	`created_at` text DEFAULT (datetime('now')) NOT NULL,
	`notified_at` text,
	FOREIGN KEY (`set_id`) REFERENCES `sets`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `set_alerts_token_unique` ON `set_alerts` (`token`);--> statement-breakpoint
CREATE UNIQUE INDEX `set_alerts_email_set_unq` ON `set_alerts` (`email`,`set_id`);--> statement-breakpoint
CREATE INDEX `idx_set_alerts_set_notified` ON `set_alerts` (`set_id`,`notified_at`);
