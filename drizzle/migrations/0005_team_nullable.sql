-- Make player_appearances.team nullable to support cards without team info
-- (e.g., historical autograph signers, musicians on crossover cards)
ALTER TABLE `player_appearances` DROP COLUMN `team`;
--> statement-breakpoint
ALTER TABLE `player_appearances` ADD COLUMN `team` text;
