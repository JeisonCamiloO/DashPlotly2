import psycopg2

engine = psycopg2.connect(
dbname="exito",
user="postgres",
password="proyecto",
host="db-proyecto2.cyfv7a2dzl8k.us-east-1.rds.amazonaws.com",
port='5432'
)
cursor = engine.cursor()

