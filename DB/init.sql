drop database if exists rg_manager;
create database rg_manager;

use rg_manager;

create table users(
	id int primary key auto_increment,
    username varchar(30) not null unique,
    u_password varchar(30) not null,
    joined datetime default now(),
    authorized_by varchar(30) not null
);

insert into users (username, u_password, authorized_by) values("Morty", "1234", "root");
