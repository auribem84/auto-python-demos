import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import requests
import pandas as pd

# -----------------------
# Cargar configuración
# -----------------------
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    expiry_days=config['cookie']['expiry_days']
)

# -----------------------
# Login moderno
# -----------------------
authenticator.login(location="main")

# -----------------------
# Estado de autenticación
# -----------------------
if st.session_state.get("authentication_status"):
    user = st.session_state.get("name")
    st.sidebar.success(f"Bienvenido {user}")
    authenticator.logout("Logout", "sidebar")

    # -----------------------
    # Dashboard VIN
    # -----------------------
    st.title("🚗 VIN Vehicle Dashboard")

    vin = st.text_input("Ingrese VIN")

    if vin:  # Solo procesar si hay un VIN
        if st.button("Decode VIN"):
            with st.spinner("Consultando base de datos NHTSA..."):
                try:
                    # Llamada a la API oficial del VIN
                    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
                    r = requests.get(url)
                    r.raise_for_status()
                    data = r.json()

                    # Filtrar resultados con valor
                    resultados = {item['Variable']: item['Value'] for item in data['Results'] if item['Value']}

                    # Campos importantes para mostrar
                    campos = [
                        "Make",
                        "Model",
                        "Model Year",
                        "Vehicle Type",
                        "Body Class",
                        "Engine Cylinders",
                        "Displacement (L)",
                        "Fuel Type - Primary",
                        "Transmission Style",
                        "Plant Country"
                    ]

                    resumen = {c: resultados.get(c, "N/A") for c in campos}

                    # Mostrar datos resumidos en métricas
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Información general")
                        st.metric("Marca", resumen["Make"])
                        st.metric("Modelo", resumen["Model"])
                        st.metric("Año", resumen["Model Year"])
                        st.metric("Tipo Vehículo", resumen["Vehicle Type"])

                    with col2:
                        st.subheader("Especificaciones técnicas")
                        st.metric("Cilindros", resumen["Engine Cylinders"])
                        st.metric("Desplazamiento (L)", resumen["Displacement (L)"])
                        st.metric("Combustible", resumen["Fuel Type - Primary"])
                        st.metric("Transmisión", resumen["Transmission Style"])
                        st.metric("País Planta", resumen["Plant Country"])

                    # Tabla completa
                    st.subheader("Reporte completo")
                    df = pd.DataFrame(resumen.items(), columns=["Especificación", "Valor"])
                    st.dataframe(df)

                except Exception as e:
                    st.error(f"Error al consultar el VIN: {e}")

else:
    st.warning("Ingrese usuario y contraseña")