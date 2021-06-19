import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as ticker
import numpy as np
import math
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.dpi']="100"


#### Graficos ###


def corrgraf(data):
    corr_matrix=data.select_dtypes(include=['float64','int64']).corr(method='pearson')
    fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(7,7)) 
    sns.heatmap(corr_matrix,annot=True,cbar=False,annot_kws={"size":6},
        vmin=-1,vmax=1,
        center=0,cmap=sns.diverging_palette(240,10,n=200),
        square=True,ax=ax) #creamos un mapa de calor con parametros por default sugeridos por seaborn
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right',) #parametros por default extraidos de matplotlib
    ax.tick_params(labelsize=8)
        
def numericagraf(data):
    total=len(data.columns)
    if total%2==0:
        nrows=math.ceil(total/2)
        columnas=math.ceil(total/2-1)
    else:
        nrows=math.ceil(total/2)
        columnas=math.ceil(total-nrows)
    fig,axes=plt.subplots(nrows=nrows,ncols=columnas,figsize=(10,7)) #creamos multiples figuras para distintos graficos
    axes=axes.flat
    columnas_numeric=data.select_dtypes(include=['float64','int64']).columns
    for i,colum in enumerate(columnas_numeric): #iteracion con las columnas numericas
        sns.histplot(data=data,x=colum,stat="count",kde=True,
            color=(list(plt.rcParams['axes.prop_cycle'])*2)[i]["color"],
            line_kws={'linewidth':2},alpha=0.3,ax=axes[i]) #parametros por default extraidos de ejemplo de seaborn
        axes[i].set_title(colum,fontsize=7,fontweight="bold")
        axes[i].tick_params(labelsize=6)
        axes[i].set_xlabel("")
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle('Distribución de variables numéricas',fontsize=10,fontweight="bold");

def cualitativagraf(data):
    total=len(data.select_dtypes(include=['object']).columns)
    if total%2==0 and total>1:
        nrows=math.ceil(total/2)-1
        if nrows==0:
            nrows=1
        elif nrows==1:
            nrows=2
        columnas=nrows
    else:
        nrows=math.ceil(total/2)
        columnas=math.ceil(total/2)
    fig,axes=plt.subplots(nrows=nrows,ncols=columnas,figsize=(10,7))
    axes=axes.flat
    columnas_object=data.select_dtypes(include=['object']).columns
    for i,colum in enumerate(columnas_object):
        data[colum].value_counts().plot.barh(ax=axes[i])
        axes[i].set_title(colum,fontsize=7,fontweight="bold")
        axes[i].tick_params(labelsize=6)
        axes[i].set_xlabel("")
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle('Distribución de variables cualitativas',fontsize=10,fontweight="bold");
    
def correlacionesgraf(data,columna):
    total=len(data.select_dtypes(include=['float64','int64']).columns)
    if total%2==0:
        nrows=math.ceil(total/2)
    else:
        nrows=math.ceil(total/2)
        columnas=math.ceil(total-nrows)
    fig,axes=plt.subplots(nrows=nrows, ncols=nrows, figsize=(9, 5))
    axes=axes.flat
    columnas_numeric=data.select_dtypes(include=['float64','int64']).columns
    columnas_numeric=columnas_numeric.drop(columna) #eliminamos la columna de estudio

    for i,colum in enumerate(columnas_numeric):
        sns.regplot(x=data[colum],y=data[columna],
        color="gray",marker='.',scatter_kws={"alpha":0.4},
        line_kws={"color":"r","alpha":0.7},ax=axes[i])
        axes[i].set_title(f"{columna} vs {colum}",fontsize=7,fontweight="bold")
        #axes[i].ticklabel_format(style='sci', scilimits=(-4,4), axis='both')
        axes[i].yaxis.set_major_formatter(ticker.EngFormatter())
        axes[i].xaxis.set_major_formatter(ticker.EngFormatter())
        axes[i].tick_params(labelsize=6)
        axes[i].set_xlabel(columna)
        axes[i].set_ylabel("")  
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    fig.suptitle(f'Correlación con {columna}',fontsize=10,fontweight="bold");
    
def distr(df,columna):
    """
    Gráfico de dispersiones de la variable seleccionada vs las demas usando el metodo "pairplot" de seaborn
    """
    sns.set_theme(style="ticks")
    if columna==0:
        sns.pairplot(df)
    else:
        sns.pairplot(df, hue=columna)
