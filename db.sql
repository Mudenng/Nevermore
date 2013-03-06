CREATE TABLE staff
(
	sid char(10) primary key, 
	name char(20), 
	age int, 
	idnumber char(18), 
	spic text, 
	created timestamp default now()
);

CREATE TABLE record
(
	rid serial primary key, 
	sid char(10), 
	type char(10), 
	rpic text, 
	created timestamp 
	default now(), 
	foreign key (sid) references staff(sid)
);

CREATE TABLE admin
(
	aid serial primary key, 
	name char(20), 
	pwd char(32)
);

CREATE TABLE log
(
	lid serial primary key,
	sid char(10),
	type char(10),
	lpic text,
	created timestamp default now(),
	static int,
	foreign key (sid) references staff(sid)
);