import pandas as pd
import uuid
import random
import csv

# Максимальное количество символов на колонку
MAX_CHARACTERS = 4000

# Функция для генерации случайного значения цены
def generate_random_price():
    return round(random.uniform(0.1, 10.9), 2)

# Функция для удаления лишних кавычек и скобок и оборачивания в двойные кавычки
def clean_and_quote(text):
    if pd.isna(text):
        return ''
    cleaned_text = str(text).replace('""', '').replace('"', '').replace('[', '').replace(']', '').replace(';', '')
    cleaned_text = cleaned_text[:MAX_CHARACTERS]
    cleaned_text = cleaned_text.replace('', "'")
    cleaned_text = cleaned_text.replace('\t', "'")
    cleaned_text = cleaned_text.replace('\\', '')

    # Обрезаем строку до максимального количества символов
    # return f'"{cleaned_text}"'
    return cleaned_text


# Чтение исходного CSV файла
input_file = 'full_dataset.csv'
output_file = 'my_dataset.csv'

# Чтение данных с использованием pandas
df = pd.read_csv(input_file)

# Оставляем только нужные колонки
# df = df[['title', 'ingredients', 'source']].rename(columns={'source': 'link'})
df = df[['title', 'ingredients','link']]

# Преобразуем массивы в строки, удаляем лишние кавычки и скобки, оборачиваем в двойные кавычки
df['title'] = df['title'].astype(str).apply(clean_and_quote)
df['ingredients'] = df['ingredients'].apply(clean_and_quote)
# df['directions'] = df['directions'].apply(clean_and_quote)
df['link'] = df['link'].astype(str).apply(clean_and_quote)


# Добавляем колонку total_price со случайными значениями
df['total_price'] = df.apply(lambda x: generate_random_price(), axis=1)

# Добавляем колонку id с уникальными идентификаторами в формате UUID
df['id'] = df.apply(lambda x: str(uuid.uuid4()), axis=1)

# Перемещаем колонку id на первое место
columns = ['id'] + [col for col in df.columns if col != 'id']
df = df[columns]

# Выводим количество строк в датасете
num_rows = df.shape[0]
print(f"Количество строк в датасете: {num_rows}")
print("Типы данных всех колонок:")
print(df.dtypes)

# Сохраняем результат в новый CSV файл с использованием параметра quotechar для двойных кавычек
df.to_csv(output_file, index=False, sep=';', quoting=csv.QUOTE_NONNUMERIC)

print(f"Новый файл сохранен как {output_file}")