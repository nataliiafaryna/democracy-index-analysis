import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Завантаження даних
df = pd.read_csv(r'C:\Users\ADMIN\OneDrive - lnu.edu.ua\Робочий стіл\курсова\data\processed_data.csv')

# Очищаємо дані від порожніх значень, якщо вони є
df = df.dropna(subset=['GDP', 'Democracy', 'Corruption'])


# --- А) КЛАСТЕРИЗАЦІЯ (K-Means) ---
# Нормалізуємо дані
scaler = StandardScaler()
features = scaler.fit_transform(df[['GDP', 'Democracy', 'Corruption']])

# Запускаємо алгоритм
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(features)


centers = df.groupby('Cluster')[['GDP', 'Democracy']].mean()

cluster_mapping = {}
for cluster_id, row in centers.iterrows():
    # Якщо середній ВВП групи космічно великий:
    if row['GDP'] > 90000:
        cluster_mapping[cluster_id] = "Надбагаті країни (Специфічні економіки)"
    # Якщо ВВП нормальний, а демократія висока:
    elif row['Democracy'] > 7.5:
        cluster_mapping[cluster_id] = "Багаті демократії"
    # Якщо демократія дуже низька:
    elif row['Democracy'] < 4.5:
        cluster_mapping[cluster_id] = "Бідні/ресурсні автократії"
    # Всі інші (середнячки):
    else:
        cluster_mapping[cluster_id] = "Перехідні / Гібридні режими"

# Застосовуємо правильні назви до нашого датасету
df['Cluster_Name'] = df['Cluster'].map(cluster_mapping)
# Застосовуємо правильні наукові назви до нашого датасету
df['Cluster_Name'] = df['Cluster'].map(cluster_mapping)
# Застосовуємо правильні назви до нашого датасету
df['Cluster_Name'] = df['Cluster'].map(cluster_mapping)


# --- Б) ПЕРЕДБАЧЕННЯ ТА ПОШУК АНОМАЛІЙ (Лінійна регресія) ---
# Навчаємо модель вгадувати демократію за грошима та рівнем відсутності корупції
X = df[['GDP', 'Corruption']]
y = df['Democracy']
model = LinearRegression()
model.fit(X, y)

# Створюємо теоретичний індекс (яким він мав би бути)
df['Predicted_Democracy'] = np.round(model.predict(X), 2)

# Шукаємо відхилення від системи (Реальність мінус Модель)
# Додатне число = Демократія розвинена краще, ніж "має бути".
# Від'ємне = Країна багата/некорумпована, але залишається диктатурою.
df['Anomaly'] = np.round(df['Democracy'] - df['Predicted_Democracy'], 2)


# ПОБУДОВА ВІЗУАЛІЗАЦІЇ (ДЖЕРЕЛО КЕРУВАННЯ)
fig = go.Figure()

# Список показників
metrics = ['Democracy', 'Corruption', 'GDP', 'Cluster', 'Predicted_Democracy', 'Anomaly']
metric_names = [
    'Демократія (Факт)',
    'Індекс сприйняття корупції (CPI)',
    'ВВП на душу населення',
    'Кластери (K-Means)',
    'Демократія (ML Модель)',
    'Відхилення'
]

for i, metric in enumerate(metrics):
    # Підбираємо правильну кольорову палітру
    if metric == 'Cluster':
        colorscale = 'Turbo'
    elif metric == 'Anomaly':
        colorscale = 'RdBu'
    elif metric == 'GDP':
        colorscale = 'Blues'
    elif metric == 'Corruption':
        colorscale = 'RdYlGn'
    else:
        colorscale = 'Viridis'

    # ДИНАМІЧНИЙ ТЕКСТ ПРИ НАВЕДЕННІ
    # Якщо це кластери - показуємо текстову назву кластера
    if metric == 'Cluster':
        dynamic_value = df['Cluster_Name']
    # Якщо це ВВП - додаємо значок долара для краси
    elif metric == 'GDP':
        dynamic_value = df[metric].astype(int).astype(str) + " $"
    # Для всіх інших цифр просто показуємо число
    else:
        dynamic_value = df[metric].astype(str)

    # Формуємо фінальний текст спливаючої підказки
    hover_text = (
            "<b>" + df['Name'] + "</b><br><br>" +
            "<b>" + metric_names[i] + ":</b> " + dynamic_value + "<br>" +
            "<i>(Кластер: " + df['Cluster_Name'] + ")</i>"  # Залишаємо інфу про кластер для контексту
    )

    # Параметри карти
    trace_args = dict(
        locations=df['Code'],
        z=df[metric],
        text=hover_text,
        hoverinfo="text",
        colorscale=colorscale,
        name=metric_names[i],
        colorbar_title=metric_names[i] if metric != 'Cluster' else "Номер Кластера",
        visible=(i == 0)
    )

    # Для карти аномалій центруємо кольори відносно нуля (білий колір = 0 відхилень)
    if metric == 'Anomaly':
        trace_args['zmid'] = 0

    fig.add_trace(go.Choropleth(**trace_args))

