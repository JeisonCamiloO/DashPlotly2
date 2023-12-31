import pandas as pd
from pgmpy.models import BayesianNetwork
from sklearn.model_selection import train_test_split
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

from infer import inferencia, prediccion_dash_infer
import metricas as m

#Lectura de datos
df = pd.read_csv("data_discreta.csv", header = 0, index_col=0, sep=";")
df = df.astype('category')

#Modelo con estructura inicial sin parámetros
mod_fit_mv = BayesianNetwork([("curricular units 1st sem (grade)","target"),("course","target"), ("tuition fees up to date","target"), ("scholarship holder","target"), 
                             ("daytime/evening attendance","course"), ("curricular units 1st sem (evaluations)","course"),("displaced","tuition fees up to date"),
                             ("unemployment rate","displaced"),("inflation rate","displaced"),("gdp","displaced"),("curricular units 1st sem (evaluations)","previous qualification (grade)")])

#División entre Train y Test
train, test = train_test_split(df, test_size=0.2, random_state=101)

train.to_csv("train.csv", sep = ";", index = False)
test.to_csv("test.csv", sep = ";", index = False)

#Modulo de ajuste para algunas CPDs del nuevo modelo
emv = MaximumLikelihoodEstimator(model=mod_fit_mv, data=train)

#Parámetros obtenidos con la estumación de Máxima verosimilitud
mod_fit_mv.fit(data=train, estimator = MaximumLikelihoodEstimator) 

#Modelo de inferencia
infer = VariableElimination(mod_fit_mv)

#Se realiza la inferencia
pred = inferencia(mod_fit_mv, test)

#Función que pasa la predicción según los valores introducidos en el dash
def prediccion_dash(ve):
    return prediccion_dash_infer(mod_fit_mv, ve)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Metricas del modelo predictivo
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

m.metricas_modelo(test, pred, "ORIGINAL")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Modelo con PUNTAJES
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pgmpy.utils import get_example_model
from pgmpy.metrics import structure_score

print("\n* MODELO ORIGINAL - PUNTJAE: BIC \n")
print(structure_score(mod_fit_mv, train, scoring_method="bic"))

print("\n* MODELO ORIGINAL - PUNTJAE: K2 \n")
print(structure_score(mod_fit_mv, train, scoring_method="k2"))


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SERIALIZACIÓN
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pickle

filename='serializacion/modelo1-original.pkl'
with open(filename,'wb') as file:
    pickle.dump(mod_fit_mv, file)
    file.close()