select *,concat('employee_',employee_id)
from employees
where full_name is null;

update employees
set full_name = concat('employee_',employee_id)
where full_name is null;


select *
from
(
select *,row_number()over(partition by full_name,gender,birth_date,hire_date,department,position) as row_num
from employees
)t
where row_num>1;

select *
from employees
where gender is null or birth_date is null or hire_date is null or department is null or position is null
or salary is null or email is null or phone_number is null or city is null or country is null or status is null;


select birth_date , date_sub(birth_date,interval 50 year)
from employees
where birth_date > curdate();

update employees
set birth_date = date_sub(birth_date,interval 50 year)
where birth_date > curdate();

select * 
from employees
where hire_date > curdate();



select *
from employees
 where email not like '%@%';
 
 select phone_number,regexp_replace(phone_number,'[^0-9x]','')
 from employees;
 
 update employees
 set phone_number = regexp_replace(phone_number,'[^0-9x]','');
 
 
 
 
 select employee_id,case when length(phone_number)=10 then
 concat('(',substring(phone_number,1,3),')',' ',substring(phone_number,4,3),' ',substring(phone_number,7)) else 
 
 concat('(',substring(phone_number,1,3),')',' ',substring(phone_number,4,3),' ',substring(phone_number,7,4),' ',substring(phone_number,11))
 
 end as phone_number
 from employees;
 
 
 update employees t1
 join
 (
 select employee_id,case when length(phone_number)=10 then
 concat('(',substring(phone_number,1,3),')',' ',substring(phone_number,4,3),' ',substring(phone_number,7)) else 
 
 concat('(',substring(phone_number,1,3),')',' ',substring(phone_number,4,3),' ',substring(phone_number,7,4),' ',substring(phone_number,11))
 
 end as phone_number_edit
 from employees
 )t2
 
 on t1.employee_id = t2.employee_id
 set t1.phone_number = t2.phone_number_edit;
 
 
 select *
 from employees
 where salary <0;
 
 update employees
 set salary = salary*-1
 where salary <0;
 
with cte as (
  select salary, ntile(4) over (order by salary) as quartile
  from employees
),
iqr_values as (
  select 
    max(case when quartile = 1 then salary end) as Q1,
    max(case when quartile = 3 then salary end) as Q3
  from cte
),
bounds as (
  select e.salary,  
    q.Q1, q.Q3,
    (q.Q1 - 1.5 * (q.Q3 - q.Q1)) as lower_bound,
    (q.Q3 + 1.5 * (q.Q3 - q.Q1)) as upper_bound
  from iqr_values q
  join employees e
),
outlier as
(
select salary as out_salary
from bounds 
where salary < lower_bound or salary > upper_bound
),
avg_salary_in_not_outliers as
(
select *
from employees
where salary not in (select salary from outlier)
)
update employees
set salary = (select round(avg(salary),2) from avg_salary_in_not_outliers)
where salary in (select out_salary from outlier);

# Data Analysis


select status,round(avg(salary),2)
from employees
group by status
order by round(avg(salary),2) desc;



select gender,count(*)*100/(select count(*) from employees)
from employees
group by gender;


select status, count(*)
from employees
group by status
order by count(*) desc;

select count(if(gender='Male',1,null)) as count_of_male,count(if(gender='Female',1,null)) as count_of_female
from employees
where status = 'Resigned';


select department,round(avg(salary),2),count(*),count(if(gender = 'Male',1,null)) as count_of_male,
count(if(gender = 'Female',1,null)) as count_of_female
from employees
where status = 'Resigned'
group by department
order by round(avg(salary),2) desc;

select *
from
(
select *,timestampdiff(year,hire_date,curdate()) as year_of_company
from employees
) t
where status = 'Resigned' and year_of_company <=0;

select department,position,count(*)
from employees
where status = 'Resigned'
group by department, position
order by department, count(*) desc;


select country,count(*)
from employees
where status = 'Resigned'
group by country
order by count(*) desc
limit 10;


select country,position,count(*)
from employees
group by country,position
order by country,position;

select date_format(hire_date,"%Y-%m") as hire_month,count(*)
from employees
group by hire_month
order by hire_month;


select year(hire_date),count(*)
from employees
group by year(hire_date)
order by count(*) desc
limit 5;


select department,hire_date_in_year,count_of_employees
from 
(
select department,year(hire_date) as hire_date_in_year,count(*) as count_of_employees
,row_number()over(partition by department order by count(*) desc) as row_num
from employees
group by department ,year(hire_date)
)t


where row_num=1;


select *
from
(
select gender,year(hire_date) as hire_date,count(*),row_number()over(partition by gender order by count(*) desc) as row_num
from employees
group by gender,year(hire_date)
)t
where row_num = 1;

select department,position,count_employees
from
(
select department,position,count(*)as count_employees,row_number()over(partition by department order by count(*) desc) as row_num
from employees
where status = 'Resigned'
group by department,position
)t
where row_num = 1;


select department,position,count_employees
from
(
select department,position,count(*)as count_employees,row_number()over(partition by department order by count(*) desc) as row_num
from employees
where status = 'Active'
group by department,position
)t
where row_num = 1;

select department,position,avg_salary
from
(
select department,position,round(avg(salary),2) as avg_salary
,row_number()over(partition by department order by round(avg(salary),2)desc) as row_num
from employees
group by department,position
)t
where row_num = 1;


select *
from employees