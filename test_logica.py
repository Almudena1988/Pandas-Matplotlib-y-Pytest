import pytest  #ejecuta pruebas (tests) que verifican si las funciones dan el resultado esperado
from logica import cargar_csv, estado_alumno, media_por_asignatura


@pytest.fixture # Prepara algo que los test necesitan antes de ejecutarse
def csv_temporal(tmp_path):
    archivo = tmp_path / "datos.csv"
    archivo.write_text(
        "Alumno,Asignatura,Nota\n"
        "Ana,Programacion,8\n"
        "Ana,Base de datos,7\n"
        "Luis,Programacion,4\n"
        "Luis,Base de datos,3\n"
    )
    return archivo

def test_cargar_csv(csv_temporal):
    df = cargar_csv(csv_temporal)
    assert len(df) == 4 # Comprueba que la longitud del csv sea 4 filas

def test_estado_aprobado():
    assert estado_alumno(7) == "Aprobado"

def test_estado_suspenso():
    assert estado_alumno(2) == "Suspenso"

def test_media_asignatura(csv_temporal):
    df = cargar_csv(csv_temporal)
    media = media_por_asignatura(df, "Programacion")
    assert media == 6
# Se escribe: pytest -v en la terminal para hacer las pruebas juntas