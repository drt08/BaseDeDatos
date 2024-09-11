import streamlit as st
import pandas as pd
import io
from data_helper import extract_and_combine_data_from_excel, save_to_database

st.title('Combina Archivos de Excel de Empleados y Proyectos')


uploaded_file_empleados = st.file_uploader("Cargar archivo de Empleados", type=["xlsx"])
uploaded_file_proyectos = st.file_uploader("Cargar archivo de Proyectos", type=["xlsx"])


if st.button("Combinar y Mostrar Datos"):
    if uploaded_file_empleados is not None and uploaded_file_proyectos is not None:
        try:
            
            df_combinado = extract_and_combine_data_from_excel(uploaded_file_empleados, uploaded_file_proyectos)
            
            
            st.write("Datos Combinados")
            st.dataframe(df_combinado)

            
            message = save_to_database(df_combinado)
            st.success(message)

            
            combined_file = io.BytesIO()
            with pd.ExcelWriter(combined_file, engine='xlsxwriter') as writer:
                df_combinado.to_excel(writer, index=False, sheet_name='Datos_Combinados')
            combined_file.seek(0)
            
            st.download_button(
                label="Descargar Datos Combinados",
                data=combined_file,
                file_name='Datos_Combinados.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        except Exception as e:
            st.error(f"Error al combinar los datos: {e}")
    else:
        st.info("Por favor, sube ambos archivos de Excel.")



