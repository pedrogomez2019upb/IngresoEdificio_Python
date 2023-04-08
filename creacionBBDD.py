# -*- coding: utf-8 -*-
import sqlite3

# Creamos la conexión a la base de datos
conn = sqlite3.connect('acceso.db')

# Creamos la tabla usuarios
conn.execute('''CREATE TABLE usuarios
         (identificacion INTEGER PRIMARY KEY,
          nombre TEXT NOT NULL,
          apellido TEXT NOT NULL
          );''')

# Creamos la tabla tarjetas
conn.execute('''CREATE TABLE tarjetas
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
          id_usuario INTEGER NOT NULL,
          numero_tarjeta TEXT NOT NULL UNIQUE,
          FOREIGN KEY (id_usuario) REFERENCES usuarios(identificacion));''')

# Cerramos la conexión
conn.close()
