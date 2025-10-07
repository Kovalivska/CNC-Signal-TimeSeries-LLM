#!/usr/bin/env python3
"""
Тест загрузки данных для IONOS Demo
"""

import os
import pandas as pd

def test_data_loading():
    print("🔍 Тестируем загрузку данных...")
    
    # Получаем путь к директории, где находится этот скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Текущая директория: {current_dir}")
    print(f"Рабочая директория: {os.getcwd()}")
    
    # Возможные пути к файлу данных
    possible_paths = [
        os.path.join(current_dir, "cnc_daten.csv"),
        os.path.join(current_dir, "..", "data_and_eda", "cnc_daten.csv"),
        "/Users/svitlanakovalivska/Industrial_Signal_Processing_TimeSeriesAnalysis/data_and_eda/cnc_daten.csv"
    ]
    
    print("\n📁 Проверяем пути:")
    for i, path in enumerate(possible_paths, 1):
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"{i}. {path}")
        print(f"   {'✅ Существует' if exists else '❌ Не найден'}")
        if exists:
            print(f"   📊 Размер: {size:,} байт")
        print()
    
    # Пробуем загрузить данные
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    if data_path:
        print(f"🎯 Используем путь: {data_path}")
        try:
            # Пробуем загрузить с разными разделителями
            try:
                df = pd.read_csv(data_path, delimiter=';')
                print(f"✅ Успешно загружено с ';': {len(df)} строк, {len(df.columns)} столбцов")
            except:
                df = pd.read_csv(data_path, delimiter=',')
                print(f"✅ Успешно загружено с ',': {len(df)} строк, {len(df.columns)} столбцов")
            
            print(f"📊 Столбцы: {list(df.columns[:5])}...")
            if 'name' in df.columns:
                print("✅ Столбец 'name' найден")
            else:
                print("❌ Столбец 'name' не найден")
                
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
    else:
        print("❌ Файл данных не найден ни по одному из путей!")

if __name__ == "__main__":
    test_data_loading()
