--For finding duplicate records:
select 
count(1)
from
(select 
sacc_items,
work_orders,
female_items,
is_newsletter_subscriber,
male_items,
afterpay_payments,
msite_orders,
wftw_items,
mapp_items,
orders,
cc_payments,
curvy_items,
paypal_payments,
macc_items,
cancels,
revenue,
returns,
other_collection_orders,
parcelpoint_orders,
customer_id,
android_orders,
days_since_last_order,
vouchers,
average_discount_used,
shipping_addresses,
redpen_discount_used,
mftw_items,
days_since_first_order,
unisex_items,
home_orders,
coupon_discount_applied,
desktop_orders,
ios_orders,
apple_payments,
wspt_items,
wacc_items,
items,
mspt_items,
devices,
different_addresses,
wapp_items,
other_device_orders,
average_discount_onoffer,
count(1) cnt
FROM 
stg_iconic_user_data
group by 
sacc_items,
work_orders,
female_items,
is_newsletter_subscriber,
male_items,
afterpay_payments,
msite_orders,
wftw_items,
mapp_items,
orders,
cc_payments,
curvy_items,
paypal_payments,
macc_items,
cancels,
revenue,
returns,
other_collection_orders,
parcelpoint_orders,
customer_id,
android_orders,
days_since_last_order,
vouchers,
average_discount_used,
shipping_addresses,
redpen_discount_used,
mftw_items,
days_since_first_order,
unisex_items,
home_orders,
coupon_discount_applied,
desktop_orders,
ios_orders,
apple_payments,
wspt_items,
wacc_items,
items,
mspt_items,
devices,
different_addresses,
wapp_items,
other_device_orders,
average_discount_onoffer
having count(1)> 1)  

--249 rows were returned.

------------------
--SQL which helped to discover the issue with days_since_last_order

select count(1)
from
(select customer_id , days_since_first_order,days_since_last_order
from stg_iconic_user_data 
where 
days_since_last_order > days_since_first_order)  --43602

--Also wanted to verify if by days_since_last_order/24 ,the data looks correct or not :
select count(1)
from
(select customer_id , days_since_first_order ,days_since_last_order ,days_since_last_order/24 rectified_days_since_last_order
from stg_iconic_user_data
where days_since_last_order > days_since_first_order)b
where b.rectified_days_since_last_order > b.days_since_first_order
--no rows were returned which gave the confidence that my assumption was right.
