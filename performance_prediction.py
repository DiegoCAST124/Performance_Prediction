# -*- coding: utf-8 -*-
"""ACD_Performance-Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZB9f0VLy2HlF_bzyJQqAbyYbQYRKRsCw

###Regresión Lineal con ScikitLearn para predecir la calificación mímima de un alumno en la aplicación de un examen

Aprendizaje Automático

Ene-Jun 2024

#Introducción

En el ámbito académico, la evaluación del rendimiento de los estudiantes es de suma importancia para comprender su progreso y brindarles el apoyo necesario. En este contexto, la capacidad de predecir la calificación de un alumno en la aplicación de un examen puede resultar invaluable para los docentes, ya que les permite identificar áreas de mejora de manera más efectiva y personalizar la enseñanza de manera más efectiva.

El conjunto de datos consiste en una serie de características que se cree puede influir en el desempeño de los estudiantes en el examen; como las horas de estudio, calificaciones previas, si realiza o no actividades extracurriculares, horas de sueño, y cuántos examenes simulacro han realizado. Para ello utilizaremos un dataset de Kaggle llamado Student Performance (Multiple Linear Regression) (https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression).

El objetivo final de este proyecto es desarrollar un modelo preciso y confiable que pueda predecir con éxito las calificaciones mínimas de los estudiantes en el examen, lo que proporcionaría información valiosa para los docentes y ayudaría a mejorar el proceso educativo en general.

#Importación de bibliotecas necesarias y preprocesamiento de datos

Importamos las bibliotecas y subibliotecas necesarios para el procedimiento.

Pandas nos permite leer y escribir en ficheros en formato CSV; así como accceder, reordenar, dividir y combinar conjuntos de datos.

Matplotlib nos ayuda a crear gráficas.

Seaborn es una herramienta de Data Visualization nos permite transformar los datos brutos en diagramas.

Scikit-learn es una biblioteca para machine learning de software libre para el lenguaje de Python, incluye varios algoritmos de clasificación, regresión y análisis de grupos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest

#Importamos el csv y lo leemos con pandas
data = pd.read_csv("Student_Performance.csv")
#Eliminamos los datos vacios
data.dropna(inplace=True)
data

"""Verificamos si existen datos nulos en nuestro dataset.

La expresión df.isnull() devuelve un DataFrame booleano que tiene el mismo tamaño que df, donde cada valor nulo es True y en caso contrario False.

.sum() se aplica al dataframe booleano, suma los valores en cada columna, la suma de cada columna dará el recuento de valores nulos en cada columna (1 True, 0 False).

El segundo .sum() se aplica al primer .sum().
"""

data.isnull().sum().sum()

#Visualizamos la informacion de los datos
data.info()

"""Como la variable de actividades extracurriculares es de tipo objeto y no de tipo numerico debemos convertirlo a una variable"""

data = data.replace({"No": 0, "Yes": 1})
data

#Histogramas
data.hist(bins=15, figsize=(15,6), layout=(2,4))
plt.show()

#Mapa de calor de la correlacion
sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
plt.title('Mapa de calor de correlacion')
correlation = data.corr()
print(correlation['Performance Index'])
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

sns.pairplot(data, x_vars=['Hours Studied','Previous Scores','Extracurricular Activities'],
              y_vars='Performance Index', height=10, aspect=1, kind='reg')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

sns.pairplot(data, x_vars=['Sleep Hours', 'Sample Question Papers Practiced'],
              y_vars='Performance Index', height=10, aspect=1, kind='reg')
plt.show()

data=data.drop(columns=['Extracurricular Activities', 'Sleep Hours', 'Sample Question Papers Practiced'])

#Describimos las caracteristicas estadisticas de las variables
data.describe()

X = data.drop("Performance Index", axis=1)
y = data["Performance Index"]

X

y

"""#Prueba de diferentes modelos de machine learning

Probaremos diferentes modelos de machine learning para conocer el más apto para este conjunto de datos.

"""

#Dividimos los datos en una proporcion de 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

"""##Regresión lineal

