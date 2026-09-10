import csv
import openpyxl
from database import Database

def import_csv(file_path, db):
    """Импорт из CSV (формат: probe_code,work_order_number)"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Пропускаем заголовок
        
        for row in reader:
            if len(row) >= 2:
                probe_code = row[0].strip().replace(' ', '').upper()
                work_order = row[1].strip()
                data.append((probe_code, work_order))
    
    return db.import_from_list(data)

def import_excel(file_path, db):
    """Импорт из Excel (первый столбец - проба, второй - наряд)"""
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Пропускаем заголовок
        if len(row) >= 2 and row[0] and row[1]:
            probe_code = str(row[0]).strip().replace(' ', '').upper()
            work_order = str(row[1]).strip()
            data.append((probe_code, work_order))
    
    return db.import_from_list(data)

if __name__ == '__main__':
    # Пример использования
    db = Database()
    
    # Тестовые данные
    test_data = [
        ('ABC123', 'НАРЯД-001'),
        ('XYZ456', 'НАРЯД-002'),
        ('TEST789', 'НАРЯД-003'),
    ]
    
    db.import_from_list(test_data)
    print(f"Импортировано: {db.get_stats()['total_probes']} проб")