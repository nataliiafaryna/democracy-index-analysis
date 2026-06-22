import wbgapi as wb
import pandas as pd

# Отримуємо дані про ВВП на душу населення (GDP per capita, PPP) за 2022 рік
# NY.GDP.PCAP.PP.CD - це код показника у Світовому банку
gdp_data = wb.data.DataFrame('NY.GDP.PCAP.PP.CD', time=2022, labels=True)

# Оновимо назви колонок для зручності
gdp_data.columns = ['Country', 'GDP_2022']

print(gdp_data.head()) # Покаже перші 5 рядків