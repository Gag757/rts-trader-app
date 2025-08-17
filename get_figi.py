import asyncio
from tinkoff.invest import AsyncClient, InstrumentIdType

TOKEN = "t.T3Y_FHopd2AHt6rHo2kG-cDcSe9vxjtXsMwCM3LzpYEZqgEII_dWtUwqjJ1utKZp3H-VgArGbPla-3K95MbteA"

async def get_rts_futures():
    """Получает список фьючерсов РТС"""
    try:
        async with AsyncClient(TOKEN) as client:
            # Ищем фьючерсы РТС
            instruments = await client.instruments.futures()
            
            rts_futures = []
            for instrument in instruments.instruments:
                if "RTS" in instrument.name.upper() or "РИУ" in instrument.name.upper():
                    rts_futures.append({
                        'name': instrument.name,
                        'figi': instrument.figi,
                        'ticker': instrument.ticker,
                        'expiration_date': instrument.expiration_date,
                        'lot': instrument.lot,
                        'currency': instrument.currency
                    })
            
            return rts_futures
            
    except Exception as e:
        print(f"Ошибка при получении фьючерсов: {e}")
        return []

async def main():
    print("🔍 Поиск фьючерсов РТС...")
    futures = await get_rts_futures()
    
    if futures:
        print("\n📊 Найденные фьючерсы РТС:")
        print("-" * 80)
        for i, future in enumerate(futures, 1):
            print(f"{i}. {future['name']}")
            print(f"   FIGI: {future['figi']}")
            print(f"   Тикер: {future['ticker']}")
            print(f"   Дата экспирации: {future['expiration_date']}")
            print(f"   Лот: {future['lot']}")
            print(f"   Валюта: {future['currency']}")
            print("-" * 80)
        
        # Рекомендуем ближайший активный фьючерс
        active_futures = [f for f in futures if f['expiration_date'] is not None]
        if active_futures:
            # Сортируем по дате экспирации
            active_futures.sort(key=lambda x: x['expiration_date'])
            recommended = active_futures[0]
            print(f"\n✅ Рекомендуемый FIGI для использования: {recommended['figi']}")
            print(f"   Инструмент: {recommended['name']}")
    else:
        print("❌ Фьючерсы РТС не найдены")

if __name__ == "__main__":
    asyncio.run(main())
