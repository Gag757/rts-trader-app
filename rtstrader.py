import streamlit as st
import pandas as pd
import datetime as dt
import asyncio
import matplotlib.pyplot as plt
from tinkoff.invest import AsyncClient, CandleInterval
from ta.trend import MACD, SMAIndicator, EMAIndicator, ADXIndicator, CCIIndicator, TRIXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator, ROCIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import VolumeWeightedAveragePrice, OnBalanceVolumeIndicator
import time
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


TOKEN = "t.T3Y_FHopd2AHt6rHo2kG-cDcSe9vxjtXsMwCM3LzpYEZqgEII_dWtUwqjJ1utKZp3H-VgArGbPla-3K95MbteA"
# Будем получать FIGI автоматически
FIGI = None
INTERVAL = CandleInterval.CANDLE_INTERVAL_15_MIN

# Настройка страницы с современным дизайном
st.set_page_config(
    layout="wide", 
    page_title="РТС Трейдер - Технический анализ",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Внедряем CSS для современного дизайна
st.markdown("""
<style>
/* Основные стили */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 0;
}

/* Стили для заголовков */
h1 {
    color: #ffffff !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin-bottom: 2rem !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
}

h2 {
    color: #2c3e50 !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}

h3 {
    color: #34495e !important;
    font-weight: 500 !important;
}

/* Стили для сайдбара */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    border-right: 1px solid #dee2e6;
}

/* Карточки и контейнеры */
.stMetric {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
    border-radius: 15px !important;
    padding: 1rem !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    border: 1px solid #e9ecef !important;
    margin: 0.5rem 0 !important;
}

/* Кнопки */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.5rem 1.5rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Селектбоксы */
.stSelectbox > div > div {
    background: white !important;
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
}

/* Текстовые поля */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 2px solid #e9ecef !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
}

/* Вкладки */
.stTabs > div > div > div > div {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border-radius: 10px 10px 0 0 !important;
}

.stTabs > div > div > div > div > button {
    color: white !important;
    font-weight: 600 !important;
    border-radius: 10px 10px 0 0 !important;
}

/* Сигналы */
.signal-up {
    background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%) !important;
    color: white !important;
    padding: 2rem !important;
    border-radius: 20px !important;
    text-align: center !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(0, 212, 170, 0.4) !important;
    border: 3px solid #00d4aa !important;
    animation: pulse 2s infinite !important;
}

.signal-down {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
    color: white !important;
    padding: 2rem !important;
    border-radius: 20px !important;
    text-align: center !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
    border: 3px solid #ff6b6b !important;
    animation: pulse 2s infinite !important;
}

.signal-neutral {
    background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%) !important;
    color: white !important;
    padding: 2rem !important;
    border-radius: 20px !important;
    text-align: center !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    box-shadow: 0 8px 25px rgba(149, 165, 166, 0.4) !important;
    border: 3px solid #95a5a6 !important;
}

/* Анимация пульсации */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

/* Информационные блоки */
.stAlert {
    border-radius: 15px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}

/* Графики */
.plotly-graph-div {
    border-radius: 15px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    background: white !important;
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
    .main {
        padding: 0.5rem !important;
    }
    
    h1 {
        font-size: 1.5rem !important;
    }
    
    .signal-up, .signal-down, .signal-neutral {
        font-size: 1.5rem !important;
        padding: 1.5rem !important;
    }
    
    .stMetric {
        padding: 0.5rem !important;
    }
    
    .stButton > button {
        padding: 0.4rem 1rem !important;
        font-size: 0.9rem !important;
    }
}

/* Стили для метрик */
.metric-container {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2c3e50;
}

.metric-label {
    font-size: 0.9rem;
    color: #6c757d;
    margin-bottom: 0.5rem;
}

/* Стили для индикаторов */
.indicator-card {
    background: white;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
    transition: all 0.3s ease;
}

.indicator-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.indicator-bullish {
    border-left-color: #00d4aa;
    background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
}

.indicator-bearish {
    border-left-color: #ff6b6b;
    background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
}

/* Стили для статуса */
.status-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 15px;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Стили для времени */
.time-display {
    background: rgba(255,255,255,0.9);
    padding: 0.5rem 1rem;
    border-radius: 25px;
    display: inline-block;
    font-weight: 600;
    color: #2c3e50;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

def generate_demo_data(interval=CandleInterval.CANDLE_INTERVAL_15_MIN):
    """Генерирует демо-данные для показа работы приложения"""
    # Определяем частоту в зависимости от интервала
    if interval == CandleInterval.CANDLE_INTERVAL_5_MIN:
        freq = '5min'
        days = 3
    elif interval == CandleInterval.CANDLE_INTERVAL_15_MIN:
        freq = '15min'
        days = 7
    elif interval == CandleInterval.CANDLE_INTERVAL_30_MIN:
        freq = '30min'
        days = 14
    elif interval == CandleInterval.CANDLE_INTERVAL_HOUR:
        freq = '1h'
        days = 30
    elif interval == CandleInterval.CANDLE_INTERVAL_DAY:
        freq = '1D'
        days = 365
    else:
        freq = '15min'
        days = 7
    
    # Создаем временной ряд
    dates = pd.date_range(start=dt.datetime.now() - dt.timedelta(days=days), 
                         end=dt.datetime.now(), 
                         freq=freq)
    
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

async def get_rts_figi():
    """Получает актуальный FIGI фьючерса РТС или акций РТС"""
    try:
        async with AsyncClient(TOKEN) as client:
            # Сначала пробуем фьючерсы
            instruments = await client.instruments.futures()
            
            for instrument in instruments.instruments:
                if "RTS" in instrument.name.upper() or "РИУ" in instrument.name.upper():
                    return instrument.figi, instrument.name, "futures"
            
            # Если фьючерсы не найдены, пробуем акции
            stocks = await client.instruments.shares()
            
            for stock in stocks.instruments:
                if "RTS" in stock.name.upper() or "РИУ" in stock.name.upper():
                    return stock.figi, stock.name, "shares"
            
            # Если ничего не найдено, пробуем индекс РТС
            etfs = await client.instruments.etfs()
            
            for etf in etfs.instruments:
                if "RTS" in etf.name.upper() or "РИУ" in etf.name.upper():
                    return etf.figi, etf.name, "etf"
            
            return None, None, None
    except Exception as e:
        st.warning(f"⚠️ Не удалось подключиться к API: {e}")
        return None, None, None

async def get_all_futures():
    """Получает список всех доступных фьючерсов"""
    try:
        async with AsyncClient(TOKEN) as client:
            instruments = await client.instruments.futures()
            
            futures_list = []
            for instrument in instruments.instruments:
                # Проверяем, что инструмент активен
                if hasattr(instrument, 'trading_status') and instrument.trading_status == 1:  # 1 = TRADING_STATUS_ACTIVE
                    futures_list.append({
                        'figi': instrument.figi,
                        'name': instrument.name,
                        'ticker': instrument.ticker,
                        'expiration_date': instrument.expiration_date,
                        'lot': instrument.lot,
                        'currency': instrument.currency,
                        'min_price_increment': getattr(instrument, 'min_price_increment', None)
                    })
            
            return futures_list
    except Exception as e:
        st.warning(f"⚠️ Не удалось получить список фьючерсов: {e}")
        return []

async def get_all_shares():
    """Получает список всех доступных акций"""
    try:
        async with AsyncClient(TOKEN) as client:
            stocks = await client.instruments.shares()
            
            shares_list = []
            for stock in stocks.instruments:
                if hasattr(stock, 'trading_status') and stock.trading_status == 1:
                    shares_list.append({
                        'figi': stock.figi,
                        'name': stock.name,
                        'ticker': stock.ticker,
                        'lot': stock.lot,
                        'currency': stock.currency,
                        'min_price_increment': getattr(stock, 'min_price_increment', None)
                    })
            
            return shares_list
    except Exception as e:
        st.warning(f"⚠️ Не удалось получить список акций: {e}")
        return []

async def get_all_etfs():
    """Получает список всех доступных ETF"""
    try:
        async with AsyncClient(TOKEN) as client:
            etfs = await client.instruments.etfs()
            
            etfs_list = []
            for etf in etfs.instruments:
                if hasattr(etf, 'trading_status') and etf.trading_status == 1:
                    etfs_list.append({
                        'figi': etf.figi,
                        'name': etf.name,
                        'ticker': etf.ticker,
                        'lot': etf.lot,
                        'currency': etf.currency,
                        'min_price_increment': getattr(etf, 'min_price_increment', None)
                    })
            
            return etfs_list
    except Exception as e:
        st.warning(f"⚠️ Не удалось получить список ETF: {e}")
        return []

def format_instrument_name(instrument):
    """Форматирует название инструмента для отображения"""
    name = instrument['name']
    ticker = instrument['ticker']
    
    if 'expiration_date' in instrument and instrument['expiration_date']:
        exp_date = instrument['expiration_date'].strftime('%m.%Y')
        return f"{name} ({ticker}) - {exp_date}"
    else:
        return f"{name} ({ticker})"

def create_instrument_selector():
    """Создает интерфейс для выбора инструмента"""
    # Современный заголовок с иконкой
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 15px; color: white; margin-bottom: 1rem;">
        <h3 style="margin: 0; color: white;">📊 Выбор инструмента</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Быстрые кнопки для популярных инструментов
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem;">
        <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">⚡ Быстрый выбор</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Обновить", key="refresh_btn"):
            st.rerun()
    
    with col2:
        if st.button("🎯 Демо", key="demo_btn"):
            return "DEMO", "Фьючерс РТС-12.25 (ДЕМО)", "futures", timeframe_options[selected_timeframe]
    
    # Выбор таймфрейма с современным дизайном
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">⏰ Таймфрейм</h4>
    </div>
    """, unsafe_allow_html=True)
    
    timeframe_options = {
        "5 минут": CandleInterval.CANDLE_INTERVAL_5_MIN,
        "15 минут": CandleInterval.CANDLE_INTERVAL_15_MIN,
        "30 минут": CandleInterval.CANDLE_INTERVAL_30_MIN,
        "1 час": CandleInterval.CANDLE_INTERVAL_HOUR,
        "1 день": CandleInterval.CANDLE_INTERVAL_DAY
    }
    
    selected_timeframe = st.sidebar.selectbox(
        "Выберите таймфрейм:",
        list(timeframe_options.keys()),
        index=1,  # По умолчанию 15 минут
        key="timeframe_select"
    )
    
    # Выбор типа инструмента с современным дизайном
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">📈 Тип инструмента</h4>
    </div>
    """, unsafe_allow_html=True)
    
    instrument_type = st.sidebar.selectbox(
        "Тип инструмента:",
        ["Фьючерсы", "Акции", "ETF"],
        index=0,
        key="instrument_type_select"
    )
    
    # Используем кэширование для получения инструментов
    @st.cache_data(ttl=300)  # кэш на 5 минут
    def get_cached_instruments(instrument_type):
        """Получает инструменты с кэшированием"""
        try:
            if instrument_type == "Фьючерсы":
                return asyncio.run(get_all_futures())
            elif instrument_type == "Акции":
                return asyncio.run(get_all_shares())
            else:  # ETF
                return asyncio.run(get_all_etfs())
        except Exception as e:
            st.sidebar.warning(f"Ошибка загрузки {instrument_type.lower()}: {e}")
            return []
    
    # Получаем список инструментов с красивым спиннером
    with st.spinner(f"🔄 Загрузка {instrument_type.lower()}..."):
        instruments = get_cached_instruments(instrument_type)
    
    if not instruments:
        st.sidebar.markdown("""
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1rem; color: #856404;">
            ⚠️ Не удалось загрузить инструменты
        </div>
        """, unsafe_allow_html=True)
        return None, None, None, timeframe_options[selected_timeframe]
    
    # Показываем количество найденных инструментов
    st.sidebar.markdown(f"""
    <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; padding: 1rem; color: #155724; margin: 1rem 0;">
        ✅ Найдено <strong>{len(instruments)}</strong> активных {instrument_type.lower()}
    </div>
    """, unsafe_allow_html=True)
    
    # Создаем список для выбора
    instrument_options = [format_instrument_name(instr) for instr in instruments]
    
    # Добавляем опцию "Автоматический выбор РТС"
    if instrument_type == "Фьючерсы":
        instrument_options.insert(0, "🔍 Автоматический поиск РТС")
    
    # Поиск по названию с современным дизайном
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">🔍 Поиск инструмента</h4>
    </div>
    """, unsafe_allow_html=True)
    
    search_term = st.sidebar.text_input(
        "Поиск по названию:", 
        placeholder="Введите название или тикер...",
        key="search_input"
    )
    
    # Фильтруем список по поисковому запросу
    if search_term:
        filtered_options = [opt for opt in instrument_options if search_term.upper() in opt.upper()]
        if not filtered_options:
            st.sidebar.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1rem; color: #856404;">
                ⚠️ Инструменты не найдены
            </div>
            """, unsafe_allow_html=True)
            return None, None, None, timeframe_options[selected_timeframe]
        instrument_options = filtered_options
    
    # Выбор конкретного инструмента
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">📋 Выбор инструмента</h4>
    </div>
    """, unsafe_allow_html=True)
    
    selected_option = st.sidebar.selectbox(
        f"Выберите {instrument_type.lower()}:",
        instrument_options,
        index=0,
        key="instrument_select"
    )
    
    if selected_option == "🔍 Автоматический поиск РТС":
        # Ищем РТС среди фьючерсов
        for instr in instruments:
            if "RTS" in instr['name'].upper() or "РИУ" in instr['name'].upper():
                return instr['figi'], instr['name'], "futures"
        st.sidebar.error("РТС не найден в списке")
        return None, None, None, timeframe_options[selected_timeframe]
    else:
        # Находим выбранный инструмент
        for i, option in enumerate(instrument_options):
            if option == selected_option:
                if i == 0 and instrument_type == "Фьючерсы":
                    # Это автоматический поиск РТС
                    continue
                else:
                    selected_instrument = instruments[i - (1 if instrument_type == "Фьючерсы" else 0)]
                    return selected_instrument['figi'], selected_instrument['name'], instrument_type.lower()[:-1], timeframe_options[selected_timeframe]  # убираем 'ы' или 'и'
    
    return None, None, None, timeframe_options[selected_timeframe]