La regresión lineal es un algoritmo de aprendizaje supervisado que se utiliza en Machine Learning y en estadística. En su versión más sencilla, lo que haremos es “dibujar una recta” que nos indicará la tendencia de un conjunto de datos continuos (si fueran discretos, utilizaríamos Regresión Logística).

En estadísticas, regresión lineal es una aproximación para modelar la relación entre una variable escalar dependiente “y” y una o mas variables explicativas nombradas con “X”.

Valores por defecto de la Regresión Logística:


1.   fit_intercept=True
2.   copy_X=True
3.   n_jobs=None
4.   positive=False
"""

# Regresión Lineal con parámetros por defecto
lr_default = LinearRegression()
lr_default.fit(X_train, y_train)
# Predicciones
y_pred_lr = lr_default.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_lr)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_lr)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_lr)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - Linear Regression')
plt.show()

# Configuración del Pipeline para Regresión Lineal
linear_pipeline = Pipeline([
    ('scaler', MinMaxScaler()), # Escalado de los datos
    ('linear', LinearRegression()) # Modelo de Regresión Lineal
])

# Parámetros a evaluar en la búsqueda de cuadrícula para Regresión Lineal
param_grid_linear = {
    'linear__fit_intercept': [True, False], # Incluir o no el intercepto en el modelo
    'linear__copy_X': [True, False], # Hacer una copia de X
    'linear__positive': [True, False] # Forzar coeficientes positivos
}

# Búsqueda de cuadrícula con validación cruzada
grid_search_linear = GridSearchCV(linear_pipeline, param_grid_linear, cv=5, scoring='neg_mean_squared_error')
grid_search_linear.fit(X_train, y_train)

# Mejores parámetros y score obtenido
print("Mejores parámetros para Regresión Lineal: ", grid_search_linear.best_params_)

best_model = grid_search_linear.best_estimator_

# Predicciones
y_pred_linear_best = grid_search_linear.predict(X_test)

# Calculamos las métricas
mse = mean_squared_error(y_test, y_pred_linear_best)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_linear_best)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_linear_best)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - Linear Regression Best')
plt.show()

"""##Máquinas de vectores de soporte SVM

Las máquinas de vectores de soporte o máquinas de vector soporte (del inglés support-vector machine SVM) son un conjunto de algoritmos de aprendizaje supervisado desarrollados por Vladimir Vapnik y su equipo en los laboratorios AT&T Bell.
Están propiamente relcionados con problemas de clasificación y regresión. Dado un conjunto de muestras podemos etiquetar las clases y formar una SVM para construir un modelo que prediga la clase de una nueva muestra. Una SVM es un modelo que representa a los puntos de muestra en el espacio, separando las clases a 2 espacios lo más amplios posibles mediante un hiperplano de separación definido como el vector entre los 2 puntos, de las 2 clases, más cercanos al que se llama vector soporte. Cuando las nuevas muestras se ponen en correspondencia con dicho modelo, en función de los espacios a los que pertenezcan, pueden ser clasificados a una o la otra clase.

Como en la mayoría de los métodos de clasificación supervisada, los datos de entrada son vistos como un vector p-dimensional.

En la literatura de las SVM, se llama atributo a la variable predictora y característica a un atributo transformado que es usado para definir el hiperplano. La elección de la representación más adecuada del universo estudiado se realiza mediante un proceso denominado selección de características. Al vector formado por los puntos más cercanos al hiperplano se le llama vector de soporte.

Los modelos basados en SVM están estrechamente relacionados con las redes neuronales. Usando una función kernel, resultan un método de formación alternativo para clasificadores polinomiales, funciones de base radial y perceptrón multicapa.

