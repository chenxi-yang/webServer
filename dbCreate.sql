create database if not exists appUserData;
use appUserData;
create table if not exists `users`(
    `user_username` varchar(45),
    `user_password` varchar(45) NULL,
    primary key(`user_username`)
);

