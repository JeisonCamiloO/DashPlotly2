from csv import reader

with open("data.csv", "r") as archivo, open("bdatos.sql", "w") as archivo_sql:

    archivo_sql.write("BEGIN;\n\n")
    archivo_sql.write("SET client_encoding = 'LATIN1';\n\n")

    
    
    lector = reader(archivo)

    columnas = next(lector)
    columnas = columnas[0]
    columnas = columnas[3:] #Aparecen 3 simbolos extraños que no deberian estar dentro de la palabra 'Marital status' por eso se eliminan de la cadena

    columnas = columnas.replace(";", ",")
    columnas = columnas.replace(" ", "_")
    columnas = columnas.replace("\t", "")
    columnas = columnas.replace('"',"")
    columnas = columnas.replace("(", "")
    columnas = columnas.replace(")", "")
    columnas = columnas.replace("/", "")
    columnas = columnas.replace("'", "")

    columnas_split = columnas.split(",")

    for i in range(0,len(columnas_split)):
        if columnas_split[i] == "Previous_qualification_grade" or columnas_split[i] == "Admission_grade" or columnas_split[i] == "Curricular_units_1st_sem_grade" or columnas_split[i] == "Curricular_units_2nd_sem_grade" or columnas_split[i] == "Unemployment_rate" or columnas_split[i] == "Inflation_rate" or columnas_split[i] == "GDP":
            columnas_split[i] = "\n"+columnas_split[i] + " REAL NOT NULL,"
        else:
            if columnas_split[i] != "Target":
                columnas_split[i] = "\n"+columnas_split[i] + " INTEGER  NOT NULL,"
            else:
                columnas_split[i] = "\n"+columnas_split[i] + " TEXT NOT NULL,"
    columnas_t = " ".join(columnas_split)[:-1]

    #Creación de la tabla con sus atributos
    archivo_sql.write(f"CREATE TABLE ESTUDIANTE ({columnas_t});")
    archivo_sql.write("\n\n")

    #Llenar la tabla
    archivo_sql.write(f"COPY ESTUDIANTE ({columnas}) FROM stdin;")
    for linea in lector:
        archivo_sql.write("\n"+ linea[0].replace(";", "\t"))
    archivo_sql.write("\n\.\n")
    archivo_sql.write("COMMIT;")


        


