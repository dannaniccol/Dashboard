import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def dashboard_objetivo_2():
    # Título de la aplicación
    st.title("Dashboard de Análisis de Ventas")

    # Menú principal
    menu = st.selectbox(
        "Selecciona un Dashboard",
        ["Tasa de Participación de Ventas", "Análisis de Markup - Margen sobre el Costo de Adquisición",
         "Porcentaje de prospectos que realizan una compra", "Análisis del KPI: CSAT (Customer Satisfaction Score)"]
    )

    # Función para procesar un DataFrame
    def procesar_dataframe(df):
        df['Modelo'] = df['Modelo'].str.strip().str.lower()
        for col in ['Venta Total', 'Precio']:
            df[col] = pd.to_numeric(df[col].astype(str).replace({'\$': '', ',': ''}, regex=True), errors='coerce')
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
        df = df.dropna(subset=['Venta Total', 'Precio', 'Cantidad'])

        df_agrupado = df.groupby('Modelo', as_index=False).agg({
            'Venta Total': 'sum',
            'Cantidad': 'sum',
            'Precio': 'mean'
        })
        ventas_totales = df_agrupado['Venta Total'].sum()
        df_agrupado['Tasa de Participación (%)'] = (df_agrupado['Venta Total'] / ventas_totales) * 100
        return df_agrupado.sort_values('Tasa de Participación (%)', ascending=False), ventas_totales

    # Función para visualizar resultados
    def visualizar_resultados(df, tipo_venta, ventas_totales):
        st.write(f"### Tabla de Resultados: {tipo_venta}")
        st.dataframe(df)

        plt.figure(figsize=(12, 6))
        plt.bar(df['Modelo'], df['Tasa de Participación (%)'], color='skyblue')
        plt.title(f"Tasa de Participación de Ventas por Modelo - {tipo_venta}", fontsize=16)
        plt.xlabel("Modelo", fontsize=12)
        plt.ylabel("Tasa de Participación (%)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.close()

        st.write(f"### Resumen de Ventas: {tipo_venta}")
        st.write(f"Ventas Totales: ${ventas_totales:,.2f}")
        st.write(f"Número de Modelos: {len(df)}")

    # Función para mostrar tablas estáticas
    def mostrar_tabla(titulo, data):
        st.write(f"### {titulo}")
        st.dataframe(pd.DataFrame(data))

    # Dashboard 1: Tasa de Participación de Ventas
    if menu == "Tasa de Participación de Ventas":
        st.subheader("Tasa de Participación de Ventas por Modelo")

        st.markdown("""
        **Fórmula del KPI:**  
        Tasa de Participación de Ventas = (Ventas del producto / Ventas totales) x 100
        """)

        # Rutas de los archivos CSV
        csv_paths = {
            "Mayoreo": "files/Formatos - Ventas al mayoreo.csv",
            "Normales": "files/Formatos - Ventas.csv"
        }

        # Cargar, procesar y visualizar los datos
        for tipo_venta, path in csv_paths.items():
            try:
                df = pd.read_csv(path)
                df_procesado, ventas_totales = procesar_dataframe(df)
                st.write(f"## Análisis de Ventas: {tipo_venta}")
                visualizar_resultados(df_procesado, tipo_venta, ventas_totales)
            except FileNotFoundError:
                st.error(f"No se encontró el archivo CSV para {tipo_venta}. Verifica la ruta.")
                st.stop()
            except Exception as e:
                st.error(f"Ocurrió un error procesando {tipo_venta}: {e}")
                st.stop()

        # Mostrar tablas adicionales
        mostrar_tabla("Explicación de las Variables Utilizadas", {
            "Variable": ["Venta Total", "Cantidad", "Precio", "Tasa de Participación (%)"],
            "Descripción": [
                "Total de ventas del modelo (suma de ventas de unidades).",
                "Cantidad total de unidades vendidas de cada modelo.",
                "Precio promedio de venta por unidad del modelo.",
                "Porcentaje de participación de cada modelo en el total de ventas."
            ]
        })

        mostrar_tabla("Interpretación de los Resultados del KPI", {
            "Tasa de Participación (%)": ["Alta (> 20%)", "Moderada (10-20%)", "Baja (< 10%)"],
            "Interpretación": [
                "El modelo tiene una gran participación en las ventas totales, es un producto clave.",
                "El modelo tiene una participación moderada, es un producto relevante pero no principal.",
                "El modelo tiene una baja participación, podría necesitar promoción o revisión de precios."
            ]
        })

    # Dashboard 2: Placeholder
    elif menu == "Análisis de Markup - Margen sobre el Costo de Adquisición":
        df = pd.read_csv('files/KPI - Markup (Margen sobre el Costo de Adquisición) - Hoja 1.csv')

        df.columns = df.columns.str.strip()

        st.title('Análisis de Markup - Margen sobre el Costo de Adquisición')
        st.write("Fórmula: (Precio de venta - Costo de adquisición / Costo de adquisición) x100")

        # Calcular el Markup
        df['Markup_Porcentaje%'] = ((df['Precio_venta'] - df['Costo_adquisicion']) / df['Costo_adquisicion']) * 100

        # Mostrar los datos con el markup calculado
        st.subheader('Datos con Markup calculado:')
        st.dataframe(df[['Producto', 'Precio_venta', 'Costo_adquisicion', 'Markup_Porcentaje%']])

        # Mostrar gráfico
        st.subheader('Gráfico de Markup de los Productos')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['Producto'], df['Markup_Porcentaje%'], color='skyblue')
        ax.set_title('Markup de los Productos')
        ax.set_xlabel('Producto')
        ax.set_ylabel('Markup (%)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        st.pyplot(fig)

        # Interpretaciones de los resultados
        st.subheader('Interpretaciones de los resultados:')
        interpretaciones = []

        # Crear una lista con las interpretaciones
        for index, row in df.iterrows():
            producto = row['Producto']
            markup = row['Markup_Porcentaje%']
            interpretacion = ""

            if producto == "Vidrio templado":
                interpretacion = ("El markup para el vidrio templado es de 900%, lo que indica que el precio de venta "
                                  "es 9 veces superior al costo de adquisición, lo que refleja un alto margen de ganancia.")
            elif producto == "Pantalla completa":
                interpretacion = (
                    "El markup para la pantalla completa es de 366.67%, lo que significa que el precio de "
                    "venta es 3.67 veces el costo de adquisición, un margen considerable.")
            elif producto == "Vidrio de privacidad":
                interpretacion = (
                    "El markup para el vidrio de privacidad es de 166.67%, lo que muestra que su precio de "
                    "venta es 1.67 veces el costo de adquisición, un margen más bajo en comparación con los otros productos.")

            # Agregar la interpretación a la lista
            interpretaciones.append({'Producto': producto, 'Interpretación': interpretacion})

        # Convertir la lista de interpretaciones en un DataFrame
        df_interpretaciones = pd.DataFrame(interpretaciones)

        # Mostrar la tabla de interpretaciones en Streamlit
        st.table(df_interpretaciones)

        # Explicación de las variables
        st.subheader('Explicación de las Variables:')
        explicaciones = [
            {'Variable': 'Producto', 'Descripción': 'Nombre del producto'},
            {'Variable': 'Precio_venta', 'Descripción': 'Precio al que se vende el producto al el público.'},
            {'Variable': 'Costo_adquisicion', 'Descripción': 'Precio que costó adquirir el producto.'},
            {'Variable': 'Markup_Porcentaje%',
             'Descripción': 'Porcentaje de ganancia del producto sobre el costo de adquisición.'}
        ]

        # Convertir la lista de explicaciones en un DataFrame
        df_explicaciones = pd.DataFrame(explicaciones)

        # Mostrar la tabla de explicaciones
        st.table(df_explicaciones)

    # Dashboard 3: Placeholder
    elif menu == "Porcentaje de prospectos que realizan una compra":
        df_prospectos = pd.read_csv('files/Prospectos - Hoja 1.csv')
        df_ventas = pd.read_csv('files/Prospectos - Hoja 2.csv')

        pd.DataFrame(df_prospectos)
        pd.DataFrame(df_ventas)

        ######## Prospectos ########
        Total_Likes = df_prospectos['Me gusta'].sum()
        Total_Compartidos = df_prospectos['Compartidos'].sum()
        Total_Comentarios = df_prospectos['Comentarios'].sum()

        Total_Prospectos = Total_Likes + Total_Compartidos + Total_Comentarios

        ####### Ventas #######
        Ventas_Cerradas = df_ventas['Ventas realizadas'].sum()

        ####### Tasa de conversion #######
        Tasa_Conversion = Ventas_Cerradas / Total_Prospectos * 100

        # Función para mostrar la página de Inicio
        def mostrar_inicio():
            st.title("Tasa de conversión")
            st.write("Porcentaje de prospectos que realizan una compra")

            # Mostramos la fórmula de tasa de conversión
            st.latex(r'''
            \small \text{Tasa de conversión} = \frac{\text{Número de ventas cerradas}}{\text{Número de prospectos}} \times 100
            ''')

            st.write('')
            st.write('')

            st.latex(fr'''
            \huge \text{{Tasa de conversión}} = \frac{{{Ventas_Cerradas}}}{{{Total_Prospectos}}} \times 100 = {Tasa_Conversion:.2f}\%
            ''')

            st.write('')

            col1, col2 = st.columns(2)

            # Mostrar DataFrames en columnas separadas
            with col1:
                st.subheader("Publicaciones")
                st.dataframe(df_prospectos)

            with col2:
                st.subheader("Ventas")
                st.dataframe(df_ventas)

            df_variables = pd.DataFrame({
                'Variable': ['Número de prospectos', 'Número de ventas cerradas'],
                'Significado': ['Cantidad de usuarios que realizaron una interaccion con la publicidad del producto. '
                                'En este caso se sumaron todos los likes, compartidos y comentarios para sacar los prospectos.',
                                'Total de ventas finalizadas.']
            })
            st.table(pd.DataFrame(df_variables))

            df_variables = pd.DataFrame({
                'Resultado': ['Tasa de conversión: 9.98%'],
                'Interpretacion': [
                    'Esto se interpreta de manera que la publicidad esta siendo poco efectiva ya que un porcentaje bajo de personas se han decidido comprar el producto. '
                    'Significando que de los 581 personas interesadas en el producto, solo 58 realmente se decidieron en comprar el producto.'
                ]
            })
            st.table(pd.DataFrame(df_variables))

        mostrar_inicio()

    # Dashboard 4: CSAT Analysis
    elif menu == "Análisis del KPI: CSAT (Customer Satisfaction Score)":
        # Función para leer el archivo CSV
        def leer_datos(archivo):
            return pd.read_csv(archivo)

        # Función para calcular el CSAT
        def calcular_csat(respuestas):
            respuestas_positivas = len(respuestas[respuestas == "Satisfecho"])
            total_respuestas = len(respuestas)
            csat = (respuestas_positivas / total_respuestas) * 100
            return csat, respuestas_positivas, total_respuestas

        # Función para generar el gráfico de distribución de respuestas
        def generar_grafico(respuestas, total_respuestas):
            plt.figure(figsize=(10, 4))
            respuesta_counts = respuestas.value_counts()
            respuesta_counts.plot(kind="bar", color=["green", "red"])
            plt.title("Distribución de Respuestas")
            plt.xlabel("Respuestas")
            plt.ylabel("Frecuencia")

            # Agregar los valores de cada barra como porcentaje
            for i, count in enumerate(respuesta_counts):
                porcentaje = (count / total_respuestas) * 100
                plt.text(i, count + 0.1, f"{porcentaje:.2f}%", ha='center', va='bottom', fontsize=10)

            st.pyplot(plt)

        # Función para mostrar la tabla de variables
        def mostrar_tabla_variables():
            tabla_variables = pd.DataFrame({
                "Variable": ["Total de respuestas", "Respuestas positivas"],
                "Descripción": [
                    "Número total de respuestas (Satisfecho + Insatisfecho)",
                    "Número de respuestas etiquetadas como 'Satisfecho'"
                ]
            })
            st.table(tabla_variables)

        # Función para mostrar la interpretación del CSAT
        def mostrar_interpretacion():
            interpretacion = pd.DataFrame({
                "CSAT (%)": ["Mayor a 80%", "Entre 60% y 80%", "Menor a 60%"],
                "Interpretación": [
                    "Alta satisfacción del cliente",
                    "Satisfacción moderada",
                    "Baja satisfacción del cliente"
                ]
            })
            st.table(interpretacion)

        st.title("Análisis del KPI: CSAT (Customer Satisfaction Score)")

        # Ruta del archivo CSV
        archivo = "files/Formatos - Ventas al mayoreo.csv"

        # Leer los datos
        datos = leer_datos(archivo)

        st.subheader("Fórmula del KPI: CSAT")
        st.write("CSAT = (Número de respuestas 'Satisfecho' / Número total de respuestas) x 100")

        # Verificar si la columna "Retroalimentacion: Satisfecho / Insatisfecho" existe
        if "Retroalimentacion: Satisfecho / Insatisfecho" in datos.columns:
            respuestas = datos['Retroalimentacion: Satisfecho / Insatisfecho']

            # Calcular el CSAT
            csat, respuestas_positivas, total_respuestas = calcular_csat(respuestas)

            st.subheader("CSAT Calculado")
            st.metric("CSAT (%)", f"{csat:.2f}")

            # Generar el gráfico
            st.subheader("Distribución de Respuestas")
            generar_grafico(respuestas, total_respuestas)

            # Mostrar la tabla de variables
            st.subheader("Tabla de Variables")
            mostrar_tabla_variables()

            # Mostrar la interpretación del CSAT
            st.subheader("Interpretación del KPI")
            mostrar_interpretacion()

        else:
            st.error("La columna 'Retroalimentacion: Satisfecho / Insatisfecho' no existe en el archivo.")

