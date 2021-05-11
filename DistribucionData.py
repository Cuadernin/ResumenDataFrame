import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import multiprocessing
from fitter import Fitter
warnings.filterwarnings('ignore')
def distribucion(data,ele):
    """
    Se elige la prueba de Kolmogorov-Smirnov ya que al ser "no parametrica" se adapta a
    los datos con el fin de no suponer que el conjunto sigue una determinada distribución y 
    así determinar si dos muestras (obviamente cuanto más grandes mucho mejor) tienen la misma 
    distribución de datos.
    
    Contraste de hipótesis:
        H_0: El conjunto de dato sigue la misma distribución
        H_a: El conjunto de datos tiene una diferente distribución
    
    Tomando un nivel de significancia del 5%, es decir, alpha=0.05 (intervalo de confianza del 95%)
    y usando el valor p, la hipótesis se ve como:
        H_0: P>0.05  ------------------> Aceptamos H_0 y podemos concluir (con un 95% de prob. ) que sigue la misma distribución
        H_a: P<=0.05 ------------------> Rechazamos H_0 
    
    En nuestro caso, usaremos el valor p más grande para determinar cuál de todas las distribuciones se adapta mejor a 
    los datos.
    """
    distr=["norm", "exponweib", "weibull_max", "weibull_min", "pareto", "uniform","t","expon",
    "lognorm","beta","alpha","cauchy","f","loguniform","chi2","laplace","gamma"]
    resultados,parametros=[],{}
    for dist_name in distr:
        dist=getattr(st, dist_name) #extraemos los atributos de cada distribucion almacenados en la libreria scipy
        parametro=dist.fit(data) #ajustamos los datos
        parametros[dist_name]=parametro #igualamos los parametros de cada distribucion a la variable ----> parametro
        estadistico,p_valor=st.kstest(data,dist_name,args=parametro)# Aplicamos la prueba de Kolmogorov-Smirnov 
        resultados.append([dist_name,p_valor])

    dist_escogida,p_value=(max(resultados,key=lambda item:item[1])) #se extrae la distribucion con el valor p mas grande
    return ele,dist_escogida,p_value,parametros[dist_escogida]

def distribucion_fitter(data):
    """
    Esta libreria funciona para determinar la distribucion de grupo de datos. Ajusta los datos a cada una de las distribuciones y realiza las prueba pertinentes
    """
    distr=["norm", "exponweib", "weibull_max", "weibull_min", "pareto", "uniform","t","expon",
    "lognorm","beta","alpha","cauchy","f","loguniform","chi2","laplace","gamma"]
    lista=list((data.dtypes=="int64") | (data.dtypes=="float64"))
    nombres=[data.columns[i] for i in range(len(lista)) if lista[i]==True] #almacenamos el nombre de todas las columnas cuyos valores sean numericos
    dfs,parametros,best_f=[],[],[]
    for ele in nombres:
        fitter=Fitter(data[ele],distributions=distr) #metodo principal
        fitter.fit(n_jobs=multiprocessing.cpu_count()) #Hacemos que use todos los nucleos del procesador
        p=fitter.summary(Nbest=1,plot=False) #aqui se almacen todos los resultados de la prueba
        parametros.append(fitter.get_best(method='sumsquare_error'))
        dfs.append(p) #agregamos los dataframes a una lista y ahora tenemos una lista de dataframes
    full=pd.concat(dfs,ignore_index=False) #agregamos todos los dataframes
    full.insert(0,"Columna",nombres) 
    full.insert(2,'parametros',parametros) #insertamos la columna en cuestion con los parametros de la mejor distribucion
    return full