@st.cache_data(ttl=60)
def calculate_indicators(df):
    """Рассчитывает технические индикаторы"""
    try:
        # Трендовые индикаторы
        df['macd'] = MACD(close=df['close']).macd()
        df['macd_signal'] = MACD(close=df['close']).macd_signal()
        df['macd_diff'] = MACD(close=df['close']).macd_diff()
        
        df['sma_20'] = SMAIndicator(close=df['close'], window=20).sma_indicator()
        df['sma_50'] = SMAIndicator(close=df['close'], window=50).sma_indicator()
        df['ema_12'] = EMAIndicator(close=df['close'], window=12).ema_indicator()
        df['ema_26'] = EMAIndicator(close=df['close'], window=26).ema_indicator()
        
        # Моментум индикаторы
        df['rsi'] = RSIIndicator(close=df['close']).rsi()
        df['stoch_k'] = StochasticOscillator(high=df['high'], low=df['low'], close=df['close']).stoch()
        df['stoch_d'] = StochasticOscillator(high=df['high'], low=df['low'], close=df['close']).stoch_signal()
        df['williams_r'] = WilliamsRIndicator(high=df['high'], low=df['low'], close=df['close']).williams_r()
        df['roc'] = ROCIndicator(close=df['close']).roc()
        
        # Волатильность
        bb = BollingerBands(close=df['close'])
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_width'] = bb.bollinger_wband()
        df['bb_percent'] = bb.bollinger_pband()
        
        df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close']).average_true_range()
        
        # Объемные индикаторы
        df['obv'] = OnBalanceVolumeIndicator(close=df['close'], volume=df['volume']).on_balance_volume()
        df['vwap'] = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume']).volume_weighted_average_price()
        
        # Дополнительные трендовые
        df['adx'] = ADXIndicator(high=df['high'], low=df['low'], close=df['close']).adx()
        df['cci'] = CCIIndicator(high=df['high'], low=df['low'], close=df['close']).cci()
        
        # Дополнительные моментум
        df['trix'] = TRIXIndicator(close=df['close']).trix()
        
        return df
    except Exception as e:
        st.error(f"Ошибка при расчете индикаторов: {e}")
        return df

