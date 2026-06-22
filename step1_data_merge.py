import pandas as pd
import wbgapi as wb
import os


try:

    gdp_df = wb.data.DataFrame('NY.GDP.PCAP.PP.CD', time=2022, labels=True).reset_index()
    # Вибираємо перші 3 стовпці: код країни, назва країни, значення ВВП
    gdp_final = gdp_df.iloc[:, [0, 1, 2]]
    gdp_final.columns = ['Code', 'Name', 'GDP']


    dem_df = pd.read_csv('../data/democracy-index-eiu.csv')
    # Фільтруємо 2022 рік та вибираємо потрібні колонки
    dem_2022 = dem_df[dem_df['Year'] == 2022][['Code', 'Democracy score']]
    dem_2022.columns = ['Code', 'Democracy']



    cpi_df = pd.read_csv('../data/cpi_data.csv', sep=';')

    # Вибираємо колонку ISO3 та бал за 2022 рік
    cpi_final = cpi_df[['ISO3', 'CPI score 2022']].copy()
    cpi_final.columns = ['Code', 'Corruption']

    # ВВП + Демократія
    merged_data = pd.merge(gdp_final, dem_2022, on='Code', how='inner')

    # додаємо Корупцію
    final_df = pd.merge(merged_data, cpi_final, on='Code', how='inner')

    # Очистка від порожніх рядків (якщо вони є)
    final_df = final_df.dropna()

    # Зберігаємо фінальний результат
    output_path = '../data/processed_data.csv'
    final_df.to_csv(output_path, index=False)

    # Виводимо перші 5 країн для перевірки
    print(final_df.head())

except FileNotFoundError:
    print(
        "\n❌ Помилка: Не знайдено файл! Перевір, щоб 'cpi_data.csv' та 'democracy-index-eiu.csv' лежали в папці 'data'.")
except Exception as e:
    print(f"\n❌ Виникла помилка: {e}")
    