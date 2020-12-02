--customer_profile_fact is the final cleansed table after removing duplictes and fixing the column days_since_last_order

--What was the total revenue to the nearest dollar for customers who have paid by credit card?
select
round(sum(revenue)) total_revenue_cc_payments
from
customer_profile_fact
WHERE cc_payments > 0

--What percentage of customers who have purchased female items have paid by credit card?
SELECT (b.customers_with_female_item_paid_by_cc*100) / b.total_customers_with_female_item percent_cust_w_female_item_n_cc
from
(SELECT
sum(case when female_items > 0 then 1 else 0 end) total_customers_with_female_item,
sum(case when female_items > 0 and cc_payments > 0 then 1 else 0 end) customers_with_female_item_paid_by_cc
from
customer_profile_fact)b

--What was the average revenue for customers who used either iOS, Android or Desktop?
select
round(total_rev/cust_count) avg_cust_revenue
from
(select
sum(revenue) total_rev,
count(customer_id) cust_count
from
customer_profile_fact
where
ios_orders > 0 or android_orders > 0 or desktop_orders > 0)

--We want to run an email campaign promoting a new mens luxury brand. Can you provide a list of customers we should send to?
--assumptions: include customers who purchased mens' (apparel, footwear,accessories,sport brand) as well as unisex items; 
--Also , they spend on average $1000 per order assuming luxury brand prices in that range. 
--is_newsletter_subscriber is also a filter we can consider if we want to show loyalty to the newsletter subscribers but for a new product launch it is better to reach out to broader audiences.
--Also , put a filter to consider customers whose last purchase was within 3 years.3 years would exclude some old customer accounts which didn't make any purchase 
--but at the same time would tempt some active customers who were not buying recently to come back and check the new luxury line along with the customers who are already making recent purchases.
--there can me many more criteria added to this.
select customer_id 
from
(select customer_id ,
revenue/orders avg_spent_per_order
from 
customer_profile_fact
where mapp_items> 0 or macc_items > 0 or mftw_items > 0 or mspt_items > 0 or unisex_items > 0 
--and is_newsletter_subscriber = 'Y'
and days_since_last_order < 1095)
where avg_spent_per_order > 1000
