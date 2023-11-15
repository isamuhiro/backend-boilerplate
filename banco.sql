drop schema cccat14 cascade;

create schema cccat14;

create table cccat14.account (
	account_id uuid primary key,
	name text not null,
	email text not null,
	cpf text not null,
	car_plate text null,
	is_passenger boolean not null default false,
	is_driver boolean not null default false
);

create table cccat14.ride (
	ride_id uuid primary key,
	passenger_id uuid,
	driver_id uuid,
	fare numeric,
	distance numeric,
	status text,
	from_lat numeric,
	from_long numeric,
	to_lat numeric,
	to_long numeric,
	date timestamp
);

insert into account (account_id, name, email, cpf, car_plate, is_passenger, is_driver) values ('e177e860-83b2-11ee-b962-0242ac120002', 'isamu', 'isamuhirahata@gmail.com', '03646768096', 'abc-1234',true, false);

select * from account a;