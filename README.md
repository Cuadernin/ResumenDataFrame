# GUI for dataframe resume
<img align="left" src="https://github.com/Cuadernin/ResumenDataFrame/blob/master/images/imagen1.jpg" height="540" width="760"> 
<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
GUI designed in Python with PyQt5 that brings together different tools used in data analysis.
<br/>
It only allows .csv files but you can modify the code to read other files. 

## Start 🚀

Main program is called
```
Metodos.py
```
## Use 📦
The GUI is divided into two parts. 
* The first consists of a compilation of the graphs most used in exploratory analysis. In two of them, you must select a main variable. 
* The second part is about calculations and some data anaysis. You can find the data distribution by two ways and using [sweetviz](https://pypi.org/project/sweetviz/) you can see a dashboard in html format with all the summary about the dataframe. This package is widely used in data analysis.

## Methods 📌
In this case, three methods of machine learning are used:
* Random Forest ----->  For more info read about this method check [Random Forest](https://builtin.com/data-science/random-forest-algorithm)
* Ridge y Lasso ----->  For more info read about this method check *[Ridge](https://www.analyticsvidhya.com/blog/2016/01/ridge-lasso-regression-python-complete-tutorial/)
* kNN ----->  For more info read about this method check *[kNN](https://realpython.com/knn-python/)

In * you can find, in addition to the explanation of the method, a Python code as an example.

## Notes 📖
Finally, there is a group box called options where you can define the percentage of data to train in the model as well as define the name of the excel or txt according to the chosen output. 

If you choose a machine learning model, the output will be an excel file with three sheets and an extra one if you want it (Descriptive statistics). With linear regression a txt file is displayed because [statsmodel](https://www.statsmodels.org/stable/index.html) is used. 

The GUI is in **Spanish** and some codes have comments for your better understanding.

**By Cuadernin.**
