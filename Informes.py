import pandas as pd
# Para analizar, manipular y limpiar datos en Python.
# Es una de las herramientas principales en análisis de datos, ciencia de datos y automatización de informes

import matplotlib.pyplot as plt
# matplotlib → la librería de gráficos
# pyplot → el módulo que permite crear gráficos fácilmente
#import datapane as dp # Para crear reportes interactivos (HTML o dashboards)
#import altair as alt # Convierte tablas de datos en visualizaciones interactivas
from pathlib import Path #importa la clase Path del módulo pathlib para trabajar con rutas de archivos y carpetas

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton, QVBoxLayout, QWidget, QMessageBox

fichero_csv = "prueba.csv" # Guardas el fichero en una variable
df = pd.read_csv(fichero_csv) # lee el archivo y lo guarda en la variable df
print(df.columns)  # Mostrar columnas
print(df)
# df["Mes"] -> selecciona columna mes
# df["Mes"] == "diciembre"
# df[df["Mes"] == "diciembre"] Filtra las filas para enseñar solo diciembre
df_mes = df[df["Mes"] == "Febrero"] #Cuando pides una columna se usa corchete
print (df_mes)
df_importe = df.groupby("Nombre")["Precio"].sum() #Nombre es el parametro de group by por eso va con paréntesis
print(df_importe)

IMG_BARRAS = Path("BARRAS.png") #Se define la ruta del archivo donde se guarda lo que se hace luego por código
IMG_PIE = Path("PIE.png") #Se define la ruta del archivo donde se guarda lo que se hace luego por código
HTML_FILE = Path("reporte.html") #Se define la ruta del archivo donde se guarda lo que se hace luego por código

################GRAFICOS

def generar_graficos(df, mes):
    datos = df[df["Mes"] == mes]
    if datos.empty:
        return False

    #GRÁFICO DE BARRAS:
    # 1 - Se crea una figura
    # 2 - Se eligen los datos
    # 3 - Se pone título
    # 4 - Se pone título al eje Y
    # 5.- Se establecen dimensiones con el layout
    # 6 - Se guarda

    plt.figure() # Para que cree la figura en una nueva ventana
    datos.groupby("Nombre")["Precio"].sum().plot(kind="bar") # Como eje x el nombre y como eje y el precio
    plt.title(f"Ventas en {mes}")
    plt.ylabel("Importe") #Lo que aparece en el eje Y
    plt.xlabel("Ventas") # Lo que aparece en el eje x
    plt.tight_layout() # Para que ajuste las dimensiones automáticamente según el gráfico
    plt.savefig(Path("BARRAS.png")) #Guardar la figura en la ruta definida arriba IMG_BARRAS = Path(BARRAS.PNG)

    #GRAFICO DE SECTORES
    plt.figure()
    datos.groupby("Nombre")["Precio"].sum().plot(kind="pie")
    plt.title("Unidades vendidas")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(Path("PIE.png")) #Guardar la figura en la ruta definida arriba IMG_PIE = Path("PIE.png")

def generar_html(df, mes):

    tabla_html = df[df["Mes"] == mes].to_html(index=False) #index=false para que no ponga índices
    generar_graficos(df, mes)
    html =f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>Informe de Ventas - {mes}</h1>
    <h3>Ventas por vendedor</h3>
    <img src="{IMG_BARRAS.name}">
    <h3>Detalle de ventas</h3>
    <img src="{IMG_PIE.name}">
    <h3>Tabla</h3>
    {tabla_html}
    </body>
    </html>
    """
    print(html)

    HTML_FILE.write_text(html, encoding="utf-8") #Guardar la figura en la ruta definida arriba
    # HTML_FILE = Path("reporte.html")

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.df = df

        self.setWindowTitle("Informe de ventas")
        self.resize(1200, 800)

        self.combo = QComboBox() # crea un cuadro desplegable (lista desplegable) en una interfaz gráfica
        self.combo.addItems(sorted(df["Mes"].unique())) #Unique para campos únicos
        self.btn = QPushButton("Actualizar informe")

        self.web = QWebEngineView() #Visualizar informes de tipo html dentro de una interfaz


        layout = QVBoxLayout()
        cont = QWidget()

        cont.setLayout(layout)
        self.setCentralWidget(cont)


        layout.addWidget(self.combo)
        layout.addWidget(self.btn)
        layout.addWidget(self.web)

        self.btn.clicked.connect(self.actualizar)
        self.actualizar()

    def actualizar(self):
        mes = self.combo.currentText()
        try:
            generar_html(self.df, mes)
            # cargar un archivo HTML local y mostrarlo en el visor web de la aplicación
            self.web.setUrl(QUrl.fromLocalFile(str(HTML_FILE.resolve())))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
   app = QApplication()
   ventana = Ventana()
   ventana.show()
   app.exec()