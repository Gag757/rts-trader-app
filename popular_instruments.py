"""
Популярные инструменты для быстрого доступа
"""

POPULAR_FUTURES = [
    {
        "name": "Фьючерс на индекс РТС",
        "search_terms": ["RTS", "РИУ", "РТС"],
        "description": "Основной индекс российского рынка"
    },
    {
        "name": "Фьючерс на нефть Brent",
        "search_terms": ["BR", "BRENT", "НЕФТЬ"],
        "description": "Международный эталон нефти"
    },
    {
        "name": "Фьючерс на золото",
        "search_terms": ["GD", "GOLD", "ЗОЛОТО"],
        "description": "Драгоценный металл"
    },
    {
        "name": "Фьючерс на доллар/рубль",
        "search_terms": ["USD", "ДОЛЛАР", "РУБЛЬ"],
        "description": "Валютная пара"
    },
    {
        "name": "Фьючерс на евро/рубль",
        "search_terms": ["EUR", "ЕВРО"],
        "description": "Валютная пара"
    }
]

POPULAR_SHARES = [
    {
        "name": "Сбербанк",
        "search_terms": ["SBER", "СБЕР"],
        "description": "Крупнейший банк России"
    },
    {
        "name": "Газпром",
        "search_terms": ["GAZP", "ГАЗПРОМ"],
        "description": "Газовая компания"
    },
    {
        "name": "Лукойл",
        "search_terms": ["LKOH", "ЛУКОЙЛ"],
        "description": "Нефтяная компания"
    },
    {
        "name": "Яндекс",
        "search_terms": ["YNDX", "ЯНДЕКС"],
        "description": "IT-компания"
    },
    {
        "name": "Магнит",
        "search_terms": ["MGNT", "МАГНИТ"],
        "description": "Розничная сеть"
    }
]

POPULAR_ETFS = [
    {
        "name": "FXRL",
        "search_terms": ["FXRL", "РТС"],
        "description": "ETF на индекс РТС"
    },
    {
        "name": "FXUS",
        "search_terms": ["FXUS", "США"],
        "description": "ETF на американские акции"
    },
    {
        "name": "FXDE",
        "search_terms": ["FXDE", "ГЕРМАНИЯ"],
        "description": "ETF на немецкие акции"
    }
]

def get_popular_instruments():
    """Возвращает все популярные инструменты"""
    return {
        "futures": POPULAR_FUTURES,
        "shares": POPULAR_SHARES,
        "etfs": POPULAR_ETFS
    }

def search_popular_instruments(search_term):
    """Ищет инструменты по поисковому запросу"""
    results = []
    
    for category, instruments in get_popular_instruments().items():
        for instrument in instruments:
            for term in instrument["search_terms"]:
                if search_term.upper() in term.upper():
                    results.append({
                        "category": category,
                        "instrument": instrument
                    })
                    break
    
    return results



