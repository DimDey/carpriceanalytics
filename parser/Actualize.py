import pandas as pd

# Загрузите основной датасет
main_df = pd.read_csv('./data.csv', low_memory=False)

# Загрузите датасет с новыми данными
result_df = pd.read_csv('data/result1.csv')

# Переименуйте колонку 'city' в 'place' в датасете с новыми данными
result_df = result_df.rename(columns={'city': 'place'})
result_df = result_df.rename(columns={'brand': 'marka'})

# Добавить недостающие колонки в result_df
for col in main_df.columns:
    if col not in result_df.columns:
        result_df[col] = None

# Убедитесь, что порядок колонок одинаков
result_df = result_df[main_df.columns]

# Объедините два датасета, добавив новые записи в конец основного датасета
combined_df = pd.concat([main_df, result_df], ignore_index=True)

# Удалите дубликаты строк, если они есть, на основе уникального идентификатора, если он существует, или всех колонок
# Если у вас есть уникальный идентификатор, замените 'all_columns' на название этой колонки
# combined_df = combined_df.drop_duplicates(subset='unique_id', keep='last')

# Если уникального идентификатора нет, удалите дубликаты на основе всех колонок
combined_df = combined_df.drop_duplicates(keep='last')

# Сохраните объединенный датасет в новый CSV файл
combined_df.to_csv('./merged_result.csv', index=False)

print("Datasets merged and saved to 'merged_result.csv'")
