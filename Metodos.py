from PyQt5.QtWidgets import QFileDialog,QMessageBox,QApplication,QMainWindow
from PyQt5.QtCore import QAbstractTableModel
from PyQt5 import QtCore
from GuiPandas import DialogoP
from LecturaTablas import lectura
from Graficos import corrgraf,numericagraf,cualitativagraf,correlacionesgraf,distr
from DistribucionData import distribucion,distribucion_fitter
from LinearRegression import regresion
from PrediccionesConMetodos import ridge,knn,random_forest,stacking
import matplotlib.pyplot as plt
import pandas as pd
import webbrowser
import sweetviz as sv #libreria que genera un resumen de datagram en formato html
import sys
import warnings
warnings.filterwarnings('ignore')

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class panda(QMainWindow):
    def __init__(self): #constructor
        super(panda,self).__init__()
        QAbstractTableModel.__init__(self)
        self.ui=DialogoP()
        self.ui.setupUi(self)
        self.ui.abrir.triggered.connect(self.abrir)
        self.ui.acerca.triggered.connect(self.acerca)
        self.ui.btn_salir.clicked.connect(self.salir)     
        self.ui.btn_calcular.clicked.connect(self.calcular)
        self.ui.btn_graficar.clicked.connect(self.graficar)
        self.df=''
        self.valor=''
        self.show()
    
    def abrir(self): #funcion abrir
        archivo=QFileDialog.getOpenFileName(self,'Abrir archivo','C:\\','CSV UTF-8 (delimitado por comas) (*.csv)')
        if archivo[0]!='':
            try:
                self.df=pd.read_csv(archivo[0],encoding='latin-1')
                model=lectura(self.df)
                self.ui.tbv_1.setModel(model)
                self.ui.btn_graficar.setEnabled(True)
                self.ui.btn_calcular.setEnabled(True)
                self.activado_1()
                self.activado_2()
                self.activado_disp()
                self.ui.lbl_head.setText("A continuación una vista predeterminada de los datos: ")
            except Exception as e:
                mensaje=QMessageBox()
                mensaje.setWindowTitle("ALGO PASO...")
                mensaje.setIcon(QMessageBox.Information)
                mensaje.setText("Al parecer algo paso.") 
                mensaje.setDetailedText(str(e))
                mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
                mensaje.exec_() 
    
    ################# MENU #################            
    def acerca(self): 
        webbrowser.open('https://github.com/Cuadernin/ResumenDataFrame') 

    def salir(self):
        sys.exit(0)
    
    ################# GRAFICOS ################# 
    def correlaciones(self):
        try:
            seleccion=self.ui.combo_grafico.itemText(self.ui.combo_grafico.currentIndex())
            correlacionesgraf(self.df,seleccion)
        except Exception as e:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("ALGO PASO")
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText("No es posible graficarlo. Verifica el comportamiento de los datos.") 
            mensaje.setDetailedText(str(e))
            mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
            mensaje.exec_() 
        
    def cualitativas(self):
        try:
            cualitativagraf(self.df)
        except Exception as e:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("ALGO PASO")
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setText("No es posible graficarlo. Verifica el comportamiento de los datos.")
            mensaje.setDetailedText(str(e))
            mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
            mensaje.exec_() 
        
    def numericas(self):
        try:
            numericagraf(self.df)
        except Exception as e:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("ALGO PASO")
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setText("No es posible graficarlo. Verifica el comportamiento de los datos.")
            mensaje.setDetailedText(str(e))
            mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
            mensaje.exec_() 
        
    def matriz(self):
        try:
            corrgraf(self.df)
        except Exception as e:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("ALGO PASO")
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setText("No es posible graficarlo. Verifica el comportamiento de los datos.")
            mensaje.setDetailedText(str(e))
            mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
            mensaje.exec_() 
            
    def dispersiones(self):
        try:
            seleccion=self.ui.combo_grafico_dispersiones.itemText(self.ui.combo_grafico_dispersiones.currentIndex())
            if seleccion=='Todas':
                seleccion=0
            distr(self.df,seleccion) 
        except Exception as e:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("ALGO PASO")
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setText("No es posible graficarlo. Verifica el comportamiento de los datos.")
            mensaje.setDetailedText(str(e))
            mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
            mensaje.exec_() 
    
    ################# Lectura de columnas para introducirlas en el combo box #################     
    def activado_1(self):
        self.ui.combo_grafico.setEnabled(True)
        self.ui.combo_grafico.clear()
        lista=list((self.df.dtypes=="int64") | (self.df.dtypes=="float64"))
        nombres=[self.df.columns[i] for i in range(len(lista)) if lista[i]==True]
        self.ui.combo_grafico.addItems(nombres)     
        
    def activado_2(self):
        self.ui.combo_variable.setEnabled(True)
        self.ui.combo_variable.clear()
        lista=list((self.df.dtypes=="int64") | (self.df.dtypes=="float64"))
        nombres=[]
        nombres=[self.df.columns[i] for i in range(len(lista)) if lista[i]==True]
        self.ui.combo_variable.addItems(nombres)         
        
    def activado_disp(self):
        self.ui.combo_grafico_dispersiones.setEnabled(True)
        self.ui.combo_grafico_dispersiones.clear()
        names=[]
        names.append('Todas')
        for i in range(len(self.df.columns)):
            names.append(self.df.columns[i])
        self.ui.combo_grafico_dispersiones.addItems(names)
    
    ################# Lectura de graficos seleccionados ################# 
    def graficar(self):
        if self.ui.cbx_matriz.isChecked():
            self.matriz()
        if self.ui.cbx_cualitativas.isChecked():
            self.cualitativas()
        if self.ui.cbx_numericas.isChecked():
            self.numericas()
        if self.ui.cbx_correlaciones.isChecked():
            self.correlaciones()
        if self.ui.cbx_dispersiones.isChecked():
            self.dispersiones()
        plt.ion()
        plt.show()

    ################# Lectura de calculos seleccionados ################# 
    def calcular(self):
        if self.ui.cbx_distribucion_kstest.isChecked():
            lista=list((self.df.dtypes=="int64") | (self.df.dtypes=="float64"))
            nombres=[self.df.columns[i] for i in range(len(lista)) if lista[i]==True]
            valores,valores2=[],[]
            for ele in nombres:
                valores.append(distribucion(self.df[ele],ele))
            df2=pd.DataFrame(valores,columns=["columna","prediccion","valor p","parametros"])
            self.valor=1
            with pd.ExcelWriter("DistribucionDatos.xlsx") as writer:
                df2.to_excel(excel_writer=writer,sheet_name="Usando Ktest",header=True)
        
        if self.ui.cbx_distribucion_teorica.isChecked():
            df=distribucion_fitter(self.df)
            self.valor=1
            with pd.ExcelWriter("DistribucionesDatos.xlsx") as writer:
                df.to_excel(excel_writer=writer,sheet_name="Fitter",header=True,index=True)
                
        if self.ui.cbx_pandas.isChecked():
            my_report=sv.analyze(self.df)
            my_report.show_html(filepath='pandas_resumen.html',open_browser=True,layout='widescreen')
            self.valor=1
        
        if self.ui.cbx_descriptivas.isChecked():
            describe=1
        else:
            describe=0
    
        if self.ui.rbt_regresion.isChecked():
            seleccion=self.ui.combo_variable.itemText(self.ui.combo_variable.currentIndex())
            if len(self.ui.txt_texto.text())>0:
                nombre=self.ui.txt_texto.text()
                if '.txt' in nombre:
                    regresion(self.df,seleccion,nombre)
                    self.valor=1
                else:
                    mensaje=QMessageBox()
                    mensaje.setWindowTitle("Al parecer te falto algo...")
                    mensaje.setIcon(QMessageBox.Warning)
                    mensaje.setText("El nombre del archivo debe tener la extensión .txt") 
                    mensaje.exec_()
            else:
                mensaje=QMessageBox()
                mensaje.setWindowTitle("Error de nombre")
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setText("Debe escribir un nombre para el archivo txt.") 
                mensaje.exec_() 
        
        if self.ui.rbt_ridge.isChecked():
            seleccion=self.ui.combo_variable.itemText(self.ui.combo_variable.currentIndex())
            if len(self.ui.txt_excel.text())>0 and len(self.ui.txt_test.text())>0:
                nombre=self.ui.txt_excel.text()
                if '.xlsx' in nombre:
                    try: 
                        test=float(self.ui.txt_test.text())
                        ridge(self.df,seleccion,nombre,describe,test)
                        self.valor=1  
                    except Exception as e:
                        mensaje=QMessageBox()
                        mensaje.setWindowTitle("ALGO PASO")
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setText("test_size es el porcentaje de datos que se van a usar para entrenar el modelo. Debe ser un dato número entre (0,80].") 
                        mensaje.setDetailedText(str(e))
                        mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
                        mensaje.exec_()   
                else:
                    mensaje=QMessageBox()
                    mensaje.setWindowTitle("Al parecer te falto algo...")
                    mensaje.setIcon(QMessageBox.Warning)
                    mensaje.setText("El nombre del archivo debe tener la extensión .xlsx") 
                    mensaje.exec_()
                    
            else:
                mensaje=QMessageBox()
                mensaje.setWindowTitle("Error de nombre")
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setText("Debes rellenar los campos.") 
                mensaje.exec_()
                
        if self.ui.rbt_forest.isChecked():
            seleccion=self.ui.combo_variable.itemText(self.ui.combo_variable.currentIndex())
            if len(self.ui.txt_excel.text())>0 and len(self.ui.txt_test.text())>0:
                nombre=self.ui.txt_excel.text()
                if '.xlsx' in nombre:    
                    try:
                        test=float(self.ui.txt_test.text())
                        random_forest(self.df,seleccion,nombre,describe,test)
                        self.valor=1 
                    except Exception as e:
                        mensaje=QMessageBox()
                        mensaje.setWindowTitle("ALGO PASO")
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setText("test_size es el porcentaje de datos que se van a usar para entrenar el modelo. Debe ser un dato número entre (0,80].") 
                        mensaje.setDetailedText(str(e))
                        mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
                        mensaje.exec_()   
                else:
                    mensaje=QMessageBox()
                    mensaje.setWindowTitle("Al parecer te falto algo...")
                    mensaje.setIcon(QMessageBox.Warning)
                    mensaje.setText("El nombre del archivo debe tener la extensión .xlsx") 
                    mensaje.exec_()
            else:
                mensaje=QMessageBox()
                mensaje.setWindowTitle("Error de nombre")
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setText("Debes rellenar los campos.") 
                mensaje.exec_()
                
        if self.ui.rbt_knn.isChecked():
            seleccion=self.ui.combo_variable.itemText(self.ui.combo_variable.currentIndex())
            if len(self.ui.txt_excel.text())>0 and len(self.ui.txt_test.text())>0:
                nombre=self.ui.txt_excel.text()
                if '.xlsx' in nombre:
                    try:
                        test=float(self.ui.txt_test.text())
                        knn(self.df,seleccion,nombre,describe,test)
                        self.valor=1  
                    except Exception as e:
                        mensaje=QMessageBox()
                        mensaje.setWindowTitle("ALGO PASO")
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setText("test_size es el porcentaje de datos que se van a usar para entrenar el modelo. Debe ser un dato número entre (0,80].") 
                        mensaje.setDetailedText(str(e))
                        mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) 
                        mensaje.exec_()   
                else:
                    mensaje=QMessageBox()
                    mensaje.setWindowTitle("Al parecer te falto algo...")
                    mensaje.setIcon(QMessageBox.Warning)
                    mensaje.setText("El nombre del archivo debe tener la extensión .xlsx") 
                    mensaje.exec_()
            else:
                mensaje=QMessageBox()
                mensaje.setWindowTitle("Error de nombre")
                mensaje.setIcon(QMessageBox.Warning)
                mensaje.setText("Debes rellenar los campos.") 
                mensaje.exec_()
        if self.valor==1:
            mensaje=QMessageBox()
            mensaje.setWindowTitle("EXITO")
            mensaje.setIcon(QMessageBox.Information)
            mensaje.setText("Busca en la carpeta el archivo correspondiente para visualizar los resultados.") 
            mensaje.exec_()  
        

# bloque principal
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ventana=panda()
    ventana.show()
    sys.exit(app.exec_())
    