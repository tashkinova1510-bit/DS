"""Data validation and KPI calculations for the Streamlit sales dashboard."""
from __future__ import annotations
import pandas as pd

REQUIRED = {
    'orders': {'order_id', 'user_id', 'item_id', 'order_date', 'quantity', 'price_per_unit'},
    'items': {'item_id', 'item_name', 'category'},
    'users': {'user_id', 'city', 'registration_date'},
}


def prepare_data(orders: pd.DataFrame, items: pd.DataFrame, users: pd.DataFrame):
    """Return prepared order-line data and validation warnings.

    Assumes each row in orders represents one order line, items and users are
    dimension tables, and price_per_unit is the price applicable to that line.
    """
    frames = {'orders': orders.copy(), 'items': items.copy(), 'users': users.copy()}
    warnings = []
    for name, frame in frames.items():
        missing = REQUIRED[name] - set(frame.columns)
        if missing:
            raise ValueError(f"{name}.csv: отсутствуют столбцы: {', '.join(sorted(missing))}")
    orders, items, users = (frames[k] for k in ('orders', 'items', 'users'))
    for name, frame, key in [('items', items, 'item_id'), ('users', users, 'user_id')]:
        if frame[key].isna().any() or frame[key].duplicated().any():
            raise ValueError(f'{name}.csv: ключ {key} должен быть уникальным и непустым')
    if orders[['order_id', 'user_id', 'item_id']].isna().any().any():
        raise ValueError('orders.csv: обязательные идентификаторы не могут быть пустыми')
    if orders.empty:
        raise ValueError('orders.csv не содержит строк')
    df = orders.merge(users, on='user_id', how='left', validate='many_to_one', indicator='_user_match')
    unmatched_users = int((df['_user_match'] == 'left_only').sum())
    df = df.drop(columns='_user_match').merge(items, on='item_id', how='left', validate='many_to_one', indicator='_item_match')
    unmatched_items = int((df['_item_match'] == 'left_only').sum())
    df = df.drop(columns='_item_match')
    if unmatched_users:
        warnings.append(f'Заказов с неизвестным пользователем: {unmatched_users}')
    if unmatched_items:
        warnings.append(f'Строк заказов с неизвестным товаром: {unmatched_items}')
    for col in ('order_date', 'registration_date'):
        df[col] = pd.to_datetime(df[col], errors='coerce')
        bad = int(df[col].isna().sum())
        if bad:
            warnings.append(f'Некорректных/пустых значений {col}: {bad}')
    for col in ('quantity', 'price_per_unit'):
        df[col] = pd.to_numeric(df[col], errors='coerce')
        bad = int(df[col].isna().sum())
        if bad:
            warnings.append(f'Некорректных/пустых значений {col}: {bad}; выручка не рассчитана для этих строк')
    negative = int(((df['quantity'] < 0) | (df['price_per_unit'] < 0)).sum())
    if negative:
        warnings.append(f'Строк с отрицательным количеством или ценой: {negative}; проверьте возвраты и корректировки')
    df['category'] = df['category'].fillna('Неизвестная категория')
    df['item_name'] = df['item_name'].fillna('Неизвестный товар')
    df['city'] = df['city'].fillna('Неизвестный город')
    df['revenue'] = df['quantity'] * df['price_per_unit']
    df['weekday'] = df['order_date'].dt.dayofweek
    return df, warnings


def metrics(df: pd.DataFrame) -> dict:
    revenue = float(df['revenue'].sum())
    orders = int(df['order_id'].nunique())
    users = int(df['user_id'].nunique())
    return {'revenue': revenue, 'orders': orders, 'users': users,
            'aov': revenue / orders if orders else 0.0,
            'items_sold': float(df['quantity'].sum())}
