CREATE DATABASE nevermore CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';

USE nevermore

CREATE TABLE staff
(
	sid char(20) primary key,
    pwd char(32),
	name char(20), 
	age int, 
	idnumber char(20),
    department int,
    ondutytime char(20),
    offdutytime char(20),
    eigenface longtext,
    distance double,
	created timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE record
(
	rid serial primary key,
	sid char(20),
	rtype int,
    rstate int,
	rimage text,
	rtime timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE admin
(
	aid serial primary key,
	name char(20),
	pwd char(32),
    atype int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE log
(
	lid serial primary key,
	uid char(20),
	ltype int,
	content text,
	ltime timestamp default now()
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE setting
(
	skey char(20) primary key,
	value longtext,
	created timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE image
(
    id serial primary key,
    sid char(20),
    img longtext,
	created timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