Parametros por default:
1.   C=1.0
2.   kernel='rbf'
3.   degree=3
4.   gamma='scale'
5.   coef0=0.0
6.   shrinking=True
7.   probability=False
8.   tol=0.001
9.   cache_size=200
10.   class_weight=None
11.   verbose=False
12.   max_iter=-1
13.   decision_function_shape='ovr'
14.   break_ties=False
15.   random_state=None
"""

# SVM con parámetros por defecto
svm_default = SVC(probability=True)
svm_default.fit(X_train, y_train)

# Predicciones
y_pred_svm_default = svm_default.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_svm_default)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_svm_default)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_svm_default)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - SVM Default')
plt.show()

#Configuracion del Pipeline para SVM
svm_pipeline = Pipeline([
    ('scaler', MinMaxScaler()), #Escalado de los datos para SVM
    ('svm', SVC(probability=True))
])

#Parametros a evaluar en la busqueda de cuadricula para SVM
param_grid_svm = {
    'svm__C': [0.1, 1, 10], #Valores del parametro de regularizacion C
    'svm__kernel': ['rbf', 'linear'], #Tipos de kernel a probar
    'svm__gamma': ['scale', 'auto'] #Coeficiente del kernel para 'rbf
}

#Busqueda de cuadricula con validacion cruzada
grid_search_svm = GridSearchCV(svm_pipeline, param_grid_svm, cv=5, scoring='neg_mean_squared_error')
grid_search_svm.fit(X_train, y_train)

#Mejores parametros y score obtenido
print("Mejores parametros para SVM: ", grid_search_svm.best_params_)

best_model = grid_search_svm.best_estimator_

# Predicciones
y_pred_svm_best = grid_search_svm.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_svm_best)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_svm_best)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_svm_best)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - SVM Best')
plt.show()

"""##Árboles de decision

Un árbol de decisión es un algoritmo de aprendizaje supervisado no paramétrico, que se utiliza tanto para tareas de clasificación como de regresión. Tiene una estructura de árbol jerárquica, que consta de un nodo raíz, ramas, nodos internos y nodos hoja.

En función de las características disponibles, ambos tipos de nodos realizan evaluaciones para formar subconjuntos homogéneos que se indican mediante nodos hoja o nodos terminales. Los nodos hoja representan todos los resultados posibles dentro del conjunto de datos.

El aprendizaje del árbol de decisiones emplea una estrategia de divide y vencerás mediante la realización de una búsqueda codiciosa para identificar los puntos de división óptimos dentro de un árbol. Este proceso de división se repite de forma recursiva de arriba hacia abajo hasta que todos o la mayoría de los registros se hayan clasificado bajo eriquetas de clase específicas.

Parametros por default:

1.   criterion='gini'
2.   splitter='best'
3.   max_depth=None
4.   min_samples_split=2
5.   min_samples_leaf=1
6.   min_weight_fraction_leaf=0.0
7.   max_features=None
8.   random_state=None
9.   max_leaf_nodes=None
10.   min_impurity_decrease=0.0
11.   class_weight=None
12.   ccp_alpha=0.0
13.   monotonic_cst=None
"""

# Arbol de decision con parámetros por defecto
dtc_default = DecisionTreeClassifier()
dtc_default.fit(X_train, y_train)

# Predicciones
y_pred_dtc_default = dtc_default.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_dtc_default)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_dtc_default)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_dtc_default)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - DTC Default')
plt.show()

from sklearn.tree import DecisionTreeClassifier

#Creamos y configuramos un pipeline con seleccion de caracteristicas, escalado
#y clasificacion

selector = SelectKBest()
scaler = MinMaxScaler()
clf = DecisionTreeClassifier(random_state=42)

dtc_pipeline = Pipeline([('selector', selector),
               ('escalador', scaler),
               ('clasificador', clf)])

#Definimos el diccionario param_grd que contiene las combinaciones de parametros
#que se probaran durante la busqueda de hiperparametros

param_grid_dtc = {
    "selector__k": [2], #Numero de caracteristicas
    "clasificador__criterion": ['gini', 'entropy'], #Criterio de division
    "clasificador__max_depth": [None, 2, 5, 7, 10], #Profundidad macima del arbol
    "clasificador__min_samples_split": [2, 5, 10], #Numero minimo de muestras para dividir un nodo
    "clasificador__min_samples_leaf": [1, 2, 4] #Numero mimimo de muestras por hoja
}

#Busqueda de cuadricula con validacion cruzada
grid_search_dtc = GridSearchCV(dtc_pipeline, param_grid_dtc, cv=5, scoring='neg_mean_squared_error')
grid_search_dtc.fit(X_train, y_train)

#Mejores parametros y score obtenido
print("Mejores parametros para DTC ", grid_search_dtc.best_params_)

best_model = grid_search_dtc.best_estimator_

#METRICAS

#Generamos las predicciones del modelo DTC
dtc_y_pred = grid_search_dtc.predict(X_test)


#Calculamos las metricas
mse = mean_squared_error(y_test, dtc_y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, dtc_y_pred)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, dtc_y_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - DTC Best')
plt.show()

"""##Random Forest

