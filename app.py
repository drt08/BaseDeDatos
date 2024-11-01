import streamlit as st
from data_helper import create_table_and_insert_data, execute_query, fetch_table_names, fetch_table_data

st.title("Base de Datos Empresa")


menu = ["Cargar Datos", "Consultas", "Ver Tablas"]
choice = st.sidebar.selectbox("Selecciona una opción", menu)


if choice == "Cargar Datos":
    st.subheader("Cargar datos desde archivos Excel")
    uploaded_files = {
        "Empleados": st.file_uploader("Cargar archivo de Empleados", type=["xlsx"]),
        "Proyectos": st.file_uploader("Cargar archivo de Proyectos", type=["xlsx"]),
        "Salarios": st.file_uploader("Cargar archivo de Salarios", type=["xlsx"]),
        "Clientes": st.file_uploader("Cargar archivo de Clientes", type=["xlsx"]),
        "Proveedores": st.file_uploader("Cargar archivo de Proveedores", type=["xlsx"]),
        "Capacitaciones": st.file_uploader("Cargar archivo de Capacitaciones", type=["xlsx"]),
        "Departamentos": st.file_uploader("Cargar archivo de Departamentos", type=["xlsx"])
    }

    if st.button("Subir Datos"):
        for table_name, uploaded_file in uploaded_files.items():
            if uploaded_file:
                try:
                    create_table_and_insert_data(uploaded_file, table_name)
                    st.success(f"Datos de {table_name} subidos correctamente.")
                except Exception as e:
                    st.error(f"Error al subir los datos de {table_name}: {e}")


elif choice == "Consultas":
    st.subheader("Consultas SQL")
    queries = {
        "Empleados y Proyectos": "SELECT Empleados.Nombre, Proyectos.Nombre_Proyecto, Proyectos.Rol_en_Proyecto FROM Empleados INNER JOIN Proyectos ON Empleados.ID_Empleado = Proyectos.ID_Empleado",
        "Clientes y Proyectos Asociados": "SELECT Clientes.Nombre_Cliente, Proyectos.Nombre_Proyecto FROM Clientes INNER JOIN Proyectos ON Clientes.ID_Proyecto = Proyectos.ID_Proyecto",
        "Proveedores por Departamento": "SELECT Proveedores.Nombre_Proveedor, Departamentos.Nombre_Departamento FROM Proveedores INNER JOIN Departamentos ON Proveedores.ID_Departamento = Departamentos.ID_Departamento",
        "Empleados con Salario Superior a 3000": "SELECT Nombre FROM Empleados INNER JOIN Salarios ON Empleados.ID_Empleado = Salarios.ID_Empleado WHERE Salarios.Salario_Base > 3000",
        "Proyectos y sus Clientes": "SELECT Proyectos.Nombre_Proyecto, Clientes.Nombre_Cliente FROM Proyectos LEFT JOIN Clientes ON Proyectos.ID_Proyecto = Clientes.ID_Proyecto",
        "Salario Más Alto por Empleado": "SELECT Empleados.Nombre, MAX(Salarios.Salario_Base) AS Salario_Mas_Alto FROM Empleados INNER JOIN Salarios ON Empleados.ID_Empleado = Salarios.ID_Empleado GROUP BY Empleados.Nombre",
        "Clientes por Sector": "SELECT Sector, COUNT(*) AS Total_Clientes FROM Clientes GROUP BY Sector",
        "Proyectos Activos": "SELECT Nombre_Proyecto FROM Proyectos WHERE Fecha_Inicio <= CURDATE()",
        "Departamentos y sus Proveedores": "SELECT Departamentos.Nombre_Departamento, Proveedores.Nombre_Proveedor FROM Departamentos LEFT JOIN Proveedores ON Departamentos.ID_Departamento = Proveedores.ID_Departamento",
        "Proyectos y su Duración": "SELECT Nombre_Proyecto, DATEDIFF(CURDATE(), Fecha_Inicio) AS Duracion_Dias FROM Proyectos WHERE Fecha_Inicio <= CURDATE()",
        "Empleados en Capacitación": "SELECT Empleados.Nombre FROM Empleados INNER JOIN Capacitaciones ON Empleados.ID_Empleado = Capacitaciones.ID_Empleado",
        "Clientes y su Último Proyecto": "SELECT Clientes.Nombre_Cliente, MAX(Proyectos.Fecha_Inicio) AS Ultima_Fecha FROM Clientes INNER JOIN Proyectos ON Clientes.ID_Proyecto = Proyectos.ID_Proyecto GROUP BY Clientes.Nombre_Cliente",
        "Empleados con Más de 5 Años de Servicio": "SELECT Nombre FROM Empleados WHERE DATEDIFF(CURDATE(), Fecha_Ingreso) > 1825",
        "Empleados y su Salario": "SELECT Empleados.Nombre, Salarios.Salario_Base FROM Empleados INNER JOIN Salarios ON Empleados.ID_Empleado = Salarios.ID_Empleado",
        "Empleados por Año de Ingreso": "SELECT YEAR(Fecha_Ingreso) AS Año, COUNT(*) AS Total_Empleados FROM Empleados GROUP BY YEAR(Fecha_Ingreso)"
    }

    query_choice = st.selectbox("Selecciona una consulta", list(queries.keys()))
    if st.button("Ejecutar Consulta"):
        query = queries[query_choice]
        try:
            results = execute_query(query)
            if results is not None:
               
                st.write("### Resultados")
                st.dataframe(results)
            else:
                st.warning("No se encontraron resultados.")
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")



elif choice == "Ver Tablas":
    st.subheader("Tablas en la base de datos")
    try:
        table_names = fetch_table_names()
        if table_names:
            for table_name in table_names:
                st.write(f"### Tabla: {table_name}")
                data = fetch_table_data(table_name)
                if data is not None:
                    st.dataframe(data)
                else:
                    st.warning(f"No hay datos en la tabla {table_name}.")
        else:
            st.warning("No hay tablas en la base de datos.")
    except Exception as e:
        st.error(f"Error al recuperar las tablas: {e}")





























