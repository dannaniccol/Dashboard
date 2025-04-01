import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def dashboard_objetivo_4():
    # Dividir la página en tres columnas
    col1, col2, col3 = st.columns(3)

    # KPI 1: Tiempo promedio de permanencia por fuente
    with col1:
        st.subheader("KPI 1: Tiempo promedio de permanencia por fuente")

        # Ruta del archivo CSV
        file_path = 'files/Copy of tecnoglass - Informe de tráfico_2023-11-13-2.csv'

        try:
            # Cargar el archivo CSV
            data = pd.read_csv(file_path)

            # Verificar las columnas necesarias
            required_columns = ['fuente de trafico', 'duracion prom. de la sesion en segundos', 'sesiones del sitio']
            if all(column in data.columns for column in required_columns):
                # Convertir columnas relevantes a numéricas
                data['duracion prom. de la sesion en segundos'] = pd.to_numeric(
                    data['duracion prom. de la sesion en segundos'], errors='coerce')
                data['sesiones del sitio'] = pd.to_numeric(data['sesiones del sitio'], errors='coerce')

                # Agrupar por fuente de tráfico y calcular métricas
                kpi_data = data.groupby('fuente de trafico').agg({
                    'duracion prom. de la sesion en segundos': 'sum',
                    'sesiones del sitio': 'sum'
                }).rename(columns={
                    'duracion prom. de la sesion en segundos': 'tiempo_total',
                    'sesiones del sitio': 'numero_usuarios'
                })

                # Calcular el tiempo promedio de permanencia por fuente
                kpi_data['tiempo_promedio'] = kpi_data['tiempo_total'] / kpi_data['numero_usuarios']

                # Mostrar la fórmula utilizada
                st.markdown("""
                  **Fórmula utilizada:**  
                  Tiempo promedio de permanencia por fuente = Tiempo total de permanencia desde una fuente / Número total de usuarios de esa fuente
                  """)

                # Agrupar categorías pequeñas en "Otros"
                threshold = 5  # Porcentaje mínimo para no agrupar
                kpi_data['porcentaje'] = (kpi_data['tiempo_total'] / kpi_data['tiempo_total'].sum()) * 100
                kpi_data['categoria_agrupada'] = kpi_data.index.where(kpi_data['porcentaje'] > threshold, 'Otros')

                # Recalcular los datos para la gráfica
                grouped_data = kpi_data.groupby('categoria_agrupada').sum()

                # Crear la gráfica de pastel
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                ax1.pie(
                    grouped_data['tiempo_total'],
                    labels=grouped_data.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=plt.cm.Paired.colors
                )
                ax1.axis('equal')  # Asegurar que el pastel sea un círculo
                st.pyplot(fig1)

                # Mostrar los datos calculados (tabla)
                st.subheader("Tabla de Datos Calculados")
                st.dataframe(kpi_data)

                # Explicación de las variables
                st.subheader("Explicación de las Variables")
                st.table(pd.DataFrame({
                    "Variable": ["Tiempo total", "Número de usuarios", "Tiempo promedio"],
                    "Descripción": [
                        "Suma de todo el tiempo que los usuarios estuvieron en el sitio desde una fuente.",
                        "Número total de personas que llegaron desde esa fuente.",
                        "Promedio del tiempo que cada usuario pasó en el sitio desde esa fuente en segundos."
                    ]
                }))

                # Interpretaciones de resultados
                st.subheader("Interpretaciones de los Resultados")
                st.table(pd.DataFrame({
                    "Resultado": ["> 100 segundos", "< 30 segundos", "Entre 30 y 100 segundos"],
                    "Interpretación": [
                        "Los usuarios pasan mucho tiempo aquí, lo que indica contenido interesante.",
                        "Los usuarios pasan poco tiempo, tal vez no encuentran lo que buscan.",
                        "El tiempo promedio es bueno, los usuarios están interesados."
                    ]
                }))
            else:
                st.error("El archivo no contiene las columnas necesarias. Por favor, verifica los datos.")
        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")

    # KPI 2: Tasa de tráfico por fuente
    with col2:
        st.subheader("KPI 2: Tasa de tráfico por fuente")

        try:
            # Verificar las columnas necesarias
            columnas_requeridas = ['fuente de trafico', 'sesiones del sitio']
            if all(column in data.columns for column in columnas_requeridas):
                # Convertir las sesiones a numéricas
                data['sesiones del sitio'] = pd.to_numeric(data['sesiones del sitio'], errors='coerce')

                # Calcular el total de visitas
                total_visitas = data['sesiones del sitio'].sum()

                # Agrupar por fuente de tráfico y calcular visitas
                trafico_data = data.groupby('fuente de trafico').agg({
                    'sesiones del sitio': 'sum'
                }).rename(columns={'sesiones del sitio': 'visitas_por_fuente'})

                # Calcular la tasa de tráfico por fuente
                trafico_data['tasa_trafico'] = (trafico_data['visitas_por_fuente'] / total_visitas) * 100

                # Mostrar la fórmula utilizada
                st.markdown("""
                **Fórmula utilizada:**  
                Tasa de tráfico por fuente = (Visitas desde una fuente específica / Total de visitas) * 100
                """)

                # Crear una gráfica de barras
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(trafico_data.index, trafico_data['tasa_trafico'], color='skyblue')
                ax.set_title("Tasa de Tráfico por Fuente (%)")
                ax.set_xlabel("Fuente de Tráfico")
                ax.set_ylabel("Tasa de Tráfico (%)")
                ax.set_xticks(range(len(trafico_data.index)))
                ax.set_xticklabels(trafico_data.index, rotation=45, ha="right")

                # Mostrar la gráfica en Streamlit
                st.pyplot(fig)

                # Explicación de las Variables
                st.subheader("Explicación de las Variables")
                st.table(pd.DataFrame({
                    "Variable": ["Visitas por fuente", "Total de visitas", "Tasa de tráfico por fuente"],
                    "Descripción": [
                        "Número de visitas desde una fuente específica.",
                        "Suma total de visitas al sitio web.",
                        "Porcentaje de visitas provenientes de una fuente específica."
                    ]
                }))

                # Interpretaciones de los Resultados
                st.subheader("Interpretaciones de los Resultados")
                st.table(pd.DataFrame({
                    "Resultado": ["Alta (> 50%)", "Media (20% - 50%)", "Baja (< 20%)"],
                    "Interpretación": [
                        "La mayoría del tráfico proviene de esta fuente.",
                        "Fuente relevante, pero no dominante.",
                        "Fuente con poca contribución al tráfico total."
                    ]
                }))
            else:
                st.error("El archivo no contiene las columnas necesarias. Por favor, verifica los datos.")
        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")

    # KPI 3: Tasa de Rebote por Fuente
    with col3:
        st.subheader("KPI 3: Tasa de Rebote promedio por Fuente")

        try:
            # Leer los datos del archivo CSV
            data = pd.read_csv('files/Copy of tecnoglass - Informe de tráfico_2023-11-13-2.csv')

            # Limpiar y transformar la 'tasa de rebote' a numérico
            data['tasa de rebote'] = data['tasa de rebote'].str.replace('%', '').astype(float)

            # Calcular la tasa de rebote promedio por fuente de tráfico
            bounce_rate_per_source = data.groupby('fuente de trafico')['tasa de rebote'].mean().reset_index()
            bounce_rate_per_source = bounce_rate_per_source.rename(columns={'tasa de rebote': 'Tasa de Rebote (%)'})

            # Tabla de metadatos para las variables utilizadas en la fórmula
            metadata = pd.DataFrame({
                'Variable': [
                    'Tasa de rebote para una fuente',
                    'Número de registros por esa fuente',
                    'Tasa de Rebote promedio por fuente'
                ],
                'Descripción': [
                    'Porcentaje de sesiones donde el usuario abandona sin alguna interacción adicional desde una fuente específica.',
                    'Cantidad de registros (sesiones o eventos) asociados a una fuente de tráfico específica.',
                    'Promedio de las tasas de rebote calculadas a partir de las tasas individuales por fuente.'
                ]
            })

            # Tabla de posibles interpretaciones
            interpretations = pd.DataFrame({
                'Resultado': ['Alta (> 70%)', 'Media (40% - 70%)', 'Baja (< 40%)'],
                'Interpretación': [
                    'Alta tasa de rebote, los usuarios abandonan rápidamente el sitio.',
                    'Tasa moderada, podría requerir ajustes menores para que el usuario se mantenga en la página.',
                    'Buena retención, los usuarios interactúan más con el sitio.'
                ]
            })

            # Aplicación Streamlit
            st.markdown("""
            **Fórmula utilizada**:  
            Tasa de Rebote promedio por fuente = ∑(Tasa de rebote para una fuente) / número de registros por esa fuente
            """)

            # Mostrar la gráfica primero
            fig, ax = plt.subplots()
            ax.bar(bounce_rate_per_source['fuente de trafico'], bounce_rate_per_source['Tasa de Rebote (%)'],
                   color='green')
            ax.set_title('Tasa de Rebote por Fuente de Tráfico')
            ax.set_xlabel('Fuente de Tráfico')
            ax.set_ylabel('Tasa de Rebote (%)')
            ax.set_xticks(range(len(bounce_rate_per_source['fuente de trafico'])))
            ax.set_xticklabels(bounce_rate_per_source['fuente de trafico'], rotation=45)
            st.pyplot(fig)

            # Mostrar tabla del significado de las variables
            st.subheader("Explicación de las Variables")
            st.table(metadata)

            # Mostrar tabla de posibles interpretaciones
            st.subheader("Interpretaciones de los Resultados")
            st.table(interpretations)

        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")
