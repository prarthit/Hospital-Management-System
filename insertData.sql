use HMS;

delete from Doctor;
delete from Patient;
delete from Emergency_Alert;
delete from Appointment;
delete from Med_History;
delete from Ambulance;
delete from Ambulance_alert;
delete from Wards;
delete from Salary_record;
delete from Bed_record;
delete from Staff;
delete from Fund_allocation;
delete from Lab_module;
delete from OT;

insert into Doctor(doctor_id,name,dept,time_in,time_out,consult_capacity) values('1','Dr. Gulati','OPD','08:00:00','11:00:00',3);
insert into Doctor values('2','Dr. Yadav','Psycho','12:30:00','17:00:00',2);
insert into Doctor values('3','Dr. Pawar','Gynaec','13:00:00','18:00:00',1);
insert into Doctor values('5','Dr. Gupta','Geronto','09:00:00','13:30:00',2);
insert into Doctor values('4','Dr. Nirania','Ortho','14:00:00','19:00:00',3);


insert into Patient(patient_id,name,sex,address,contact_no) values(1,'Abhishek','M','vill-Ramnagar',60058951);
insert into Patient values(2,'Deepanshu','M','Connought',485934975);
insert into Patient values(3,'Atul','M','Hauz-Khas',48783598);
insert into Patient values(4,'Prarthit','M','Mannat',9448309);
insert into Patient values(5,'Aman','M','Srinagar',03849085);
insert into Patient values(6,'Riya','F','Rohini',349030083);
insert into Patient values(7,'Priya','F','Leh',304983);
insert into Patient values(8,'Aishwarya','F','Mathura',274937597);
insert into Patient values(9,'Alia','F','Gurugram',384989894);
insert into Patient values(10,'Rahul','M','South-4',90309828);


insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-02','2019-05-06','Malaria','MedicineX','1');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2018-05-22','2018-06-07','Dengue','MedicineX','1');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2017-04-15','2017-05-08','Diabetes','MedicineY','1');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2012-04-17','2012-05-02','Malaria','MedicineZ','1');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-05','2019-05-12','Diarhea','MedicineX','2');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2016-04-21','2016-05-13','Swine flu','MedicineX','2');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2015-04-22','2015-05-21','Ebola','MedicineX','2');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-22','2019-05-06','Cowpox','MedicineX','3');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-02-22','2019-03-06','Allgeria','MedicineX','3');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-12','2019-05-06','Asthma','MedicineX','5');
insert into Med_History(admission_date,discharge_date,diagnosis,medication,patient_id) values('2019-04-22','2019-05-06','Heart Attack','MedicineX','4');

insert into Appointment(patient_id,doctor_id) values(2,1);	

insert into Appointment(patient_id,doctor_id) values(2,2);
insert into Appointment values(7,2);
insert into Appointment values(5,1);
insert into Appointment values(3,4);
insert into Appointment values(8,3);

insert into Emergency_Alert(message,doctor_id) values('Bleeding from head',1);
insert into Emergency_Alert values('Pain in stomach',1);
insert into Emergency_Alert values('leg broken',2);
insert into Emergency_Alert values('kidney failed',3);
insert into Emergency_Alert values('heart pumping stopped',2);
insert into Emergency_Alert values('fracture in neck',4);

insert into Ambulance(ambulance_id,status) values('HR43-344','Busy');

insert into Ambulance_alert(message_id,date_of_alert,Address,ambulance_id)values('1','2019-05-03','Sharma Appartement,Punjabi Bagh','HR43-344');

insert into Wards(ward_id,dept,Ward_type) values('1','Pysho','1');	
insert into Wards(ward_id,dept,Ward_type) values('2','Pysho','2');
insert into Wards(ward_id,dept,Ward_type) values('3','Pysho','3');
insert into Wards(ward_id,dept,Ward_type) values('4','Ortho','1');
insert into Wards(ward_id,dept,Ward_type) values('5','Ortho','2');
insert into Wards(ward_id,dept,Ward_type) values('6','Ortho','3');
insert into Wards(ward_id,dept,Ward_type) values('7','Neuro','1');	
insert into Wards(ward_id,dept,Ward_type) values('8','Neuro','2');
insert into Wards(ward_id,dept,Ward_type) values('9','Cardio','1');
insert into Wards(ward_id,dept,Ward_type) values('10','Cardio','2');
insert into Wards(ward_id,dept,Ward_type) values('11','Gyano','1');	

insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('1','F','1','1','2019-04-02','2019-05-06');
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('2','F','2','2','2019-04-05','2019-05-12');
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('3','F','3','3','2019-04-22','2019-04-22');
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('4','F','4','4','2019-04-22','2019-05-06');
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('5','F','5','5','2019-04-22','2019-05-06');
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('6','V','1',NULL,NULL,NULL);
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('7','V','2',NULL,NULL,NULL);
insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('8','V','3',NULL,NULL,NULL);


insert into Ambulance values('HR56-354','Vacant');
insert into Ambulance values('MR77-244','Vacant');
insert into Ambulance values('PS51-845','Busy');
insert into Ambulance values('NH64-939','Vacant');

insert into Ambulance_alert(message_id,date_of_alert,Address,ambulance_id)values('1','2019-05-03','Sharma Appartement,Punjabi Bagh','HR43-344');	

insert into Bed_record(bed_id,status,ward_id,patient_id,date_in,date_out)values('1','F','1','2','2019-03-05','2019-03-31');


insert into Salary_record(dept,staff_type,salary)values('Pysho','Nurse','13000');
insert into Salary_record values('Pysho','Doctor','50000');
insert into Salary_record values('OPD','Nurse','15000');
insert into Salary_record values('OPD','Doctor','52000');
insert into Salary_record values('Gynaecologist','Nurse','17000');
insert into Salary_record values('Gynaecologist','Doctor','45000');
insert into Salary_record values('Ortho','Doctor','60000');
insert into Salary_record values('Gerontologist','Doctor','30000');

insert into Staff(staff_id,name,staff_type,contact_no,address)values('1','Suzan','Nurse',9433443243,'Indra-vihar');
insert into Fund_allocation(fund_id,dept,year,hod,amount)values('1','Pyscho','2019-01-01','Dr Gulati','423435');
insert into Lab_module(lab_test_id,diagnosis,lab_test_type,patient_id)values('1','Low Platelete','Blood Test','1');
insert into OT(status,patient_id)values('Vacant',NULL);