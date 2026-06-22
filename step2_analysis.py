import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression # ДОДАНО: імпорт для розрахунку лінії

df = pd.read_csv('../data/processed_data.csv')

# 2. Розрахунок кореляції
# Коефіцієнт Пірсона: від -1 до 1.
# Ближче до 1 = сильний зв'язок.
correlation_matrix = df[['GDP', 'Democracy', 'Corruption']].corr()

print(" Матриця кореляції:")
print(correlation_matrix)

# 3. Візуалізація №1: Зв'язок Корупції та ВВП
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Corruption', y='GDP', scatter_kws={'alpha':0.5}, line_kws={'color':'red'})

plt.title('Зв’язок між Індексом корупції та ВВП на душу населення')
plt.xlabel('Індекс сприйняття корупції (чим більше, тим менше корупції)')
plt.ylabel('ВВП на душу населення (USD)')
plt.grid(True, linestyle='--', alpha=0.6)

# Підпишемо деякі країни для наочності (Україна, Польща, тощо)
countries_to_label = ['Ukraine', 'Poland', 'Germany', 'Norway', 'Singapore', 'Afghanistan']
for country in countries_to_label:
    if country in df['Name'].values:
        row = df[df['Name'] == country].iloc[0]
        plt.text(row['Corruption'], row['GDP'], country, fontsize=9, fontweight='bold')

plt.savefig('../data/corruption_vs_gdp.png')
print("\n Графік 'corruption_vs_gdp.png' збережено у папку data.")


# 1. Очищаємо дані від пропусків (NaN) тільки для цих двох колонок
df_clean = df.dropna(subset=['Corruption', 'GDP'])

# 2. Беремо вже очищені дані
X_simple = df_clean[['Corruption']]
y_simple = df_clean['GDP']

# 3. Рахуємо модель
simple_model = LinearRegression()
simple_model.fit(X_simple, y_simple)

print("\n Рівняння простої червоної лінії тренду (Слайд 7):")
print(f"ВВП = {simple_model.intercept_:.2f} + {simple_model.coef_[0]:.2f} * Corruption")
print("ШПАРГАЛКА: Якщо корупція зменшується на 1 бал (індекс зростає на 1), ВВП зростає на", round(simple_model.coef_[0], 2), "доларів.")
# 4. Візуалізація №2: Теплова карта кореляції
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Матриця взаємозв’язку показників')
plt.savefig('../data/correlation_heatmap.png')
print("\n Графік 'correlation_heatmap.png' збережено.")

plt.show()