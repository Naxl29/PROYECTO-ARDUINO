from conexion import mysql # Se importa el archivo de conexion


# Funcion para mostrar historial osea los usuario que encienden y apagan el boton
def see():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.id, u.usuario, b.fecha, b.estado, b.anterior_hash, b.hash
        FROM blockchain b
        JOIN usuarios u ON b.id_usuario = u.id
        ORDER BY b.id ASC
    """)
    bloques = cursor.fetchall()
    conn.close()

    return bloques

# Funcion para mostar los datos el usuario creado actualmente
def show(id):
    conn = mysql.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s LIMIT 1", (id,))
    fila = cursor.fetchone()
    conn.close()
    return fila if fila else False