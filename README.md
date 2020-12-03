# for_ICONIC

Contains code , sql and documentation related to the Data Engineer Technical challenge from ICONIC.

For Stage 1(clean): 

As part of stage one, I kept the extract separate than the cleansing. My idea is to get the data as is to a staging table and then investigate and perform the data cleansing. The python scipt "iconic_data_extraction.py" does the job of extracting the password protected zip file , converting it to a datframe and then loading that dataframe to a staging table in SQLite database.
Next step in Stage 1 involves data investigation. As part of data investigation I ran several queries to look into data discrepancies.
First things first, I looked for duplicate data and found there are duplicates in the data. So one of the task became to remove those duplicates .
Secondly, there's a hint for two columns being corrupted. One of the column that I found out is the "days_since_last_order". What I noticed is that there are multiple rows where "days_since_last_order" is greater than "days_since_first_order" and that is not expected logically.One a closer look it looked to me that for those corrupted values,they might have actually been put in hours instead of days. On dividing those values by 24 I found that the resultant values looked logical and less than days_since_first_order. So, based on this assumption I updated all those values for days_since_last_order where 
days_since_last_order > days_since_first_order  with days_since_last_order/24.
Note: refer to the data_cleansing.sql to refer to the SQLs that were used as part of investigation.


For Stage 2(ingest):

Please refer to the data_cleansing_n_ingestion.py for the final cleansing and loading of the final table customer_profile_fact.

For Stage 3(analysis): 
SQL for analysis purpose is posted in stage3_analysis.sql
Note: For the last SQL I made some assumptions which are part of the comments.

For Stage 4(productionalisation): 
Please refer to stage4_prod_strategy.txt
