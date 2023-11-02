import psycopg2

engine = psycopg2.connect(
dbname="exito",
user="****",
password="****",
host="db-proyecto2.cyfv7a2dzl8k.us-east-1.rds.amazonaws.com",
port='5432'
)

print(engine)

cursor = engine.cursor()

consulta = "SELECT Target FROM ESTUDIANTE WHERE Admission_grade >= 170;"

cursor.execute(consulta)
result = cursor.fetchall()
print(result)