def analyze(df):
    """Анализирует сигналы индикаторов"""
    try:
        last = df.iloc[-1]
        
        # Трендовые сигналы
        macd_signal = last['macd'] > 0
        sma_20_signal = last['close'] > last['sma_20']
        sma_50_signal = last['close'] > last['sma_50']
        ema_12_signal = last['close'] > last['ema_12']
        ema_26_signal = last['close'] > last['ema_26']
        
        # Моментум сигналы
        rsi_signal = last['rsi'] > 55
        stoch_signal = last['stoch_k'] > 50
        williams_signal = last['williams_r'] > -50
        roc_signal = last['roc'] > 0
        
        # Волатильность сигналы
        bb_signal = last['close'] > last['bb_middle']
        bb_percent_signal = last['bb_percent'] > 0.5
        
        # Объемные сигналы
        obv_signal = last['obv'] > df['obv'].iloc[-2] if len(df) > 1 else True
        vwap_signal = last['close'] > last['vwap']
        
        # Дополнительные сигналы
        adx_signal = last['adx'] > 25  # Сильный тренд
        cci_signal = last['cci'] > 0
        trix_signal = last['trix'] > 0
        
        # Подсчитываем голоса
        trend_votes = macd_signal + sma_20_signal + sma_50_signal + ema_12_signal + ema_26_signal
        momentum_votes = rsi_signal + stoch_signal + williams_signal + roc_signal
        volatility_votes = bb_signal + bb_percent_signal
        volume_votes = obv_signal + vwap_signal
        additional_votes = adx_signal + cci_signal + trix_signal
        
        total_votes = trend_votes + momentum_votes + volatility_votes + volume_votes + additional_votes
        max_votes = 15  # Общее количество индикаторов
        
        # Определяем сигнал
        if total_votes >= max_votes * 0.6:  # 60% голосов за рост
            return "UP"
        elif total_votes <= max_votes * 0.4:  # 40% голосов за рост = падение
            return "DOWN"
        else:
            return "NEUTRAL"

    except Exception as e:
        st.error(f"Ошибка при анализе: {e}")
        return "NEUTRAL"

