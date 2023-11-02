from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

def metricas_modelo(test, pred):
    print("\n--------- MÉTRICAS DEL MODELO ------------")
    print("\nAciertos: ", accuracy_score(test.loc[:,"target"], pred, normalize=False)) 
    print("\nTasa de Aciertos: ", accuracy_score(test.loc[:,"target"], pred)) 
    print("\nMatriz de confusion: ", confusion_matrix(test.loc[:,"target"], pred, labels=["Dropout", "Graduate","Enrolled"]).ravel()) 
    print("\n-----------------------------------------\n")
