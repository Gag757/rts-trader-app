import asyncio
from tinkoff.invest import AsyncClient

TOKEN = "t.T3Y_FHopd2AHt6rHo2kG-cDcSe9vxjtXsMwCM3LzpYEZqgEII_dWtUwqjJ1utKZp3H-VgArGbPla-3K95MbteA"

async def test_instruments():
    """Тестирует доступность различных инструментов"""
    try:
        async with AsyncClient(TOKEN) as client:
            print("🔍 Проверка доступности инструментов...")
            
            # Тест фьючерсов
            try:
                futures = await client.instruments.futures()
                rts_futures = [f for f in futures.instruments if "RTS" in f.name.upper()]
                print(f"✅ Фьючерсы: найдено {len(rts_futures)} инструментов РТС")
                for f in rts_futures[:3]:  # Показываем первые 3
                    print(f"   - {f.name} (FIGI: {f.figi})")
            except Exception as e:
                print(f"❌ Ошибка при получении фьючерсов: {e}")
            
            # Тест акций
            try:
                stocks = await client.instruments.shares()
                rts_stocks = [s for s in stocks.instruments if "RTS" in s.name.upper()]
                print(f"✅ Акции: найдено {len(rts_stocks)} инструментов РТС")
                for s in rts_stocks[:3]:  # Показываем первые 3
                    print(f"   - {s.name} (FIGI: {s.figi})")
            except Exception as e:
                print(f"❌ Ошибка при получении акций: {e}")
            
            # Тест ETF
            try:
                etfs = await client.instruments.etfs()
                rts_etfs = [e for e in etfs.instruments if "RTS" in e.name.upper()]
                print(f"✅ ETF: найдено {len(rts_etfs)} инструментов РТС")
                for e in rts_etfs[:3]:  # Показываем первые 3
                    print(f"   - {e.name} (FIGI: {e.figi})")
            except Exception as e:
                print(f"❌ Ошибка при получении ETF: {e}")
            
            # Тест облигаций
            try:
                bonds = await client.instruments.bonds()
                rts_bonds = [b for b in bonds.instruments if "RTS" in b.name.upper()]
                print(f"✅ Облигации: найдено {len(rts_bonds)} инструментов РТС")
                for b in rts_bonds[:3]:  # Показываем первые 3
                    print(f"   - {b.name} (FIGI: {b.figi})")
            except Exception as e:
                print(f"❌ Ошибка при получении облигаций: {e}")
                
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_instruments())






