#---------------------------------------------------------------------------------------
# Estimando la estructura de un modelo a partir de datos: puntajes
#---------------------------------------------------------------------------------------
import pandas as pd
from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import K2Score

from pgmpy.estimators import BicScore

from infer import inferencia
import metricas as m

df = pd.read_csv("train.csv", sep = ";")
test = pd.read_csv("test.csv", sep = ";")

df = df.drop(df.columns[0], axis = 1 )

#bicscore
#k2score
#-------------------------------------------------------------------------------------------------
# ESTIMACIÓN CON EL PUNTAJE K2
#-------------------------------------------------------------------------------------------------

scoring_method = K2Score(data=df)
esth = HillClimbSearch(data=df)
estimated_modelh = esth.estimate(
    scoring_method=scoring_method, max_indegree=4, max_iter=int(1e4)
)
print("\n* DAG\n")
print(estimated_modelh)

print("\n* Nodos del modelo (variables)\n")
print(estimated_modelh.nodes())

print("\n* Arcos del modelo (relaciones)\n")
print(estimated_modelh.edges())

print("\n* Puntaje\n")
print(scoring_method.score(estimated_modelh))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from pgmpy.models import BayesianNetwork
#modelo = BayesianNetwork([('daytime/evening attendance', 'displaced'), ('daytime/evening attendance', 'scholarship holder'), ('daytime/evening attendance', 'inflation rate'), ('tuition fees up to date', 'displaced'), ('curricular units 1st sem (evaluations)', 'curricular units 1st sem (grade)'), ('curricular units 1st sem (evaluations)', 'target'), ('curricular units 1st sem (evaluations)', 'inflation rate'), ('curricular units 1st sem (grade)', 'target'), ('curricular units 1st sem (grade)', 'daytime/evening attendance'), ('curricular units 1st sem (grade)', 'previous qualification (grade)'), ('unemployment rate', 'displaced'), ('inflation rate', 'unemployment rate'), ('inflation rate', 'gdp'), ('gdp', 'unemployment rate'), ('gdp', 'tuition fees up to date'), ('target', 'tuition fees up to date'), ('target', 'scholarship holder')])
modelo = BayesianNetwork(list(estimated_modelh.edges()))

#nodos_fit = list(estimated_modelh.nodes())

#Debo quitarle las columnas al train (df) que no fueron tomadas en cuenta por la estimación del grafo
#df_fit = df[['daytime/evening attendance', 'previous qualification (grade)', 'displaced', 'tuition fees up to date', 'scholarship holder', 'curricular units 1st sem (evaluations)', 'curricular units 1st sem (grade)', 'unemployment rate', 'inflation rate', 'gdp', 'target']]
df_fit = df[list(estimated_modelh.nodes())]

from pgmpy.estimators import MaximumLikelihoodEstimator

emv = MaximumLikelihoodEstimator(model=modelo, data=df_fit)
modelo.fit(data=df_fit, estimator = MaximumLikelihoodEstimator) 

from pgmpy.inference import VariableElimination
#Modelo de inferencia
infer = VariableElimination(modelo)

test_fit = test[list(estimated_modelh.nodes())]

pred = inferencia(modelo, test_fit)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Metricas del modelo predictivo

m.metricas_modelo(test_fit, pred)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------
# ESTIMACIÓN CON EL PUNTAJE BIC
#------------------------------------------------------------------------------------------------

# scoring_method = BicScore(data=df)
# esth = HillClimbSearch(data=df)
# estimated_modelh = esth.estimate(
#     scoring_method=scoring_method, max_indegree=4, max_iter=int(1e4)
# )

# print("\n* DAG\n")
# print(estimated_modelh)

# print("\n* Nodos del modelo (variables)\n")
# print(estimated_modelh.nodes())

# print("\n* Arcos del modelo (relaciones)\n")
# print(estimated_modelh.edges())

# print("\n* Puntaje\n")
# print(scoring_method.score(estimated_modelh))