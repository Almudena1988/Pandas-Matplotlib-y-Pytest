from pathlib import Path

ruta = Path("../prueba.csv")
print(ruta.exists())

Path("datos.csv").exists()
Path("").mkdir()
Path("../prueba.csv").suffix
Path("../prueba.csv").name