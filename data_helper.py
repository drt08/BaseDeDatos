import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


load_dotenv()


def create_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def create_table_and_insert_data(uploaded_file, table_name):
    conn = create_connection()
    cursor = conn.cursor()

   
    df = pd.read_excel(uploaded_file)

  
    if table_name == "Empleados":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Empleados (
            ID_Empleado INT PRIMARY KEY,
            Nombre VARCHAR(100),
            Departamento VARCHAR(100),
            Cargo VARCHAR(100),
            Fecha_Ingreso DATE
        )
        """)
    elif table_name == "Proyectos":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Proyectos (
            ID_Proyecto INT PRIMARY KEY,
            Nombre_Proyecto VARCHAR(100),
            ID_Empleado INT,
            Rol_en_Proyecto VARCHAR(100),
            Fecha_Inicio DATE,
            FOREIGN KEY (ID_Empleado) REFERENCES Empleados(ID_Empleado)
        )
        """)
    elif table_name == "Salarios":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Salarios (
            ID_Salario VARCHAR(10) PRIMARY KEY,
            ID_Empleado INT,
            Salario_Base DECIMAL(10, 2),
            Bonificacion DECIMAL(10, 2),
            Fecha_Actualizacion DATE,
            FOREIGN KEY (ID_Empleado) REFERENCES Empleados(ID_Empleado)
        )
        """)
    elif table_name == "Clientes":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Clientes (
            ID_Cliente INT PRIMARY KEY,
            Nombre_Cliente VARCHAR(100),
            Sector VARCHAR(100),
            ID_Proyecto INT,
            Fecha_Registro DATE,
            FOREIGN KEY (ID_Proyecto) REFERENCES Proyectos(ID_Proyecto)
        )
        """)
    elif table_name == "Proveedores":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Proveedores (
            ID_Proveedor INT PRIMARY KEY,
            Nombre_Proveedor VARCHAR(100),
            Servicio_Ofrecido VARCHAR(100),
            ID_Departamento INT,
            Fecha_Contratacion DATE,
            FOREIGN KEY (ID_Departamento) REFERENCES Departamentos(ID_Departamento)
        )
        """)
    elif table_name == "Capacitaciones":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Capacitaciones (
            ID_Capacitacion INT PRIMARY KEY,
            Nombre_Capacitacion VARCHAR(100),
            ID_Empleado INT,
            Fecha_Inicio DATE,
            Fecha_Finalizacion DATE,
            Proveedor VARCHAR(100),
            FOREIGN KEY (ID_Empleado) REFERENCES Empleados(ID_Empleado)
        )
        """)
    elif table_name == "Departamentos":
        cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS Departamentos (
            ID_Departamento INT PRIMARY KEY,
            Nombre_Departamento VARCHAR(100)
        )
        """)

  
    for i, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", tuple(row))

    conn.commit()
    cursor.close()
    conn.close()


def execute_query(query):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result)


def fetch_table_names():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return [table[0] for table in tables]


def fetch_table_data(table_name):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result)



























