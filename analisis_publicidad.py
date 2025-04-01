import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Función para cargar datos
def cargar_datos(archivo_csv):
    df = pd.read_csv(archivo_csv)
    promedios_por_periodo_red = (
        df
        .groupby(['Periodo', 'Red de alcance'])['Cantidad']
        .mean()
        .reset_index()
    )
    promedios_por_periodo_red.columns = ['Periodo', 'Red de Alcance', 'Promedio Alcance']
    return promedios_por_periodo_red

# Función para ordenar periodos
def ordenar_periodos(df, orden_periodos):
    df['Periodo'] = pd.Categorical(
        df['Periodo'],
        categories=orden_periodos,
        ordered=True
    )
    return df.sort_values(by='Periodo')

# Función para calcular porcentaje de aumento
def calcular_porcentaje_aumento(df):
    pre_publicidad = df[df['Periodo'] == 'Pre-Publicidad']
    durante_publicidad = df[df['Periodo'] == 'Durante Publicidad']
    comparacion = pd.merge(
        pre_publicidad,
        durante_publicidad,
        on='Red de Alcance',
        suffixes=('_Pre', '_Durante')
    )
    comparacion['Porcentaje Aumento (%)'] = (
        (comparacion['Promedio Alcance_Durante'] - comparacion['Promedio Alcance_Pre']) /
        comparacion['Promedio Alcance_Pre']
    ) * 100
    return comparacion

# Función para graficar barras
def graficar_barras(df, comparacion, orden_periodos):
    periodos = df['Periodo'].unique()
    redes = df['Red de Alcance'].unique()
    x = np.arange(len(periodos))  # Posiciones en el eje X para los periodos
    width = 0.25  # Ancho de las barras

    plt.figure(figsize=(12, 6))

    for i, red in enumerate(redes):
        subset = df[df['Red de Alcance'] == red]
        bars = plt.bar(
            x + i * width,  # Desplazamiento en el eje X
            subset['Promedio Alcance'],
            width=width,
            label=red
        )

        # Agregar porcentajes encima de las barras para el periodo "Durante Publicidad"
        for bar, periodo in zip(bars, subset['Periodo']):
            if periodo == 'Durante Publicidad':
                porcentaje_aumento = comparacion.loc[
                    comparacion['Red de Alcance'] == red, 'Porcentaje Aumento (%)'
                ].values[0]
                plt.text(
                    bar.get_x() + bar.get_width() / 2,  # Posición horizontal
                    bar.get_height(),  # Posición vertical
                    f"{porcentaje_aumento:.1f}%",  # Texto con porcentaje
                    ha='center', va='bottom', fontsize=10, color='black'
                )

    plt.title('Promedio de Alcance por Periodo y Red', fontsize=16)
    plt.xlabel('Periodo', fontsize=12)
    plt.ylabel('Promedio Alcance', fontsize=12)
    plt.xticks(x + width * (len(redes) - 1) / 2, orden_periodos)  # Centrar etiquetas en las agrupaciones
    plt.legend(title='Red de Alcance')
    plt.tight_layout()
    st.pyplot(plt)  # Mostrar gráfica en Streamlit
