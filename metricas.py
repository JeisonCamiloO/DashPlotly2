from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

def metricas_modelo(test, pred):
    print("\n------------------- MÉTRICAS DEL MODELO -------------------------")
    print("\nAciertos: ", accuracy_score(test.loc[:,"target"], pred, normalize=False)) 
    print("\nTasa de Aciertos: ", accuracy_score(test.loc[:,"target"], pred)) 
    print("\nMatriz de confusion: ", confusion_matrix(test.loc[:,"target"], pred, labels=["Dropout", "Graduate","Enrolled"]).ravel()) 
    print("\n-----------------------------------------------------------------------------------\n")

    #Sensibilidad
    from sklearn.metrics import recall_score

    recall = recall_score(test.loc[:, "target"], pred, labels=["Dropout", "Graduate", "Enrolled"], average=None)
    print("\nSensibilidad (Recall): ", recall)


    #Exactitud
    from sklearn.metrics import precision_score

    precision = precision_score(test.loc[:, "target"], pred, labels=["Dropout", "Graduate", "Enrolled"], average=None)
    print("\nExactitud (Precision): ", precision)


    # #ROC
    # from sklearn.metrics import roc_curve, roc_auc_score
    # import matplotlib.pyplot as plt
    # # Calcular la puntuación AUC
    # auc = roc_auc_score(test.loc[:, "target"], pred)

    # # Calcular la curva ROC
    # fpr, tpr, _ = roc_curve(test.loc[:, "target"], pred, pos_label="Graduate")

    # # Graficar la curva ROC
    # plt.figure()
    # plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.2f})')
    # plt.xlabel('Tasa de Falsos Positivos (FPR)')
    # plt.ylabel('Tasa de Verdaderos Positivos (TPR)')
    # plt.title('Curva ROC')
    # plt.legend(loc='lower right')
    # plt.show()

    #Puntaje BIC
    #Puntaje K2
    #Es necesario comparar los modelos por puntaje o por efectividad?
