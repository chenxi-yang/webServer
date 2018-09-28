create database if not exists appUserData;
use appUserData;
create table if not exists `users`(
    `user_id` int NOT NULL AUTO_INCREMENT,
    `user_username` varchar(45) NULL,
    `user_password` varchar(45) NULL,
    primary key(`user_id`)
);
create table if not exists `user_plan`(
    `user_id` int NOT NULL,
    `plan_id` int NOT NULL AUTO_INCREMENT,
    `start_time` TIMESTAMP NULL,
    `end_time` TIMESTAMP NULL,
    `plan_name` TEXT NULL,
    primary key(`plan_id`)
);
create table if not exists `app_screen_time`(
    `screen_time_id` int NOT NULL AUTO_INCREMENT,
    `start_time` TIMESTAMP NULL,
    `end_time` TIMESTAMP NULL,
    `app_name` varchar(45),
    primary key(`screen_time_id`)
);
create table if not exists `app_notification`(
    `notification_id` int NOT NULL AUTO_INCREMENT,
    `notification_time` TIMESTAMP NOT NULL,
    `notification_type` TINYTEXT,
    `app_name` varchar(45),
    primary key(`notification_id`)
);
