import mysql.connector
from mysql.connector import Error
from pyswip import Prolog

# Inicializar Prolog y cargar archivo de conocimientos
prolog = Prolog()
prolog.consult("enfermedades.pl")

# Conexión a MySQL
def conectar_mysql():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='hospital',
            user='app_user',
            password='secure_password'
        )
        return conn
    except Error as e:
        print(f"Error de conexión a MySQL: {e}")
        return None

# Inicializar base de datos y tabla
def init_db():
    conn = conectar_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255),
                            edad INT,
                            genero VARCHAR(50),
                            sintomas TEXT,
                            diagnostico VARCHAR(255),
                            tratamiento TEXT
                          )''')
        conn.commit()
        cursor.close()
        conn.close()

# Agregar paciente sin diagnóstico inicial
def agregar_paciente(nombre, edad, genero, sintomas):
    conn = conectar_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes (nombre, edad, genero, sintomas) VALUES (%s, %s, %s, %s)",
                       (nombre, edad, genero, sintomas))
        conn.commit()
        cursor.close()
        conn.close()
        print("Paciente agregado con éxito.")

# Actualizar paciente con diagnóstico y tratamiento
def actualizar_paciente(id_paciente, diagnostico, tratamiento):
    conn = conectar_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE pacientes SET diagnostico = %s, tratamiento = %s WHERE id = %s",
                       (diagnostico, tratamiento, id_paciente))
        conn.commit()
        cursor.close()
        conn.close()
        print("Información de diagnóstico y tratamiento actualizada.")

# Obtener diagnóstico y tratamiento en base a los síntomas
def diagnosticar_paciente(sintomas_texto):
    # Convertir los síntomas a una lista y ajustarlos para Prolog
    sintomas_lista = sintomas_texto.replace(" ", "").split(",")
    sintomas_lista_prolog = f"[{', '.join(sintomas_lista)}]"
    consulta = list(prolog.query(f"diagnosticar({sintomas_lista_prolog}, Enfermedad)"))
    
    if consulta:
        enfermedad = consulta[0]['Enfermedad']
        tratamiento_query = list(prolog.query(f"obtener_tratamiento({enfermedad}, Tratamiento)"))
        if tratamiento_query:
            tratamiento = tratamiento_query[0]['Tratamiento']
            return enfermedad, ", ".join(tratamiento)
    return None, None

# Menú del sistema
def menu():
    init_db()
    while True:
        print("\n--- Sistema de Gestión Médica ---")
        print("1. Agregar nuevo paciente")
        print("2. Ver todos los pacientes")
        print("3. Diagnosticar paciente")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            edad = int(input("Edad: "))
            genero = input("Género (Masculino/Femenino/Otro): ")
            sintomas = input("Ingrese los síntomas separados por comas: ")
            agregar_paciente(nombre, edad, genero, sintomas)
        
        elif opcion == "2":
            conn = conectar_mysql()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pacientes")
                pacientes = cursor.fetchall()
                for paciente in pacientes:
                    print(f"\nID: {paciente[0]}, Nombre: {paciente[1]}, Edad: {paciente[2]}, Género: {paciente[3]}")
                    print(f"  Síntomas: {paciente[4]}, Diagnóstico: {paciente[5]}, Tratamiento: {paciente[6]}")
                cursor.close()
                conn.close()
        
        elif opcion == "3":
            nombre = input("Ingrese el nombre del paciente para diagnosticar: ")
            conn = conectar_mysql()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pacientes WHERE nombre = %s", (nombre,))
                paciente = cursor.fetchone()
                if paciente:
                    sintomas = paciente[4]
                    diagnostico, tratamiento = diagnosticar_paciente(sintomas)
                    if diagnostico and tratamiento:
                        print(f"Diagnóstico: {diagnostico}")
                        print(f"Tratamiento: {tratamiento}")
                        actualizar_paciente(paciente[0], diagnostico, tratamiento)
                    else:
                        print("No se encontró un diagnóstico basado en los síntomas proporcionados.")
                else:
                    print("Paciente no encontrado.")
                cursor.close()
                conn.close()
        
        elif opcion == "4":
            print("Saliendo del sistema.")
            break
        
        else:
            print("Opción no válida.")

menu() 