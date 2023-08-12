create table customer(
	c_email varchar(50),
	name varchar(30), 
	c_pass varchar(20),
	c_address varchar(50),
	c_mobile varchar(10),
	primary key (c_email));

create table employee(
	e_email varchar(50),
	name varchar(30),
	dob varchar(20),
	e_pass varchar(20),
	e_address varchar(50),
	e_mobile varchar(10),
	salary numeric(10,2),
	primary key (e_email));

create table admin(
	admin_ID int,
	name varchar(20),
	a_pass varchar(20),
	primary key (admin_ID));

create table food(
	foodid int,
	foodname varchar(20),
	categery varchar(20),
	price int,
	primary key (foodid));

create table order1(
	ordid int,
	c_email varchar(20),
	foodid int,
	quantity int,
	bill int,
	primary key (ordid, c_email, foodid),
	foreign key (c_email) references customer(c_email) 
		on delete cascade,
	foreign key (foodid) references food(foodid) 
		on delete cascade);

create table delivery(
	delid int auto_increment,
	ordid int,
	c_email varchar(50),
	e_email varchar(50),
	delcharge int,
	deldate varchar(20),
	deltime varchar(20),
	primary key (delid),
	foreign key (ordid, c_email) references order1(ordid, c_email) 
		on delete cascade,
	foreign key (e_email) references employee(e_email)
		on delete cascade);
	
