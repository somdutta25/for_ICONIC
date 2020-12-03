#This code removed duplicates from stg_iconic_user_data table and also fixed the days_since_last_order issue.
import sqlite3

SQLITE_DB_NAME = '/Users/somduttasanyal/iconic/iconic_db.db'

#Creates a sqlite connection.
def create_sqlite_connection(SQLITE_DB_NAME):
    sqlite_connection = sqlite3.connect(SQLITE_DB_NAME)
    return sqlite_connection
#remove the duplicates.
def duplicate_remove(sql_conn):
    cur = sql_conn.cursor()
    dup_qry = """create table dedup_stg_iconic_user_data as
                    select
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
                    macc_items,cancels,
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
                    average_discount_onoffer"""
    cur.execute(dup_qry)

#to fix days_since_last_order
def fix_column(sql_conn):
    cur = sql_conn.cursor()
    upd_qry = """update dedup_stg_iconic_user_data
                set days_since_last_order = days_since_last_order/24
                where days_since_last_order > days_since_first_order"""
    cur.execute(upd_qry)

#customer_profile_fact is created seperately using DDL in customer_profile_fact_ddl.sql
def load_fact(sql_conn):
    cur = sql_conn.cursor()
    load_qry = """insert into customer_profile_fact select * from dedup_stg_iconic_user_data"""
    cur.execute(load_qry)


def main():
    sql_conn = create_sqlite_connection(SQLITE_DB_NAME)
    with sql_conn:
        duplicate_remove(sql_conn)
        fix_column(sql_conn)
        load_fact(sql_conn)


if __name__ == '__main__':
    main()