# --- ІНТЕРАКТИВНЕ МЕНЮ ---
buttons = []
for i, name in enumerate(metric_names):
    visibility = [False] * len(metrics)
    visibility[i] = True

    button = dict(
        label=name,
        method="update",
        args=[{"visible": visibility},
              {"title": f"Системний макроаналіз: {name}"}]
    )
    buttons.append(button)
fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.15,
            yanchor="top",
            font=dict(size=14)
        ),
    ],
    title="Глобальний аналіз: Реальна Демократія (Факт)",
    title_x=0.5,
    title_font_size=20,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',  # Виглядає професійніше, ніж просто прямокутник
        landcolor='lightgray',
    ),
    width=1100,
    height=700
)

# 4. Збереження результату
fig.write_html("analysis_dashboard.html")
print("Супер! ML-дашборд згенеровано у файл 'analysis_dashboard.html'")





 #СТВОРЕННЯ ТАБЛИЦІ РЕЗУЛЬТАТІВ КЛАСТЕРИЗАЦІЇ


# 1. Готуємо дані: беремо тільки потрібні колонки і сортуємо за кластерами
table_df = df[['Name', 'Cluster_Name', 'Democracy', 'GDP', 'Corruption', 'Predicted_Democracy', 'Anomaly']].copy()
table_df = table_df.sort_values(by=['Cluster_Name', 'Democracy'], ascending=[True, False])

# 2. Округлюємо ВВП для красивішого вигляду в таблиці
table_df['GDP'] = table_df['GDP'].round(0).astype(int)

# 3. Створюємо фігуру таблиці
fig_table = go.Figure(data=[go.Table(
    # Налаштування заголовків (шапки таблиці)
    header=dict(
        values=["<b>Країна</b>", "<b>Кластер (K-Means)</b>",
                "<b>Індекс Демократії</b>", "<b>ВВП ($)</b>", "<b>Індекс Корупції</b>",
                "<b>Прогнозований Індекс Демократії</b>", "<b>Відхилення</b>"],
        fill_color='royalblue',   # Колір фону шапки
        font=dict(color='white', size=12),
        align='center'
    ),
    # Налаштування клітинок (вмісту)
    cells=dict(
        values=[table_df['Name'], table_df['Cluster_Name'],
                table_df['Democracy'], table_df['GDP'], table_df['Corruption'],
                table_df['Predicted_Democracy'], table_df['Anomaly']],
        fill_color=[['white', 'lightgrey'] * (len(table_df) // 2 + 1)], # Смугастий фон для зручності читання
        align=['left', 'center', 'center', 'center', 'center', 'center', 'center'],
        font=dict(color='black', size=11),
        height=30
    )
)])

# 4. Налаштовуємо загальний вигляд та зберігаємо
fig_table.update_layout(
    title="Таблиця результатів:",
    title_x=0.5,
    height=800, # Висота таблиці
    margin=dict(l=20, r=20, t=50, b=20)
)

fig_table.write_html("cluster_results_table.html")
fig_table.show()
table_df.to_excel("ML_Clusters_Report.xlsx", index=False)

print("Вільний член (b0):", model.intercept_)
print("Коефіцієнти (b1 для ВВП, b2 для Корупції):", model.coef_)