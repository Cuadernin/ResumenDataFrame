from sklearn.model_selection import RandomizedSearchCV,RepeatedKFold,train_test_split
from sklearn.ensemble import RandomForestRegressor,StackingRegressor
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.linear_model import Ridge,RidgeCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_percentage_error,r2_score
from sklearn import preprocessing,utils
import multiprocessing
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
def ridge(df,valor,url,describe,test):
    """
    - El modelo consiste en la creación de un pipeline que contega Preprocesado + modelo.
    - Después iniciamos con la optimización de hiperparámetros.
    - Finalmente obtenemos las predicciones.
    """
    lista=list(df.dtypes=="object")
    nombres=[df.columns[i] for i in range(len(lista)) if lista[i]==True]
    X=df.drop(nombres,axis=1)
    Y=df[valor]
    df_describe=X.describe(include="all")
    X=X.drop(valor,axis='columns')
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=test,random_state=42,shuffle=True) #entrenamiento
    #Identificamos las columnas numéricas y catégoricas
    numeric_cols=X_train.select_dtypes(include=['float64','int']).columns.to_list()
    cat_cols=X_train.select_dtypes(include=['object','category']).columns.to_list()
    
    numeric_transformer=Pipeline(steps=[('scaler',StandardScaler())]) #Definimos cómo queremos transformar las variables numéricas usando el metodo de estandarización
    categorical_transformer=Pipeline(steps=[('onehot',#Definimos cómo queremos transformar las variables categóricas para poder usarlas en el modelo
    OneHotEncoder(handle_unknown="ignore"))]) 
    preprocessor=ColumnTransformer(transformers=[('numeric',numeric_transformer, numeric_cols),('cat', categorical_transformer, cat_cols)],
    remainder='passthrough') #Comienza la transformacion anterior
    
    pipe=Pipeline([('preprocessing',preprocessor),('modelo',Ridge())]) #Combinamos el preprocesado y el modelo en un mismo pipeline
    param_distributions={'modelo__alpha':np.logspace(-5,5,500)} #Conjunto de busqueda de cada hiperpárametro
    grid=RandomizedSearchCV(estimator=pipe,param_distributions=param_distributions, #En este caso usamos la busqueda random grid con algunos parametros default y otros modificados
    n_iter=20,scoring='neg_root_mean_squared_error',        #Usando como validación cruzada RepeatedKFold 
    n_jobs=multiprocessing.cpu_count(),cv=RepeatedKFold(n_splits=5,n_repeats=3), 
    refit=True,verbose= 0,random_state=123,return_train_score=True)

    grid.fit(X=X_train,y=y_train) #ajustamos
    #Iniciamos con las predicciones
    resultados=pd.DataFrame(grid.cv_results_)
    modelo_final=grid.best_estimator_
    predicciones=modelo_final.predict(X_test)
    dic={valor:y_test,'prediccion':predicciones}
    df_predicciones=pd.DataFrame(dic)
    
    #Acomodamos los resultados y los datos a pegar en el excel
    rmse=mean_squared_error(y_true=y_test,y_pred=predicciones,squared=False)
    score=modelo_final.score(X,Y)
    r2=r2_score(y_true=y_test,y_pred=predicciones)
    mae=mean_absolute_percentage_error(y_true=y_test,y_pred=predicciones)
    met={"RMSE":rmse,'Score':score,"r2_score":r2,"MAE":mae}
    df_metricas=pd.DataFrame(met,index=[0])
    print(predicciones)
    with pd.ExcelWriter(url) as writer:
        df_predicciones.to_excel(excel_writer=writer,sheet_name="Predicciones",header=True)
        resultados.to_excel(excel_writer=writer,sheet_name="Resultados",header=True)
        df_metricas.to_excel(excel_writer=writer,sheet_name="Metricas",header=True)
        if describe==1:
            df_describe.to_excel(excel_writer=writer,sheet_name="Estadisticas descriptivas",header=True)

