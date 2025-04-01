import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def dashboard_objetivo_1():
    # Cargar datos
    df_crecimiento = pd.read_csv('files/TECHNOGLASS_DF - Hoja 1.csv')
    df_engagement = pd.read_csv("files/TECHNOGLASS_DF - Hoja 2.csv")
    df_frecuencia = pd.read_csv("files/TECHNOGLASS_DF - Hoja 3.csv")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Crecimiento de Seguidores")
        st.markdown("**(Seguidores actuales / deseados) * 100**")

        df_crecimiento["Crecimiento_sept"] = (df_crecimiento["Periodo_sept"] / df_crecimiento[
            "Seguidores_deseados"]) * 100
        df_crecimiento["Crecimiento_oct"] = (df_crecimiento["Periodo_oct"] / df_crecimiento[
            "Seguidores_deseados"]) * 100
        df_crecimiento["Crecimiento_nov"] = (df_crecimiento["Periodo_nov"] / df_crecimiento[
            "Seguidores_deseados"]) * 100

        df_melted = df_crecimiento.melt(
            id_vars=["Red_Social"],
            value_vars=["Crecimiento_sept", "Crecimiento_oct", "Crecimiento_nov"],
            var_name="Periodo",
            value_name="Tasa_de_Crecimiento"
        )

        red_social = st.selectbox("Selecciona red social:", df_crecimiento["Red_Social"])
        filtro = df_melted[df_melted["Red_Social"] == red_social]

        fig1 = px.bar(
            filtro,
            x="Periodo",
            y="Tasa_de_Crecimiento",
            color="Periodo",
            title=f"Crecimiento en {red_social}",
            labels={"Tasa_de_Crecimiento": "%"},
            text="Tasa_de_Crecimiento"
        )

        fig1.add_trace(
            go.Scatter(
                x=filtro["Periodo"],
                y=[100] * len(filtro),
                mode="lines",
                name="Meta (100%)",
                line=dict(color="red", dash="dash")
            )
        )
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Engagement Rate")
        st.markdown("**(Total interacciones / alcance) * 100**")

        engagement_df = df_engagement[df_engagement['TIPO'].isin(['RESULTADO_FB', 'RESULTADO_IG', 'RESULTADO_TT'])]
        engagement_long = engagement_df.melt(
            id_vars='TIPO',
            value_vars=['SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE'],
            var_name='Mes',
            value_name='Engagement Rate'
        )

        engagement_long['TIPO'] = engagement_long['TIPO'].replace({
            'RESULTADO_FB': 'Facebook',
            'RESULTADO_IG': 'Instagram',
            'RESULTADO_TT': 'TikTok'
        })

        fig2 = px.line(
            engagement_long,
            x='Mes',
            y='Engagement Rate',
            color='TIPO',
            title='Engagement por Red Social',
            markers=True
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown("### Frecuencia de Publicaciones")
        st.markdown("**(Publicaciones realizadas / planeadas) * 100**")

        df_frecuencia['KPI_Frecuencia (%)'] = (df_frecuencia['Publicaciones Realizadas'] / df_frecuencia[
            'Publicaciones Planeadas']) * 100

        fig3 = px.bar(
            df_frecuencia,
            x='Mes',
            y='KPI_Frecuencia (%)',
            color='Red Social',
            title='Frecuencia de Publicación',
            barmode='group'
        )

        fig3.add_hline(
            y=100,
            line_dash="dash",
            line_color="red",
            annotation_text="Meta"
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander(" Interpretación Crecimiento"):
            st.markdown("""
            - **0-50%**: Aún falta para alcanzar la meta
            - **51-59%**: A mitad de la meta
            - **60-99%**: Cerca de alcanzar la meta
            - **100%+**: Meta lograda
            """)
            st.write("**Significado de las variables:**")
            tabla_explicativa = pd.DataFrame({
                "Variable": ["Seguidores actuales", "Seguidores deseados"],
                "Significado": [
                    "Cantidad de seguidores que se han tenido por mes.",
                    "Cantidad de seguidores que buscas tener al finalizar un periodo de tiempo."
                ]
            })
            st.table(tabla_explicativa)

    with col2:
        with st.expander(" Interpretación Engagement"):
            st.markdown("""
            - **0-33%**: Nivel bajo de interacción
            - **34-66%**: Nivel moderado de interacción
            - **67%+**: Nivel alto de interacción
            """)
            data = {
                "Variable": ["Total interacciones", "Alcance", "Engagement Rate"],
                "Descripción": [
                    "Número total de interacciones (likes + comentarios + compartidos) en el conjunto de publicaciones por mes.",
                    "Número de personas que han visto el contenido.",
                    "Métrica que mide la interacción de los usuarios con el contenido, expresada como un porcentaje."
                ]
            }
            variables_df = pd.DataFrame(data)
            st.write("**Significado de las variables:**")
            st.table(variables_df)
    with col3:
        with st.expander(" Interpretación Frecuencia"):
            st.markdown("""
            - **100%+**: Calendario cumplido o superado
            - **<100%**: No se alcanzó el objetivo
            """)
            st.write("**Significado de las variables**")
            valores_df = pd.DataFrame({
                "Variables de la formula": [
                    "Publicaciones realizadas",
                    "Publicaciones planeadas"
                ],
                "Significado": [
                    "Número de publicaciones realizadas en una red social.",
                    "Número de publicaciones planificadas en el calendario."
                ]
            })
            st.dataframe(valores_df)