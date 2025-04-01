import streamlit as st
from kpisequipo4 import dashboard_objetivo_4
from kpisequipo1 import dashboard_objetivo_1
from kpisequipo3 import dashboard_objetivo_3
from kpisequipo2 import dashboard_objetivo_2

def main():
    # Configuración de la página (debe estar solo aquí)
    st.set_page_config(page_title="Objetivos SMART", layout="wide")

    # Título principal
    st.title("Dashboard Tecnhoglass")

    # Menú de navegación en la barra lateral
    menu = st.sidebar.radio(
        "Menú de Navegación",
        ["Página Principal", "KPIs del Objetivo 1", "KPIs del Objetivo 2", "KPIs del Objetivo 3", "KPIs del Objetivo 4"]
    )

    # Página Principal
    if menu == "Página Principal":
        st.header("Objetivos SMART:")
        st.subheader("**Objetivo SMART 1**: Alcanzar 150 seguidores en instagram y al menos 100 seguidores en facebook para finales de noviembre de 2024, mediante la publicación de contenido mensual y la interacción activa con la comunidad. Basado en publicidad orgánica.")
        st.write("**Desarrollado por**: Dana Carlon, Yohali Fernández y Michelle Pérez.")

        st.subheader("**Objetivo SMART 2**: Evaluar la efectividad de los productos de Technoglass mediante el análisis de cuatro KPIs clave: índice de satisfacción del cliente (CSAT), tasa de participación de ventas, margen sobre el costo de adquisición (Markup), y tasa de conversión, para identificar áreas de mejora en calidad, precio y aceptación de los productos.")
        st.write("**Desarrollado por**: Jose Blazquez, Andrea Hernandez, Danna Garcia, Ricardo Aguilar.")

        st.subheader("**Objetivo SMART 3**: Aumentar el alcance, ventas e impresiones en instagram y facebook en un 20% al implementar el uso de publicidad pagada durante 5 días.")
        st.write("**Desarrollado por**: Natalia Tirado ,Jazmin Quezada, Herik Maldonado.")

        st.subheader("**Objetivo SMART 4**: Generar que el 30% del tráfico hacia el sitio web provenga de redes sociales logrando que al menos el 20% de esos usuarios permanezcan en el sitio web durante un mínimo de 1 minuto y manteniendo la tasa de rebote por debajo del 70% para finales de noviembre de 2024.")
        st.write("**Desarrollado por**: Hassel Maciel García, Danna Martinez Carrasco, Gretshell Martinez Figueroa.")

    # Opcion para KPIs del Objetivo 1
    elif menu == "KPIs del Objetivo 1":
        dashboard_objetivo_1()

    elif menu == "KPIs del Objetivo 2":
        dashboard_objetivo_2()

    elif menu == "KPIs del Objetivo 3":
        dashboard_objetivo_3()

    # Opción para KPIs del Objetivo 4
    elif menu == "KPIs del Objetivo 4":
        dashboard_objetivo_4()

# Llamar a la función principal
if __name__ == "__main__":
    main()