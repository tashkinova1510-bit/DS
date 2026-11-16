"""Interactive e-commerce analytics dashboard. Run: streamlit run app.py"""
from pathlib import Path
import io
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from analytics import prepare_data, metrics

st.set_page_config(page_title='E-commerce Sales Analytics', page_icon='📊', layout='wide')
st.title('📊 Аналитика продаж интернет-магазина')
st.caption('Интерактивный дашборд · Python · Streamlit · Pandas · Matplotlib')

@st.cache_data(show_spinner=False)
def load_csv(content: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(content))

st.sidebar.header('Источники данных')
st.sidebar.caption('Загрузите три CSV или положите их в папку data/.')
files = {}
for name in ('orders', 'items', 'users'):
    uploaded = st.sidebar.file_uploader(f'{name}.csv', type='csv', key=name)
    if uploaded is not None:
        files[name] = uploaded.getvalue()
    else:
        path = Path(__file__).parent / 'data' / f'{name}.csv'
        if path.exists():
            files[name] = path.read_bytes()

missing = [name for name in ('orders', 'items', 'users') if name not in files]
if missing:
    st.info('Для запуска загрузите CSV: ' + ', '.join(f'{name}.csv' for name in missing) + '.')
    st.stop()
try:
    df, warnings = prepare_data(*(load_csv(files[k]) for k in ('orders', 'items', 'users')))
except (ValueError, pd.errors.ParserError, UnicodeError) as exc:
    st.error(f'Ошибка подготовки данных: {exc}')
    st.stop()

if warnings:
    with st.expander(f'⚠️ Замечания по качеству данных ({len(warnings)})'):
        for message in warnings:
            st.warning(message)

st.sidebar.header('Фильтры')
all_categories = sorted(df['category'].dropna().astype(str).unique().tolist())
chosen = st.sidebar.multiselect('Категории', all_categories, default=all_categories)
valid_dates = df['order_date'].dropna()
if valid_dates.empty:
    st.error('Нет корректных дат заказов для построения дашборда')
    st.stop()
start, end = valid_dates.min().date(), valid_dates.max().date()
selected_dates = st.sidebar.date_input('Период заказов', value=(start, end), min_value=start, max_value=end)
if len(selected_dates) != 2:
    st.info('Выберите начало и конец периода.')
    st.stop()
start_date, end_date = selected_dates
filtered = df.loc[df['category'].isin(chosen) & df['order_date'].dt.date.between(start_date, end_date)].copy()
if filtered.empty:
    st.info('По выбранным фильтрам нет данных. Измените период или категории.')
    st.stop()

m = metrics(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric('Выручка', f"{m['revenue']:,.0f} ₽")
c2.metric('Заказы', f"{m['orders']:,}")
c3.metric('Покупатели', f"{m['users']:,}")
c4.metric('Средний чек (AOV)', f"{m['aov']:,.0f} ₽")
st.caption('Все KPI и графики учитывают выбранные фильтры. Средний чек = сумма выручки / число уникальных заказов.')

tab1, tab2, tab3 = st.tabs(['📈 Визуализация', '🧾 Данные и экспорт', '💡 Выводы'])
with tab1:
    left, right = st.columns(2)
    with left:
        st.subheader('Топ-10 товаров по выручке')
        top = filtered.groupby('item_name', dropna=False)['revenue'].sum().nlargest(10).sort_values()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(top.index.astype(str), top.values)
        ax.set_xlabel('Выручка, ₽')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.subheader('Выручка по категориям')
        cat = filtered.groupby('category')['revenue'].sum().sort_values(ascending=False)
        st.bar_chart(cat)
    left, right = st.columns(2)
    with left:
        st.subheader('Заказы по дням недели')
        days = filtered.groupby('weekday')['order_id'].nunique().reindex(range(7), fill_value=0)
        days.index = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        st.bar_chart(days)
    with right:
        st.subheader('Динамика выручки по дням')
        daily = filtered.groupby(filtered['order_date'].dt.date)['revenue'].sum()
        st.line_chart(daily)
with tab2:
    st.subheader('Данные после фильтрации')
    st.dataframe(filtered, use_container_width=True)
    st.download_button('Скачать CSV', filtered.to_csv(index=False).encode('utf-8-sig'),
                       file_name='filtered_sales_report.csv', mime='text/csv')
with tab3:
    st.subheader('Краткие аналитические выводы')
    top_cat = filtered.groupby('category')['revenue'].sum().idxmax()
    top_item = filtered.groupby('item_name')['revenue'].sum().idxmax()
    st.markdown(f'**Категория с наибольшей выручкой:** {top_cat}.')
    st.markdown(f'**Товар с наибольшей выручкой:** {top_item}.')
    st.markdown(f"**Средний чек:** {m['aov']:,.2f} ₽ при {m['orders']:,} заказах.")
    st.caption('Выводы описательные: причинно-следственные связи по этим графикам не устанавливаются.')

st.divider()
st.caption('Учебный аналитический проект. Для публикации используйте обезличенные данные.')
