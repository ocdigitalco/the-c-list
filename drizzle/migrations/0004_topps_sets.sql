CREATE TABLE `topps_sets` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`name` text NOT NULL,
	`sport` text NOT NULL,
	`year` integer NOT NULL
);
--> statement-breakpoint
INSERT INTO `topps_sets` (`name`, `sport`, `year`) VALUES
	('2025 Bowman''s Best Baseball', 'Baseball', 2026),
	('2025 Bowman Draft Baseball Sapphire Edition', 'Baseball', 2026),
	('2026 Topps Brooklyn Collection', 'Baseball', 2026),
	('2025-26 Topps Chrome Basketball Sapphire', 'Basketball', 2026),
	('2025-26 Topps Chrome Cactus Jack Basketball', 'Basketball', 2026),
	('2025 Topps Chrome Deadpool', 'Entertainment', 2026),
	('2025 Topps Chrome Formula 1 Sapphire Edition', 'Racing', 2026),
	('2025 Topps Chrome McDonald''s All-American Basketball', 'Basketball', 2026),
	('2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls', 'Other', 2026),
	('2026 Topps Disney Neon', 'Entertainment', 2026),
	('2025 Topps Disneyland 70th Anniversary', 'Entertainment', 2026),
	('2025-26 Topps Finest Basketball', 'Basketball', 2026),
	('2026 Topps Heritage Baseball', 'Baseball', 2026),
	('2025 Topps Marvel Studios Chrome Sapphire', 'Entertainment', 2026),
	('2025 Topps Marvel The Collector', 'Entertainment', 2026),
	('2025 Topps Museum Collection Baseball', 'Baseball', 2026),
	('2025 Topps Royalty UFC', 'MMA', 2026),
	('2026 Topps Series 1 Baseball', 'Baseball', 2026),
	('2025 Topps Stadium Club Baseball', 'Baseball', 2026),
	('2025 Topps Star Wars Smugglers Outpost', 'Entertainment', 2026),
	('2025-26 Topps Three Basketball', 'Basketball', 2026),
	('2025 Topps Universe WWE', 'Wrestling', 2026);
