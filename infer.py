from pgmpy.inference import VariableElimination

#Predicciones

#Función que genera el vector de la predicción
def inferencia(modelo, test):

    infer = VariableElimination(modelo)

    pred = []

    for i in range(len(test)):

        evidencias = {}

        for j in range(len(test.columns)):
            if test.columns[j] != "target":
                evidencias[test.columns[j]] = test.iloc[i][j]

        pred_test = infer.map_query(["target"], 
                            evidence=evidencias, show_progress=False)
        
        pred.append(pred_test["target"])

    return pred

        # course_v = test.iloc[i][0]
        # daytime_v = test.iloc[i][1]
        # previous_qualification_grade_v = test.iloc[i][2]
        # displaced_v = test.iloc[i][3]
        # tuition_v = test.iloc[i][4]
        # scholarship_v = test.iloc[i][5]
        # curricular_units_1sem_evaluations_v = test.iloc[i][6]
        # curricular_units_1sem_grade_v = test.iloc[i][7]
        # unemployment_rate_v = test.iloc[i][8]
        # inflation_rate_v = test.iloc[i][9]
        # gdp_v = test.iloc[i][10]

        ##infer.predict



        # pred_test = infer.map_query(["target"], 
        #                             evidence={"course": course_v, "daytime/evening attendance": daytime_v, "previous qualification (grade)": previous_qualification_grade_v, 
        #                                     "displaced":displaced_v, "tuition fees up to date": tuition_v, "scholarship holder": scholarship_v, 
        #                                     "curricular units 1st sem (evaluations)": curricular_units_1sem_evaluations_v, "curricular units 1st sem (grade)":curricular_units_1sem_grade_v,
        #                                     "unemployment rate":unemployment_rate_v, "inflation rate":inflation_rate_v,
        #                                     "gdp":gdp_v}, show_progress=False)
        # pred.append(pred_test["target"])
    

#Función que pasa la predicción según los valores introducidos en el dash
def prediccion_dash_infer(modelo, ve ):

    infer = VariableElimination(modelo)

    pred_test = infer.map_query(["target"], 
                            evidence={"course": ve[0], "daytime/evening attendance": ve[1], "previous qualification (grade)": ve[2], 
                                        "displaced":ve[3], "tuition fees up to date": ve[4], "scholarship holder": ve[5], 
                                        "curricular units 1st sem (evaluations)": ve[6], "curricular units 1st sem (grade)":ve[7],
                                        "unemployment rate":ve[8], "inflation rate":ve[9],
                                        "gdp":ve[10]}, show_progress=False)
    return pred_test
