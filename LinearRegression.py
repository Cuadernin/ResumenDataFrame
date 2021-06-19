import pandas as pd
pd.set_option("display.width",100)
import matplotlib.pyplot as plt
import statsmodels.api as sm
import warnings
import numpy as np
warnings.filterwarnings('ignore')

## Regresion lineal usando la libreria statsmodels

def regresion(df,col,nombre):
    lista=list(df.dtypes=="object")
    nombres=[df.columns[i] for i in range(len(lista)) if lista[i]==True] #lista de columnas con valores de tipo string
    df=df.drop(nombres,axis="columns") #eliminamos estas columnas pues no las necesitamos
    df=sm.add_constant(df) #agregamos una constante al modelo
    reg=sm.OLS(df[col],df).fit() #llamamos al metodo OLS (metodo que hace la regresion) y ajustamos los daots
    with open(nombre,"a+") as f:
        f.write(str(reg.summary())) #escribimos el summary en un archivo de texto