async def get_candles(figi, interval=None):
    """Получает свечи с Tinkoff API"""
    if interval is None:
        interval = INTERVAL
        
    try:
        async with AsyncClient(TOKEN) as client:
            # Используем timezone-aware datetime
            now = dt.datetime.now(dt.timezone.utc)
            # Увеличиваем период до 7 дней для получения большего количества данных
            from_ = now - dt.timedelta(days=7)

            candles = await client.market_data.get_candles(
                figi=figi,
                from_=from_,
                to=now,
                interval=interval
            )
            
            if not candles.candles:
                st.warning("Не получены данные свечей")
                return pd.DataFrame()
                
            df = pd.DataFrame([{
                'time': c.time,
                'open': float(c.open.units) + c.open.nano / 1e9,
                'high': float(c.high.units) + c.high.nano / 1e9,
                'low': float(c.low.units) + c.low.nano / 1e9,
                'close': float(c.close.units) + c.close.nano / 1e9,
                'volume': c.volume
            } for c in candles.candles])
            return df

    except Exception as e:
        st.warning(f"⚠️ Ошибка при получении данных: {e}")
        return pd.DataFrame()

async def get_candles_with_fallback(figi, preferred_interval=None):
    """Получает свечи с fallback на другие интервалы"""
    # Список интервалов для попытки
    if preferred_interval:
        intervals = [preferred_interval]
        # Добавляем другие интервалы как fallback
        all_intervals = [
            CandleInterval.CANDLE_INTERVAL_5_MIN,
            CandleInterval.CANDLE_INTERVAL_15_MIN,
            CandleInterval.CANDLE_INTERVAL_30_MIN,
            CandleInterval.CANDLE_INTERVAL_HOUR,
            CandleInterval.CANDLE_INTERVAL_DAY
        ]
        for interval in all_intervals:
            if interval != preferred_interval:
                intervals.append(interval)
    else:
        intervals = [
            CandleInterval.CANDLE_INTERVAL_5_MIN,
            CandleInterval.CANDLE_INTERVAL_15_MIN,
            CandleInterval.CANDLE_INTERVAL_30_MIN,
            CandleInterval.CANDLE_INTERVAL_HOUR,
            CandleInterval.CANDLE_INTERVAL_DAY
        ]
    
    for interval in intervals:
        df = await get_candles(figi, interval)
        if len(df) >= 20:
            return df, interval
    
    return pd.DataFrame(), None

