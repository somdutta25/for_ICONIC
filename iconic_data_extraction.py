#This python script takes an encrypted zip file and decodes it using a password string passed as command line parameter.
#Next it creates a pandas dataframe out of the data file (after extraction)
#This file is then loaded to a Sqllite database table called : stg_iconic_user_data to implement data cleansing.
import hashlib
from zipfile import ZipFile
import pandas as pd
from sqlalchemy import create_engine
import sys

PASS_STRING = sys.argv[1]

#PASS_STRING = 'welcometotheiconic'
#Path where the zip file was stored after downloading from the github link.
ZIP_FILE_PATH = '/Users/somduttasanyal/iconic/test_data.zip'
#Path where the extracted zip file is to be kept.
EXTRACT_FILE_PATH = '/Users/somduttasanyal/iconic/landing2'
#Fully qualified file name
EXTRACT_FILE_NAME = EXTRACT_FILE_PATH+'/data.json'
#database name for the sqlite database where datafranes will be loaded as tables.
SQLITE_DB_NAME = 'sqlite:///iconic_test_a.db'
#Name of the table where we want to load the dataset from dataframe
SQLITE_STG_TABLE_NAME = 'stg_iconic_user_data_678'

#Creates the passkey
def create_unhash_pass(pwd_string):

    ENCR_PASS_CODE = hashlib.sha256(bytes(PASS_STRING,'utf-8')).hexdigest()
    return ENCR_PASS_CODE

#Unzips the file using passkey
def unzip_file_using_pass(encr_pwd,EXTRACT_FILE_PATH):
    zip_file = ZIP_FILE_PATH
    with ZipFile(zip_file) as zf:
        zf.extractall(path=EXTRACT_FILE_PATH, pwd=bytes(encr_pwd,'utf-8'))

#Creates a sqlite connection
def create_sqlite_connection(SQLITE_DB_NAME):
    engine = create_engine(SQLITE_DB_NAME, echo=True)
    sqlite_connection = engine.connect()
    return sqlite_connection

#Load dataframe to sqlite
def load_df_to_sqlite(EXTRACT_FILE_NAME,SQLITE_TABLE_NAME,sqlite_connection):
    #create a pandas dataframe with the extracted file
    df = pd.read_json(r"{}".format(EXTRACT_FILE_NAME),lines=True)
    df.to_sql(SQLITE_STG_TABLE_NAME, sqlite_connection, if_exists='fail')

def main():
    encr_pwd = create_unhash_pass(PASS_STRING)
    unzip_file_using_pass(encr_pwd,EXTRACT_FILE_PATH)
    sql_conn = create_sqlite_connection(SQLITE_DB_NAME)
    load_df_to_sqlite(EXTRACT_FILE_NAME,SQLITE_STG_TABLE_NAME,sql_conn)

if __name__ == '__main__':
    main()
