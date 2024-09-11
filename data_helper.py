import pandas as pd
import mysql.connector
from mysql.connector import Error

def extract_and_combine_data_from_excel(empleados_file, proyectos_file):
    """Extracts and combines employee and project data from the provided Excel files."""
    try:
        df_empleados = pd.read_excel(empleados_file)
        df_proyectos = pd.read_excel(proyectos_file)
    except Exception as e:
        raise Exception(f"Error reading the Excel files: {e}")


    df_empleados = df_empleados.rename(columns={
        'ID de Empleado': 'ID de Empleado',
        'Nombre': 'Nombre',
        'Departamento': 'Departamento',
        'Cargo': 'Cargo',
        'Fecha de Ingreso': 'Fecha de Ingreso'
    })

    df_proyectos = df_proyectos.rename(columns={
        'ID de Proyecto': 'ID de Proyecto',
        'Nombre del Proyecto': 'Nombre del Proyecto',
        'ID de Empleado': 'ID de Empleado',
        'Rol en el Proyecto': 'Rol en el Proyecto',
        'Fecha de Inicio': 'Fecha de Inicio'
    })

  
    df_combinado = pd.merge(df_empleados, df_proyectos, on='ID de Empleado', how='left')

    return df_combinado

def save_to_database(df_combinado):
    """Guarda el DataFrame combinado en la base de datos y verifica el resultado."""
    try:
       
        connection = mysql.connector.connect(
            host='localhost',
            user='daniela',
            password='daniela',
            database='empresa'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS empleados_proyectos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_empleado VARCHAR(255),
                nombre VARCHAR(255),
                departamento VARCHAR(255),
                cargo VARCHAR(255),
                fecha_ingreso DATE,
                id_proyecto VARCHAR(255),
                nombre_proyecto VARCHAR(255),
                rol_proyecto VARCHAR(255),
                fecha_inicio DATE
            )
            """
            cursor.execute(create_table_query)

            
            insert_query = """
            INSERT INTO empleados_proyectos 
            (id_empleado, nombre, departamento, cargo, fecha_ingreso, id_proyecto, nombre_proyecto, rol_proyecto, fecha_inicio)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            
            data_to_insert = df_combinado[['ID de Empleado', 'Nombre', 'Departamento', 'Cargo', 'Fecha de Ingreso', 'ID de Proyecto', 'Nombre del Proyecto', 'Rol en el Proyecto', 'Fecha de Inicio']].values.tolist()

            
            cursor.executemany(insert_query, data_to_insert)
            connection.commit()

            
            cursor.execute("SELECT COUNT(*) FROM empleados_proyectos")
            row_count = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            if row_count > 0:
                return f"Datos guardados en la base de datos correctamente. Total de registros: {row_count}."
            else:
                return "No se insertaron datos en la base de datos."
        else:
            raise Exception("No se pudo conectar a la base de datos.")
    except Error as err:
        raise Exception(f"Error al conectar o insertar en la base de datos: {err}")