def plot_chart(df, instrument_type_text="Инструмент", interval_text="15 минутные", is_demo=False):
    """Строит интерактивный график с Plotly"""
    try:
        # Создаем подграфики
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Цена и индикаторы', 'RSI', 'MACD'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Основной график цены
        fig.add_trace(
            go.Scatter(
                x=df['time'], y=df['close'],
                mode='lines',
                name='Цена закрытия',
                line=dict(color='#2E86AB', width=2),
                hovertemplate='<b>Время:</b> %{x}<br><b>Цена:</b> %{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # SMA и EMA
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['sma_20'], mode='lines', name='SMA (20)',
                      line=dict(color='#FF6B6B', width=1, dash='solid')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['sma_50'], mode='lines', name='SMA (50)',
                      line=dict(color='#4ECDC4', width=1, dash='solid')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['ema_12'], mode='lines', name='EMA (12)',
                      line=dict(color='#45B7D1', width=1, dash='dot')),
            row=1, col=1
        )
        
        # Полосы Боллинджера
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['bb_upper'], mode='lines', name='BB Upper',
                      line=dict(color='#95A5A6', width=1, dash='dash'), showlegend=False),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['bb_lower'], mode='lines', name='BB Lower',
                      line=dict(color='#95A5A6', width=1, dash='dash'), showlegend=False),
            row=1, col=1
        )
        
        # Заполнение между полосами Боллинджера
        fig.add_trace(
            go.Scatter(
                x=df['time'].tolist() + df['time'].tolist()[::-1],
                y=df['bb_upper'].tolist() + df['bb_lower'].tolist()[::-1],
                fill='toself',
                fillcolor='rgba(149, 165, 166, 0.1)',
                line=dict(color='rgba(255,255,255,0)'),
                name='BB Zone',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # VWAP
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['vwap'], mode='lines', name='VWAP',
                      line=dict(color='#9B59B6', width=2)),
            row=1, col=1
        )
        
        # RSI
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['rsi'], mode='lines', name='RSI',
                      line=dict(color='#9B59B6', width=2)),
            row=2, col=1
        )
        
        # Уровни RSI
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1,
                     annotation_text="Перекупленность")
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1,
                     annotation_text="Перепроданность")
        fig.add_hline(y=50, line_dash="solid", line_color="gray", row=2, col=1,
                     annotation_text="Нейтраль")
        
        # MACD
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['macd'], mode='lines', name='MACD',
                      line=dict(color='#2E86AB', width=2)),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['macd_signal'], mode='lines', name='Signal',
                      line=dict(color='#FF6B6B', width=2)),
            row=3, col=1
        )
        
        # Гистограмма MACD
        colors = ['#4ECDC4' if val >= 0 else '#FF6B6B' for val in df['macd_diff']]
        fig.add_trace(
            go.Bar(x=df['time'], y=df['macd_diff'], name='Histogram',
                  marker_color=colors, opacity=0.6),
            row=3, col=1
        )
        
        # Нулевая линия для MACD
        fig.add_hline(y=0, line_dash="solid", line_color="black", row=3, col=1)
        
        # Настройка макета
        demo_text = " (ДЕМО)" if is_demo else ""
        fig.update_layout(
            title=f'{instrument_type_text} РТС - {interval_text} свечи{demo_text}',
            title_x=0.5,
            title_font_size=16,
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Настройка осей
        fig.update_xaxes(title_text="Время", row=3, col=1)
        fig.update_yaxes(title_text="Цена", row=1, col=1)
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
        fig.update_yaxes(title_text="MACD", row=3, col=1)
        
        # Отображение графика
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
        
    except Exception as e:
        st.error(f"Ошибка при построении графика: {e}")

def display_signals(df):
    """Отображает сигналы индикаторов с современным дизайном (без кастомного HTML)"""
    try:
        last = df.iloc[-1]
        # Создаем вкладки для разных категорий индикаторов
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Трендовые", "📈 Моментум", "📉 Волатильность", "📊 Объемные"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="MACD",
                    value=f"{last['macd']:.4f}",
                    delta="Покупка" if last['macd'] > 0 else "Продажа",
                    help="Индикатор MACD"
                )
                st.metric(
                    label="SMA (20)",
                    value=f"{last['sma_20']:.2f}",
                    delta="Покупка" if last['close'] > last['sma_20'] else "Продажа",
                    help="SMA 20"
                )
                st.metric(
                    label="EMA (20)",
                    value=f"{last['ema_20']:.2f}",
                    delta="Покупка" if last['close'] > last['ema_20'] else "Продажа",
                    help="EMA 20"
                )
            with col2:
                st.metric(
                    label="ADX",
                    value=f"{last['adx']:.2f}",
                    delta="Сильный тренд" if last['adx'] > 25 else "Слабый тренд",
                    help="ADX"
                )
                st.metric(
                    label="CCI",
                    value=f"{last['cci']:.2f}",
                    delta="Покупка" if last['cci'] > 100 else ("Продажа" if last['cci'] < -100 else "Нейтрально"),
                    help="CCI"
                )
                st.metric(
                    label="TRIX",
                    value=f"{last['trix']:.2f}",
                    delta="Покупка" if last['trix'] > 0 else "Продажа",
                    help="TRIX"
                )

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="RSI",
                    value=f"{last['rsi']:.1f}",
                    delta="Покупка" if last['rsi'] > 55 else "Продажа",
                    help="RSI"
                )
                st.metric(
                    label="Stochastic %K",
                    value=f"{last['stoch_k']:.1f}",
                    delta="Покупка" if last['stoch_k'] > 50 else "Продажа",
                    help="Stochastic %K"
                )
                st.metric(
                    label="Williams %R",
                    value=f"{last['williams_r']:.1f}",
                    delta="Покупка" if last['williams_r'] > -50 else "Продажа",
                    help="Williams %R"
                )
            with col2:
                st.metric(
                    label="ROC",
                    value=f"{last['roc']:.2f}",
                    delta="Покупка" if last['roc'] > 0 else "Продажа",
                    help="ROC"
                )
                st.metric(
                    label="Stochastic %D",
                    value=f"{last['stoch_d']:.1f}",
                    delta="Покупка" if last['stoch_d'] > 50 else "Продажа",
                    help="Stochastic %D"
                )

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Bollinger Bands (BB)",
                    value=f"{last['bb_middle']:.2f}",
                    delta="Верхняя" if last['close'] > last['bb_middle'] else "Нижняя",
                    help="Bollinger Bands Middle"
                )
                st.metric(
                    label="ATR",
                    value=f"{last['atr']:.2f}",
                    delta="Высокая" if last['atr'] > 1 else "Низкая",
                    help="Average True Range"
                )
            with col2:
                st.metric(
                    label="BB High",
                    value=f"{last['bb_upper']:.2f}",
                    delta="Пробой" if last['close'] > last['bb_upper'] else "В пределах",
                    help="Bollinger Bands High"
                )
                st.metric(
                    label="BB Low",
                    value=f"{last['bb_lower']:.2f}",
                    delta="Пробой" if last['close'] < last['bb_lower'] else "В пределах",
                    help="Bollinger Bands Low"
                )

        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="VWAP",
                    value=f"{last['vwap']:.2f}",
                    delta="Выше" if last['close'] > last['vwap'] else "Ниже",
                    help="Volume Weighted Average Price"
                )
                st.metric(
                    label="OBV",
                    value=f"{last['obv']:.2f}",
                    delta="Рост" if last['obv'] > 0 else "Падение",
                    help="On Balance Volume"
                )
            with col2:
                st.metric(
                    label="Объём",
                    value=f"{last['volume']:.0f}",
                    delta="Рост" if last['volume'] > 0 else "Падение",
                    help="Объём торгов"
                )
    except Exception as e:
        st.error(f"Ошибка при отображении сигналов: {e}")

