import psycopg2
from dotenv import load_dotenv # pip install python-dotenv
import os

env_path="env/app.env"

# load env 
load_dotenv(dotenv_path=env_path)

# extract env variables
USER=os.getenv('user')
PASSWORD=os.getenv('password')
HOST=os.getenv('host')
PORT=os.getenv('port')
DBNAME=os.getenv('dbname')

engine = psycopg2.connect(
dbname = DBNAME,
user = USER,
password = PASSWORD,
host = HOST,
port = PORT
)

print(engine)

cursor = engine.cursor()

consulta = "SELECT Target FROM ESTUDIANTE WHERE Admission_grade >= 170;"

cursor.execute(consulta)
result = cursor.fetchall()
print(result)