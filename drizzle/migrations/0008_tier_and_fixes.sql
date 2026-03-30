ALTER TABLE `sets` ADD COLUMN `tier` text NOT NULL DEFAULT 'Standard';
--> statement-breakpoint
UPDATE `sets` SET `tier` = 'Chrome' WHERE `id` IN (11, 15, 19);
--> statement-breakpoint
UPDATE `sets` SET `tier` = 'Sapphire' WHERE `id` IN (10, 21);
--> statement-breakpoint
UPDATE `sets` SET `league` = 'Olympics' WHERE `id` = 15;
--> statement-breakpoint
ALTER TABLE `topps_sets` ADD COLUMN `tier` text NOT NULL DEFAULT 'Standard';
--> statement-breakpoint
UPDATE `topps_sets` SET `tier` = 'Chrome' WHERE `name` IN (
  '2025-26 Topps Chrome Cactus Jack Basketball',
  '2025 Topps Chrome McDonald''s All-American Basketball',
  '2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls'
);
--> statement-breakpoint
UPDATE `topps_sets` SET `tier` = 'Sapphire' WHERE `name` IN (
  '2025-26 Topps Finest Basketball',
  '2025 Topps Chrome Sapphire Formula 1',
  '2025-26 Topps Chrome Basketball Sapphire',
  '2025 Bowman Draft Baseball Sapphire Edition',
  '2025 Topps Marvel Studios Chrome Sapphire'
);