def main():
    """Основная функция приложения с современным дизайном"""
    # Современный заголовок с градиентом
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 20px; color: white; margin-bottom: 2rem; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);">
        <h1 style="margin: 0; color: white; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            💹 РТС Трейдер
        </h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Технический анализ в реальном времени
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Создаем интерфейс выбора инструмента в сайдбаре
    figi, instrument_name, instrument_type, selected_interval = create_instrument_selector()
    
    # Если не удалось получить инструмент через селектор, используем демо-режим
    if not figi:
        st.markdown("""
        <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 15px; padding: 1rem; color: #856404; margin: 1rem 0;">
            🎭 API недоступен. Переключение в демо-режим с тестовыми данными.
        </div>
        """, unsafe_allow_html=True)
        figi = "DEMO"
        instrument_name = "Фьючерс РТС-12.25 (ДЕМО)"
        instrument_type = "futures"
    
    # Информация о текущем инструменте
    instrument_type_text = {
        "futures": "Фьючерс",
        "shares": "Акция", 
        "etf": "ETF"
    }.get(instrument_type, "Инструмент")
    
    demo_text = " (ДЕМО РЕЖИМ)" if figi == "DEMO" else ""
    
    # Отображаем информацию в сайдбаре с современным дизайном
    st.sidebar.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 1rem 0;">
        <h3 style="margin: 0 0 1rem 0; color: #2c3e50; text-align: center;">📈 Текущий инструмент</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Определяем текст таймфрейма
    timeframe_text = "15 минут"
    if selected_interval == CandleInterval.CANDLE_INTERVAL_5_MIN:
        timeframe_text = "5 минут"
    elif selected_interval == CandleInterval.CANDLE_INTERVAL_30_MIN:
        timeframe_text = "30 минут"
    elif selected_interval == CandleInterval.CANDLE_INTERVAL_HOUR:
        timeframe_text = "1 час"
    elif selected_interval == CandleInterval.CANDLE_INTERVAL_DAY:
        timeframe_text = "1 день"
    
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 12px; margin: 1rem 0;">
        <div style="font-weight: 700; margin-bottom: 0.5rem;">{instrument_name}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">
            <div>Тип: {instrument_type_text}</div>
            <div>Таймфрейм: {timeframe_text}</div>
            <div>FIGI: {figi}</div>
            {demo_text}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Отображаем информацию в основном контенте
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 1px solid #dee2e6; border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem;">📊</div>
            <div>
                <div style="font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem;">Анализируемый инструмент</div>
                <div style="color: #6c757d;">{instrument_name} ({instrument_type_text}, таймфрейм: {timeframe_text}, FIGI: {figi}){demo_text}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Получаем данные
    if figi == "DEMO":
        df = generate_demo_data(selected_interval)
        used_interval = selected_interval
        is_demo = True
    else:
        # Используем кэширование для получения данных
        @st.cache_data(ttl=180)  # кэш на 3 минуты
        def get_cached_data(figi, interval):
            """Получает данные с кэшированием"""
            try:
                return asyncio.run(get_candles_with_fallback(figi, interval))
            except Exception as e:
                st.error(f"Ошибка получения данных: {e}")
                return pd.DataFrame(), None
        
        df, used_interval = get_cached_data(figi, selected_interval)
        is_demo = False
    
    if df.empty:
        if figi != "DEMO":
            st.error("Не удалось получить данные. Проверьте токен и FIGI.")
            return
        else:
            st.error("Ошибка генерации демо-данных")
            return
    
    if len(df) < 20:
        st.warning(f"Недостаточно данных для анализа (получено {len(df)} свечей, нужно минимум 20)")
        return

    df = calculate_indicators(df)
    signal = analyze(df)

    # Определяем текст интервала
    interval_text = "15 минутные"
    if used_interval == CandleInterval.CANDLE_INTERVAL_HOUR:
        interval_text = "часовые"
    elif used_interval == CandleInterval.CANDLE_INTERVAL_DAY:
        interval_text = "дневные"

    # Отображаем результаты с современным дизайном
    demo_header = " (ДЕМО)" if is_demo else ""
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #2c3e50; margin-bottom: 1rem;">💹 Сигнал по {instrument_type_text.lower()} РТС ({timeframe_text}){demo_header}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Отображение основного сигнала с анимацией
    if signal == "UP":
        signal_class = "signal-up"
        signal_icon = "📈"
        signal_text = "ВВЕРХ"
    elif signal == "DOWN":
        signal_class = "signal-down"
        signal_icon = "📉"
        signal_text = "ВНИЗ"
    else:
        signal_class = "signal-neutral"
        signal_icon = "😐"
        signal_text = "НЕЙТРАЛЬНО"
    
    st.markdown(f"""
    <div class="{signal_class}">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{signal_icon}</div>
        <div style="font-size: 2.5rem; font-weight: 700;">{signal_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Отображение детальных сигналов
    display_signals(df)
    
    # График
    plot_chart(df, instrument_type_text, timeframe_text, is_demo)
    
    # Статус и время обновления
    st.markdown("""
    <div class="status-container">
        <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">🕐 Статус обновления</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="time-display">
            <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.25rem;">Последнее обновление</div>
            <div style="font-size: 1.1rem; font-weight: 700;">{dt.datetime.now().strftime('%H:%M:%S')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if is_demo:
            st.markdown("""
            <div class="time-display">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.25rem;">Режим</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #ff6b6b;">ДЕМО</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            next_update = dt.datetime.now() + dt.timedelta(minutes=3)
            st.markdown(f"""
            <div class="time-display">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.25rem;">Следующее обновление</div>
                <div style="font-size: 1.1rem; font-weight: 700;">{next_update.strftime('%H:%M:%S')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Кнопки обновления
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Обновить данные", key="refresh_data"):
            st.rerun()
    
    with col2:
        if is_demo:
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1rem; color: #856404; text-align: center;">
                💡 Это демонстрационные данные. Для работы с реальными данными проверьте токен API.
            </div>
            """, unsafe_allow_html=True)

# Запуск Streamlit
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        st.info("Приложение остановлено пользователем")
    except Exception as e:
        st.error(f"Ошибка запуска: {e}")
