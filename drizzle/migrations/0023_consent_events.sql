CREATE TABLE IF NOT EXISTS `consent_events` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`consent_id` text NOT NULL,
	`ts` text NOT NULL,
	`notice_version` integer NOT NULL,
	`analytics` integer NOT NULL,
	`advertising` integer NOT NULL,
	`gpc` integer NOT NULL,
	`source` text NOT NULL
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS `idx_consent_events_consent_id` ON `consent_events` (`consent_id`);
