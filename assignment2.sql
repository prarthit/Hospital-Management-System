show databases;
create database HMS;
use HMS;

-- create the various table and use fk approcah
-- to convert to relational model
create table Patient(patient_id int(10),Name varchar(20),sex enum('M','F','Other'),address text,contact_no bigint(11), primary key (patient_id));
create table Med_History(admission_date DATE, discharge_date DATE, diagnosis text, medication text,patient_id int(10));
create table Doctor(doctor_id int(5), name varchar(20), dept varchar(10), time_in Time, time_out time, primary key(doctor_id));
create table Appointment(patient_id int(10),doctor_id int(5));
create table Emergency_Alert(message text, doctor_id int(5));
create table Ambulance(ambulance_id varchar(20), primary key(ambulance_id), status varchar(20));
create table Ambulance_alert(message_id int(20), date_of_alert date, Address text, ambulance_id varchar(20), primary key(message_id));

create table Wards(ward_id int(10), dept varchar(10),Ward_type enum('1','2','3'),primary key(ward_id));
create table Bed_record(bed_id int(10), status enum('V','F'),ward_id int(10),patient_id int(10),date_in date, date_out date,primary key(bed_id));
create table Salary_record(dept varchar(10), staff_type enum('Nurse','Doctor','Consultant','Intern'),salary int(5));
create table Staff(staff_id int(10), name varchar(20), staff_type enum('Nurse','Intern','Consultant'),contact_no bigint(10), address varchar(20),primary key(staff_id));
create table Fund_allocation(fund_id int(10),dept varchar(20),year date, hod varchar(10),amount int(30),primary key(fund_id));
create table Lab_module(lab_test_id varchar(20),diagnosis text, lab_test_type varchar(30),patient_id int(10),primary key(lab_test_id));
create table OT(status enum('Vacant','Filled'),patient_id int(10));


-- add foreign key constraints 
alter table Med_History add foreign key (patient_id) references Patient(patient_id) on delete cascade;
alter table Appointment add foreign key (patient_id) references Patient(patient_id) on delete cascade;
alter table Appointment add foreign key (doctor_id) references Doctor(doctor_id) on delete cascade;
alter table Emergency_Alert add foreign key (doctor_id) references Doctor(doctor_id) on delete cascade;
alter table Bed_record add foreign key (ward_id) references Wards(ward_id) on delete cascade;
alter table Bed_record add foreign key (patient_id) references Patient(patient_id) on delete cascade; 
alter table Lab_module add foreign key (patient_id) references Patient(patient_id) on delete cascade;
alter table OT add foreign key (patient_id) references Patient(patient_id) on delete cascade;

Alter table Doctor add consult_capacity int(5);

-- Queries to show the schema of the tables
show columns from Patient;
show columns from Doctor;
show columns from Med_History;
show columns from Appointment;
show columns from Wards;
show columns from Bed_record;
show columns from Emergency_Alert;
show columns from Fund_allocation;
show columns from Staff;
show columns from Salary_record;
show columns from Ambulance;