describe transactions;

select *
from 
(
select *,row_number()over(partition by transaction_id,amount_paid,payment_method) as row_num
from transactions
)t
where row_num >1;

select customer_id,count(*) as number_of_transactions
from transactions
group by customer_id
order by count(*)  desc, customer_id
limit 10;



select *,monthname(transaction_date)
from transactions;

alter table transactions
add column month_name varchar(10);
update transactions
set month_name = monthname(transaction_date);


select payment_method,round(avg(amount_paid),2) as avg_amount
from transactions
group by payment_method
order by sum(amount_paid);
 
 select payment_method,count(*)
 from transactions
 group by payment_method
 order by count(*) desc;
 
select hour(transaction_date),count(*)
from transactions
group by hour(transaction_date);
select *,(amount_paid - prev_amount) as diff_amount
from
(
select *, lag(amount_paid)over(order by transaction_date) as prev_amount
from transactions
)t;

select customer_id,month(transaction_date),avg(amount_paid)
from transactions
group by customer_id,month(transaction_date)
order by avg(amount_paid) desc;

select customer_id, sum(amount_paid)
from transactions
group by customer_id
order by sum(amount_paid) desc
limit 5;

select hour(transaction_date),sum(amount_paid)
from transactions
group by hour(transaction_date)
order by sum(amount_paid) desc
limit 10;

alter table transactions
drop column month_name;

-- العملاء المشتركين بين الأعلى نشاطًا والأعلى إنفاقًا
SELECT top_customers.customer_id,
       top_customers.total_spent,
       active_customers.number_of_transactions
FROM
(
    SELECT customer_id, SUM(amount_paid) AS total_spent
    FROM transactions
    GROUP BY customer_id
    ORDER BY total_spent DESC

) AS top_customers
JOIN
(
    SELECT customer_id, COUNT(*) AS number_of_transactions
    FROM transactions
    GROUP BY customer_id
    ORDER BY number_of_transactions DESC
) AS active_customers
ON top_customers.customer_id = active_customers.customer_id;


select t1.customer_id,total_spent,number_of_transactions
from
(
select customer_id,sum(amount_paid) as total_spent
from transactions
group by customer_id
order by total_spent desc
)t1
join
(
select customer_id, count(*) as number_of_transactions
from transactions
group by customer_id
order by number_of_transactions desc
)t2
on t1.customer_id = t2.customer_id;


select *
from transactions