Es un algoritmo de machine learning de uso común registrado por Leo Breiman y Adele Cutler, que combina la salida de múltiples árboles de decisión para alcanzar un solo resultado. Su facilidad de uso y flexibilidad han impulsado su adopción, ya que maneja problemas de clasificación y regresión.

El algoritmo de bosque aleatorio es una extensión del método de ensacado, ya que utiliza tanto el ensacado como la aleatoriedad de características para crear un bosque no correlacionado de árboles de decisión.

Mientras que los árboles de decisión consideran todas las posibles divisiones de características, los bosques aleatorios solo seleccionan un subconjunto de esas características.

Parametros por default:



1.   n_estimators=100
2.   criterion='gini'
3.   max_depth=None
4.   min_samples_split=2
5.   min_samples_leaf=1
6.   min_weight_fraction_leaf=0.0
7.   max_features='sqrt'
8.   max_leaf_nodes=None
9.   min_impurity_decrease=0.0
10.   bootstrap=True
11.   oob_score=False
12.   n_jobs=None
13.   random_state=None
14.   verbose=0
15.   warm_start=False
16.   class_weight=None
17.   ccp_alpha=0.0
18.   max_samples=None
19.   monotonic_cst=None
"""

# Random Forest con parámetros por defecto
rfc_default = RandomForestClassifier()
rfc_default.fit(X_train, y_train)

# Predicciones
y_pred_rfc_default = rfc_default.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_rfc_default)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_rfc_default)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_rfc_default)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - RFC Default')
plt.show()

from sklearn.ensemble import RandomForestClassifier

#Creamos y configuramos un pipeline con seleccion de caracteristicas, escalado
#y clasificacion

selector = SelectKBest()
scaler = MinMaxScaler()
clf = RandomForestClassifier(random_state=42)

rfc_pipeline = Pipeline([('selector', selector),
               ('escalador', scaler),
               ('clasificador', clf)])

#Definimos el diccionario param_grd que contiene las combinaciones de parametros
#que se probaran durante la busqueda de hiperparametros

param_grid_rfc = {
    "selector__k": [2], #Numero de caracteristicas
    "clasificador__n_estimators": [50], #Numero de arboles en el bosque
    "clasificador__criterion": ['gini', 'entropy'], #Criterio de division
    "clasificador__max_depth": [None, 10, 20, 30, 40, 50], #Profundidad macima del arbol
    "clasificador__min_samples_split": [2, 5, 10], #Numero minimo de muestras para dividir un nodo
    "clasificador__min_samples_leaf": [1, 2, 4] #Numero mimimo de muestras por hoja
}

#Busqueda de cuadricula con validacion cruzada
grid_search_rfc = GridSearchCV(rfc_pipeline, param_grid_rfc, cv=5, scoring='neg_mean_squared_error')
grid_search_rfc.fit(X_train, y_train)

#Mejores parametros y score obtenido
print("Mejores parametros para RFC ", grid_search_rfc.best_params_)

best_model = grid_search_rfc.best_estimator_

# Predicciones
y_pred_rfc_best = grid_search_rfc.predict(X_test)

#Calculamos las metricas
mse = mean_squared_error(y_test, y_pred_rfc_best)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred_rfc_best)

print(f"Mean Squared Error: {mse:.3f}")
print(f"Root Mean Squared Error: {rmse:.3f}")
print(f"R^2 Score: {r2:.3f}")

# Visualización de la predicción vs realidad
plt.figure()
plt.scatter(y_test, y_pred_rfc_best)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted - RFC Best')
plt.show()

"""#Pero, ¿qué significa cada parámetro?

Los parámetros que se presentan a lo largo de esta notebook son diferentes de los que utilizamos para clasificación. Estos son utilizados para la predicción de la variable objetivo.

