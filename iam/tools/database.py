# -*- coding: utf-8 -*-
"""
IAM Database - Gestion de bases de datos
SQLite, MySQL, PostgreSQL, MongoDB
"""

import subprocess
import os
import json
from typing import Tuple, List, Dict, Any, Optional


class Database:
    """
    Gestion completa de bases de datos
    """
    
    def __init__(self):
        self.connections = {}
    
    # === SQLITE ===
    
    def sqlite_create(self, db_path: str) -> Tuple[bool, str]:
        """Crear base de datos SQLite"""
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.close()
            return True, f"[OK] Base de datos creada: {db_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def sqlite_query(self, db_path: str, query: str) -> Tuple[bool, Any]:
        """Ejecutar query SQLite"""
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                conn.close()
                return True, {"columns": columns, "rows": rows}
            else:
                conn.commit()
                affected = cursor.rowcount
                conn.close()
                return True, f"[OK] Query ejecutada. Filas afectadas: {affected}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def sqlite_tables(self, db_path: str) -> Tuple[bool, List[str]]:
        """Listar tablas SQLite"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        success, result = self.sqlite_query(db_path, query)
        if success and isinstance(result, dict):
            return True, [row[0] for row in result.get("rows", [])]
        return False, []
    
    def sqlite_table_info(self, db_path: str, table: str) -> Tuple[bool, List[Dict]]:
        """Obtener info de una tabla"""
        query = f"PRAGMA table_info({table})"
        success, result = self.sqlite_query(db_path, query)
        if success and isinstance(result, dict):
            return True, result.get("rows", [])
        return False, []
    
    def sqlite_export(self, db_path: str, output_file: str) -> Tuple[bool, str]:
        """Exportar SQLite a JSON"""
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            data = {}
            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                data[table] = {
                    "columns": columns,
                    "rows": [dict(zip(columns, row)) for row in rows]
                }
            
            conn.close()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, f"[OK] Exportado a: {output_file}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === MYSQL ===
    
    def mysql_connect(self, host: str, user: str, password: str, 
                      database: str = None, port: int = 3306) -> Tuple[bool, str]:
        """Conectar a MySQL"""
        try:
            import mysql.connector
            config = {
                'host': host,
                'user': user,
                'password': password,
                'port': port
            }
            if database:
                config['database'] = database
            
            conn = mysql.connector.connect(**config)
            conn_id = f"{host}:{port}"
            self.connections[conn_id] = conn
            return True, f"[OK] Conectado a MySQL: {conn_id}"
        except ImportError:
            return False, "[ERROR] mysql-connector-python no instalado. Instala con: pip install mysql-connector-python"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def mysql_query(self, connection_id: str, query: str) -> Tuple[bool, Any]:
        """Ejecutar query MySQL"""
        try:
            if connection_id not in self.connections:
                return False, "[ERROR] Conexion no encontrada"
            
            conn = self.connections[connection_id]
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return True, {"columns": columns, "rows": rows}
            else:
                conn.commit()
                return True, f"[OK] Query ejecutada. Filas: {cursor.rowcount}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def mysql_databases(self, connection_id: str) -> Tuple[bool, List[str]]:
        """Listar bases de datos"""
        success, result = self.mysql_query(connection_id, "SHOW DATABASES")
        if success and isinstance(result, dict):
            return True, [row[0] for row in result.get("rows", [])]
        return False, []
    
    def mysql_tables(self, connection_id: str, database: str) -> Tuple[bool, List[str]]:
        """Listar tablas"""
        success, result = self.mysql_query(connection_id, f"USE {database}; SHOW TABLES")
        if success and isinstance(result, dict):
            return True, [row[0] for row in result.get("rows", [])]
        return False, []
    
    # === POSTGRESQL ===
    
    def postgresql_connect(self, host: str, user: str, password: str,
                          database: str, port: int = 5432) -> Tuple[bool, str]:
        """Conectar a PostgreSQL"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=host, user=user, password=password,
                database=database, port=port
            )
            conn_id = f"{host}:{port}"
            self.connections[conn_id] = conn
            return True, f"[OK] Conectado a PostgreSQL: {conn_id}"
        except ImportError:
            return False, "[ERROR] psycopg2 no instalado. Instala con: pip install psycopg2-binary"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def postgresql_query(self, connection_id: str, query: str) -> Tuple[bool, Any]:
        """Ejecutar query PostgreSQL"""
        try:
            if connection_id not in self.connections:
                return False, "[ERROR] Conexion no encontrada"
            
            conn = self.connections[connection_id]
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return True, {"columns": columns, "rows": rows}
            else:
                conn.commit()
                return True, f"[OK] Query ejecutada. Filas: {cursor.rowcount}"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    # === GENERALES ===
    
    def close_connection(self, connection_id: str) -> Tuple[bool, str]:
        """Cerrar conexion"""
        try:
            if connection_id in self.connections:
                self.connections[connection_id].close()
                del self.connections[connection_id]
                return True, f"[OK] Conexion {connection_id} cerrada"
            return False, "[ERROR] Conexion no encontrada"
        except Exception as e:
            return False, f"[ERROR] {e}"
    
    def list_connections(self) -> List[str]:
        """Listar conexiones activas"""
        return list(self.connections.keys())
    
    def backup_database(self, db_path: str, backup_path: str) -> Tuple[bool, str]:
        """Crear backup de SQLite"""
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            return True, f"[OK] Backup creado: {backup_path}"
        except Exception as e:
            return False, f"[ERROR] {e}"


# Instancia global
database = Database()
