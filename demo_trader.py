import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from ta.trend import MACD, SMAIndicator
from ta.momentum import RSIIndicator
import numpy as np

st.set_page_config(layout="wide", page_title="РТС Трейдер - Демо")

def generate_demo_data():
    """Генерирует демо-данные для показа работы приложения"""
    # Создаем временной ряд
    dates = pd.date_range(start=dt.datetime.now() - dt.timedelta(days=7), 
                         end=dt.datetime.now(), 
                         freq='15min')
    
    # Генерируем цены с трендом и шумом
    np.random.seed(42)
    base_price = 1500
    trend = np.linspace(0, 50, len(dates))
    noise = np.random.normal(0, 10, len(dates))
    prices = base_price + trend + noise
    
    # Создаем OHLC данные
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Добавляем небольшой шум для OHLC
        open_price = price + np.random.normal(0, 2)
        high_price = max(open_price, price) + abs(np.random.normal(0, 3))
        low_price = min(open_price, price) - abs(np.random.normal(0, 3))
        close_price = price + np.random.normal(0, 2)
        
        data.append({
            'time': date,
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': np.random.randint(1000, 5000)
        })
    
    return pd.DataFrame(data)

@st.cache_data(ttl=60)
def calculate_indicators(df):
    """Рассчитывает технические индикаторы"""
    try:
        df['macd'] = MACD(close=df['close']).macd()
        df['rsi'] = RSIIndicator(close=df['close']).rsi()
        df['sma'] = SMAIndicator(close=df['close'], window=20).sma_indicator()
        return df
    except Exception as e:
        st.error(f"Ошибка при расчете индикаторов: {e}")
        return df

def analyze(df):
    """Анализирует сигналы индикаторов"""
    try:
        last = df.iloc[-1]
        macd_signal = last['macd'] > 0
        rsi_signal = last['rsi'] > 55
        sma_signal = last['close'] > last['sma']
        vote_sum = macd_signal + rsi_signal + sma_signal

        if vote_sum >= 2:
            return "UP"
        elif vote_sum <= 1:
            return "DOWN"
        else:
            return "NEUTRAL"
    except Exception as e:
        st.error(f"Ошибка при анализе: {e}")
        return "NEUTRAL"

def plot_chart(df, instrument_type_text="Инструмент"):
    """Строит график"""
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        df.plot(x='time', y='close', ax=ax, label='Цена закрытия', linewidth=2)
        df.plot(x='time', y='sma', ax=ax, label='SMA (20)', linewidth=1, alpha=0.7)
        ax.set_title(f'{instrument_type_text} РТС - 15 минутные свечи (ДЕМО)', fontsize=14)
        ax.set_xlabel('Время')
        ax.set_ylabel('Цена')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    except Exception as e:
        st.error(f"Ошибка при построении графика: {e}")

def display_signals(df):
    """Отображает сигналы индикаторов"""
    try:
        last = df.iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            macd_color = "green" if last['macd'] > 0 else "red"
            st.metric("MACD", f"{last['macd']:.4f}", delta_color="normal")
            st.markdown(f"<div style='color:{macd_color}; font-weight:bold;'>📊 MACD: {'ПОКУПКА' if last['macd'] > 0 else 'ПРОДАЖА'}</div>", unsafe_allow_html=True)
        
        with col2:
            rsi_color = "green" if last['rsi'] > 55 else "red"
            st.metric("RSI", f"{last['rsi']:.1f}", delta_color="normal")
            st.markdown(f"<div style='color:{rsi_color}; font-weight:bold;'>📈 RSI: {'ПОКУПКА' if last['rsi'] > 55 else 'ПРОДАЖА'}</div>", unsafe_allow_html=True)
        
        with col3:
            sma_color = "green" if last['close'] > last['sma'] else "red"
            st.metric("SMA", f"{last['sma']:.2f}", delta_color="normal")
            st.markdown(f"<div style='color:{sma_color}; font-weight:bold;'>📉 SMA: {'ПОКУПКА' if last['close'] > last['sma'] else 'ПРОДАЖА'}</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Ошибка при отображении сигналов: {e}")

def main():
    """Основная функция демо-приложения"""
    st.title("💹 РТС Трейдер - Технический анализ (ДЕМО)")
    st.markdown("---")
    
    # Информация о демо-режиме
    st.warning("🎭 Это демо-версия с тестовыми данными. Для работы с реальными данными используйте rtstrader.py")
    
    # Информация о текущем инструменте
    st.info("📊 Анализируемый инструмент: Фьючерс РТС-12.25 (ДЕМО ДАННЫЕ)")
    
    # Генерируем демо-данные
    df = generate_demo_data()
    
    if len(df) < 20:
        st.error("Недостаточно данных для анализа")
        return

    # Рассчитываем индикаторы
    df = calculate_indicators(df)
    signal = analyze(df)

    # Отображаем результаты
    st.subheader("💹 Сигнал по фьючерсу РТС (15м) - ДЕМО")
    
    # Отображение основного сигнала
    color = "green" if signal == "UP" else "red" if signal == "DOWN" else "gray"
    label = "ВВЕРХ 📈" if signal == "UP" else "ВНИЗ 📉" if signal == "DOWN" else "НЕЙТРАЛЬНО 😐"
    st.markdown(f"<h1 style='color:{color}; text-align:center; padding:20px; border:2px solid {color}; border-radius:10px;'>{label}</h1>", unsafe_allow_html=True)
    
    # Отображение детальных сигналов
    display_signals(df)
    
    # График
    plot_chart(df, "Фьючерс")
    
    # Время последнего обновления
    st.markdown(f"🕐 Последнее обновление: {dt.datetime.now().strftime('%H:%M:%S')}")
    
    # Информация о демо-режиме
    st.info("💡 Это демонстрационные данные. В реальном приложении данные обновляются каждые 15 минут.")
    
    # Кнопка для обновления демо-данных
    if st.button("🔄 Обновить демо-данные"):
        st.rerun()

if __name__ == "__main__":
    main()



