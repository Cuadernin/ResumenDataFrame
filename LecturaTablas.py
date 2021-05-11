from PyQt5.QtCore import QAbstractTableModel, Qt
class lectura(QAbstractTableModel):
    def __init__(self,data):
        QAbstractTableModel.__init__(self)
        self._data=data

    def rowCount(self,parent=None): #QAbstractTableModel.rowCount()
        return self._data.shape[0] #Lee el total de filas

    def columnCount(self,parnet=None): #QAbstractTableModel.columnCount() 
        return self._data.shape[1] #Lee el total decolumnas

    def data(self,index,role=Qt.DisplayRole): #funcion que acomoda las filas con su respectiva columna
        if index.isValid():
            if role==Qt.DisplayRole:
                return str(self._data.iloc[index.row(),index.column()])
        return None

    def headerData(self,col,orientation,role):   #funcion que extrae el nombre de las columnas
        if orientation==Qt.Horizontal and role==Qt.DisplayRole:
            return self._data.columns[col]
        return None