def random_forest(df,valor,url,describe,test):
    """
    - El modelo consiste en la creación de un pipeline que contega Preprocesado + modelo.
    - Después iniciamos con la optimización de hiperparámetros.
    - Finalmente obtenemos las predicciones.
    """
    lista=list(df.dtypes=="object")
    nombres=[df.columns[i] for i in range(len(lista)) if lista[i]==True]
    X=df.drop(nombres,axis=1)
    df_describe=X.describe(include="all")
    Y=df[valor]
    X=X.drop(valor,axis='columns')
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=test,random_state=42,shuffle=True)
    #Identificamos las columnas numéricas y catégoricas
    numeric_cols=X_train.select_dtypes(include=['float64','int']).columns.to_list()
    cat_cols=X_train.select_dtypes(include=['object','category']).columns.to_list()
    
    numeric_transformer=Pipeline(steps=[('scaler',StandardScaler())]) #Definimos cómo queremos transformar las variables numéricas usando el metodo de estandarización
    # Transformaciones para las variables categóricas
    categorical_transformer=Pipeline(steps=[('onehot', #Definimos cómo queremos transformar las variables categóricas para poder usarlas en el modelo
            OneHotEncoder(handle_unknown='ignore'))])
    preprocessor=ColumnTransformer(transformers=[('numeric',numeric_transformer,numeric_cols),
    ('cat',categorical_transformer,cat_cols)],remainder='passthrough')
    
    pipe=Pipeline([('preprocessing', preprocessor),('modelo',RandomForestRegressor())]) #Se combinan los pasos de preprocesado y el modelo en un mismo pipeline.
    
    #Optimización de hiperparámetros
    param_distributions={'modelo__n_estimators':[25,50,500,1000],
    'modelo__max_features':["auto",3,5,7],'modelo__max_depth':[None, 3, 5, 10, 20]} #Espacio de búsqueda de cada hiperparámetro (recomendado por sklearn)
    grid=RandomizedSearchCV(estimator=pipe,param_distributions=param_distributions, # Búsqueda random grid
            n_iter=15,scoring='neg_root_mean_squared_error',
            n_jobs=multiprocessing.cpu_count(),
            cv=RepeatedKFold(n_splits=5,n_repeats=3),
            refit=True,verbose=0,random_state=123,return_train_score=True)
    grid.fit(X=X_train,y=y_train)
    
    #predicciones
    resultados=pd.DataFrame(grid.cv_results_)
    modelo_final=grid.best_estimator_
    predicciones=modelo_final.predict(X=X_test)
    dic={valor:y_test,'prediccion':predicciones}
    df_predicciones=pd.DataFrame(dic)
    
    rmse=mean_squared_error(y_true=y_test,y_pred=predicciones,squared=False)
    score=modelo_final.score(X,Y)
    r2=r2_score(y_true=y_test,y_pred=predicciones)
    mae=mean_absolute_percentage_error(y_true=y_test,y_pred=predicciones)
    met={"RMSE":rmse,'Score':score,"r2_score":r2,"MAE":mae}
    df_metricas=pd.DataFrame(met,index=[0])
    
    url='random_forest.xlsx'
    with pd.ExcelWriter(url) as writer: #Guardamos toda la información importante en un mismo excel
        df_predicciones.to_excel(excel_writer=writer,sheet_name="Predicciones",header=True)
        resultados.to_excel(excel_writer=writer,sheet_name="Resultados",header=True)
        df_metricas.to_excel(excel_writer=writer,sheet_name="Metricas",header=True)
        df_describe.to_excel(excel_writer=writer,sheet_name="Estadisticas descriptivas",header=True)
        if describe==1:
            df_describe.to_excel(excel_writer=writer,sheet_name="Estadisticas descriptivas",header=True)

def knn(df,valor,url,describe,test):
    """
    - El modelo consiste en la creación de un pipeline que contega Preprocesado + modelo.
    - Después iniciamos con la optimización de hiperparámetros.
    - Finalmente obtenemos las predicciones.
    """
    lista=list(df.dtypes=="object")
    nombres=[df.columns[i] for i in range(len(lista)) if lista[i]==True]
    X=df.drop(nombres,axis=1)
    df_describe=X.describe(include="all")
    Y=df[valor]
    X=X.drop(valor,axis='columns')
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=test, random_state=42)

    numeric_cols=X_train.select_dtypes(include=['float64','int']).columns.to_list()
    cat_cols=X_train.select_dtypes(include=['object','category']).columns.to_list()
    
    numeric_transformer=Pipeline(steps=[('scaler',StandardScaler())])
    
    categorical_transformer=Pipeline(steps=[('onehot',OneHotEncoder(handle_unknown='ignore'))])
    preprocessor=ColumnTransformer(transformers=[('numeric',numeric_transformer, numeric_cols),
    ('cat',categorical_transformer,cat_cols)],remainder='passthrough')
    
    pipe=Pipeline([('preprocessing',preprocessor),('modelo',KNeighborsRegressor())])

    param_distributions={'modelo__n_neighbors':np.linspace(1,100,500,dtype=int)}
    
    grid=RandomizedSearchCV(estimator=pipe, 
            param_distributions=param_distributions,n_iter=20,
            scoring='neg_root_mean_squared_error',
            n_jobs=multiprocessing.cpu_count(),
            cv=RepeatedKFold(n_splits=5,n_repeats=3), 
            refit=True,verbose=0,random_state=123,return_train_score=True)
    grid.fit(X=X_train,y=y_train)

    resultados=pd.DataFrame(grid.cv_results_)
    modelo_final=grid.best_estimator_
    predicciones=modelo_final.predict(X=X_test)
    dic={valor:y_test,'prediccion':predicciones}
    df_predicciones=pd.DataFrame(dic)
    
    rmse=mean_squared_error(y_true=y_test,y_pred=predicciones,squared=False)
    score=modelo_final.score(X,Y)
    r2=r2_score(y_true=y_test,y_pred=predicciones)
    mae=mean_absolute_percentage_error(y_true=y_test,y_pred=predicciones)
    met={"RMSE":rmse,'Score':score,"r2_score":r2,"MAE":mae}
    df_metricas=pd.DataFrame(met,index=[0])
    
    with pd.ExcelWriter(url) as writer:
        df_predicciones.to_excel(excel_writer=writer,sheet_name="Predicciones",header=True)
        resultados.to_excel(excel_writer=writer,sheet_name="Resultados",header=True)
        df_metricas.to_excel(excel_writer=writer,sheet_name="Metricas",header=True)
        if describe==1:
            df_describe.to_excel(excel_writer=writer,sheet_name="Estadisticas descriptivas",header=True)
