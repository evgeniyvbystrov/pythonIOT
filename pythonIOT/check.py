import os
import psycopg2

conn = psycopg2.connect(dbname=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),password=os.environ.get('DB_PASS'), host=os.environ.get('DB_HOST'))
print('Connection successful')

