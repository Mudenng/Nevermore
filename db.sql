CREATE DATABASE nevermore CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE nevermore
CREATE TABLE staff
(
	sid char(10) primary key, 
	name char(20), 
	age int, 
	idnumber char(18), 
    eigenface longtext,
	created timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE record
(
	rid serial primary key, 
	sid char(10), 
	type char(10), 
	rpic text, 
	created timestamp 
	default now(), 
	foreign key (sid) references staff(sid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE admin
(
	aid serial primary key, 
	name char(20), 
	pwd char(32)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE log
(
	lid serial primary key,
	sid char(10),
	type char(10),
	lpic text,
	created timestamp default now(),
	static int,
	foreign key (sid) references staff(sid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE settings
(
	sid char(20) primary key, 
	value longtext, 
	created timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE images
(
    id int auto_increment primary key not null,
    sid char(10),
    img longtext,
    foreign key (sid) references staff(sid)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