1. Mean Squared Error: En estadística, el error cuadrático medio (MSE) se define como la media o el promedio de las diferencias cuadradas entre los valores reales y estimados. El MSE mide la cantidad de error en un modelo estadístico. Si el modelo no tiene errores el MSE es cero, su valor aumenta a medida que aumenta el error del modelo.

2. Root Mean Squared Error: La raíz del error cuadrático medio (RMSE por sus siglas en inglés) es una medida de uso frecuente de las diferencias entre los valores predichos por un modelo y los valores observados. representa la raíz cuadrada de las diferencias cuadradas promedio entre los resultados predichos y observados. Es una métrica predominantemente utilizada en análisis de regresión y pronósticos donde la precisión importa significativamente. Cuanto menor sea el RMSE mejor será la capacidad de los modelos para predecir con precisión. Por el contrario un RMSE más alto significa una mayor discrepancia entre los resultados predichos y reales.

3. R^2 Score: Es una medida estadística que representa la bondad de ajuste de un modelo de regresión. El valor de R-cuadrado se encuentra entre 0 y 1. Obtenemos R-cuadrado igual a 1 cuando el modelo se ajusta perfectamente a los datos y no hay diferencia entre el valor predicho y el valor real. Por el otro lado, obtenemos R-cuadrado igual a 0 cuando el modelo no predice ninguna variabilidad en el modelo y no aprende ninguna relación entre las variables dependientes e independientes.

#Tabla de mejores modelos dado el valor de R^2
"""

#Definimos los modelos
models ={
    "Linear Regression": LinearRegression(),
    "Linear Regression Best": LinearRegression(copy_X=True, fit_intercept=True, positive=True),
    "SVM Default": SVC(probability=True),
    "SVM Best": SVC(C=10, gamma='auto', kernel='rbf'),
    "Decision Tree Default": DecisionTreeClassifier(),
    "Decision Tree Best": DecisionTreeClassifier(criterion='gini', max_depth=None, min_samples_leaf=5, min_samples_split=2),
    "Random Forest Default": RandomForestClassifier(),
    "Random Forest Best": RandomForestClassifier(criterion='gini', max_depth=10, min_samples_leaf=2, min_samples_split=10, n_estimators=50)
    }

#Entrenamos y evaluamos los modelos con parametros
metrics = []
for name, model in models.items():
  model.fit(X_train, y_train)
  y_pred = model.predict(X_test)

  mse = mean_squared_error(y_test, y_pred)
  rmse = np.sqrt(mse)
  r2 = r2_score(y_test, y_pred)

  metrics.append({
        "Model": name,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    })

#Convertimos las metricas en un DataFrame y ordenamos por True Positive
metrics_df = pd.DataFrame(metrics)
metrics_df = metrics_df.sort_values(by="RMSE", ascending=True)
print(metrics_df)

#Seleccionamos el mejor modelo
best_model_name = metrics_df.iloc[0]["Model"]
best_model = models[best_model_name]
print(f"Mejor modelo: {best_model_name}")

"""#Hacemos la prediccion

Tomaremos los siguientes parámetros del dataset para hacer la evaluación del modelo:

![image.png](data:image/png;base64,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)

![image.png](data:image/png;base64,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)
"""

X_new = pd.DataFrame([[6, 99]],
                     columns=["Hours Studied", "Previous Scores"])
y_new_pred = best_model.predict(X_new)
print(f"La calificacion minima que obtendra el alumno segun el modelo es: {y_new_pred}")

X_new = pd.DataFrame([[2, 61]],
                     columns=["Hours Studied", "Previous Scores"])
y_new_pred = best_model.predict(X_new)
print(f"La calificacion minima que obtendra el alumno segun el modelo es: {y_new_pred}")

"""Ahora haremos predicciones nuevas"""

X_new = pd.DataFrame([[7, 88]],
                     columns=["Hours Studied", "Previous Scores"])
y_new_pred = best_model.predict(X_new)
print(f"La calificacion minima que obtendra el alumno segun el modelo es: {y_new_pred}")

X_new = pd.DataFrame([[9, 75]],
                     columns=["Hours Studied", "Previous Scores"])
y_new_pred = best_model.predict(X_new)
print(f"La calificacion minima que obtendra el alumno segun el modelo es: {y_new_pred}")