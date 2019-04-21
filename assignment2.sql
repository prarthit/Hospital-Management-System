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

-- insert queries 
insert into Doctor(doctor_id,name,dept,time_in,time_out,consult_capacity) values('1','Dr. Gulati','OPD','01:00:00','11:00:00',20);
insert into Patient(patient_id,name,sex,address,contact_no) values(1,'Abhishek','M','vill-Ramnagar',60058951);
insert into Patient(patient_id,name,sex,address,contact_no) values(2,'Deepanshu','M','Indore',9454354534);
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-02','2019-05-06','Malaria','Paracetamole','1');	
insert into Appointment(patient_id,doctor_id) values(2,1);
insert into Emergency_Alert(message,doctor_id) values('Bleeding from head',1);
insert into Ambulance(ambulance_id,status) values('HR43-344','Busy');
insert into Ambulance_alert(message_id,date_of_alert,Address,ambulance_id)values('1','2019-05-03','Sharma Appartement,Punjabi Bagh','HR43-344');
insert into Wards(ward_id,dept,Ward_type) values('1','Pysho','2');	
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('1','F','1','2','2019-03-05','2019-03-31');
insert into Salary_record(dept,staff_type,salary)values('Pysho','Nurse','13000');
insert into Staff(staff_id,name,staff_type,contact_no,address)values('1','Suzan','Nurse',9433443243,'Indra-vihar');
insert into Fund_allocation(fund_id,dept,year,hod,amount)values('1','Pyscho','2019-01-01','Dr Gulati','423435');
insert into Lab_module(lab_test_id,diagnosis,lab_test_type,patient_id)values('1','Low Platelete','Blood Test','1');
insert into OT(status,patient_id)values('Vacant',NULL);
 
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