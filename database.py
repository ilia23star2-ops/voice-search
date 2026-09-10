import sqlite3
import os

class Database:
    def __init__(self, db_path='probes.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()
    
    def init_db(self):
        """Инициализация БД и создание индексов"""
        cursor = self.conn.cursor()
        
        # Таблица проб
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS probes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                probe_code TEXT UNIQUE NOT NULL,
                work_order_number TEXT NOT NULL
            )
        ''')
        
        # Индекс для быстрого поиска
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_probe_code 
            ON probes(probe_code)
        ''')
        
        self.conn.commit()
    
    def add_probe(self, probe_code, work_order_number):
        """Добавление пробы"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO probes (probe_code, work_order_number)
                VALUES (?, ?)
            ''', (probe_code, work_order_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления: {e}")
            return False
    
    def find_work_order(self, probe_code):
        """Поиск наряда по коду пробы"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT work_order_number FROM probes
            WHERE probe_code = ?
        ''', (probe_code,))
        
        result = cursor.fetchone()
        return result[0] if result else None
    
    def import_from_list(self, data_list):
        """Импорт из списка [(probe_code, work_order), ...]"""
        cursor = self.conn.cursor()
        
        try:
            cursor.executemany('''
                INSERT OR REPLACE INTO probes (probe_code, work_order_number)
                VALUES (?, ?)
            ''', data_list)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False
    
    def get_stats(self):
        """Статистика БД"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM probes')
        count = cursor.fetchone()[0]
        return {'total_probes': count}
    
    def close(self):
        """Закрытие подключения"""
        self.conn.close()