import pandas as pd


def cargar_csv(ruta):
    df = pd.read_csv(ruta)
    df.columns = df.columns.str.strip()

    return df

def estado_alumno(media):
    return "Aprobado" if media >=5 else "Suspenso"

def calcular_media_por_alumno(df):
    medias = df.groupby("Alumno")["Nota"].mean().reset_index() # mean para calcular la media
    medias["Estado"] = medias["Nota"].apply(estado_alumno)
    return medias

def media_por_asignatura(df, asignatura):
    datos = df[df["Asignatura"] == asignatura]
    return datos["Nota"].mean()
