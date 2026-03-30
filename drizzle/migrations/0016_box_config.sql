ALTER TABLE `sets` ADD `box_config` text;

-- 2024 Topps Midnight UFC: 12 boxes/case, 1 pack/box, 1 card/pack (hobby)
UPDATE `sets` SET `box_config` = '{"cards_per_pack":1,"packs_per_box":1,"boxes_per_case":12}' WHERE `id` = 9;
