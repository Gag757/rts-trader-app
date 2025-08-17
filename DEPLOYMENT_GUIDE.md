# 📱 Руководство по развертыванию PWA приложения

## Что такое PWA?

**Progressive Web App (PWA)** - это веб-приложение, которое можно установить на iPhone/Android как нативное приложение. Оно работает офлайн, отправляет уведомления и выглядит как обычное приложение.

## 🚀 Быстрый старт

### 1. Развертывание на Streamlit Cloud (Рекомендуется)

1. **Загрузите код на GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/ваш-username/rts-trader.git
   git push -u origin main
   ```

2. **Подключите к Streamlit Cloud:**
   - Зайдите на [share.streamlit.io](https://share.streamlit.io)
   - Войдите через GitHub
   - Нажмите "New app"
   - Выберите репозиторий и файл `rtstrader.py`
   - Нажмите "Deploy"

3. **Получите ссылку:**
   - После деплоя получите ссылку вида: `https://your-app-name.streamlit.app`

### 2. Установка на iPhone

1. **Откройте Safari на iPhone**
2. **Перейдите по ссылке вашего приложения**
3. **Нажмите кнопку "Поделиться" (квадрат со стрелкой)**
4. **Выберите "На экран «Домой»"**
5. **Нажмите "Добавить"**

### 3. Установка на Android

1. **Откройте Chrome на Android**
2. **Перейдите по ссылке приложения**
3. **Появится баннер "Установить приложение"**
4. **Нажмите "Установить"**

## 🔧 Локальная разработка

### Запуск локально:

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
streamlit run rtstrader.py
```

### Тестирование PWA:

1. Откройте браузер
2. Нажмите F12 (Developer Tools)
3. Перейдите на вкладку "Application"
4. Проверьте разделы:
   - Manifest
   - Service Workers
   - Storage

## 📁 Структура файлов

```
rts-trader/
├── rtstrader.py          # Основное приложение
├── manifest.json         # PWA манифест
├── sw.js                # Service Worker
├── static/              # Статические файлы
│   ├── icon-72x72.png
│   ├── icon-96x96.png
│   ├── icon-128x128.png
│   ├── icon-144x144.png
│   ├── icon-152x152.png
│   ├── icon-192x192.png
│   ├── icon-384x384.png
│   └── icon-512x512.png
├── requirements.txt      # Зависимости Python
└── README.md            # Документация
```

## 🎨 Создание иконок

### Автоматическое создание:

```bash
# Установите Pillow
pip install Pillow

# Создайте иконки
python create_icons.py
```

### Ручное создание:

1. Создайте изображение 512x512 пикселей
2. Используйте онлайн-генератор: [PWA Builder](https://www.pwabuilder.com/imageGenerator)
3. Скачайте все размеры иконок
4. Поместите в папку `static/`

## ⚙️ Настройка HTTPS

PWA требует HTTPS для работы. Streamlit Cloud предоставляет его автоматически.

### Для локальной разработки:

```bash
# Установите mkcert
pip install mkcert

# Создайте локальный сертификат
mkcert -install
mkcert localhost

# Запустите с HTTPS
streamlit run rtstrader.py --server.sslCertFile=localhost.pem --server.sslKeyFile=localhost-key.pem
```

## 🔔 Push-уведомления

Для отправки уведомлений нужно настроить серверную часть:

```python
# Пример отправки уведомления
import requests

def send_notification(title, body, icon="/static/icon-192x192.png"):
    # Здесь код для отправки push-уведомлений
    pass
```

## 📱 Функции PWA

✅ **Установка на главный экран**  
✅ **Офлайн работа**  
✅ **Push-уведомления**  
✅ **Нативный интерфейс**  
✅ **Быстрая загрузка**  
✅ **Автообновление**

## 🐛 Отладка

### Проверка PWA:

1. Откройте [Lighthouse](https://developers.google.com/web/tools/lighthouse)
2. Запустите аудит PWA
3. Исправьте найденные проблемы

### Логи Service Worker:

1. Откройте Developer Tools
2. Перейдите на вкладку "Application"
3. Выберите "Service Workers"
4. Проверьте логи

## 📊 Аналитика

Добавьте Google Analytics для отслеживания использования:

```html
<!-- Добавьте в rtstrader.py -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🚀 Оптимизация производительности

1. **Сжатие изображений**
2. **Минификация CSS/JS**
3. **Кэширование данных**
4. **Ленивая загрузка**

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте консоль браузера на ошибки
2. Убедитесь, что все файлы загружаются
3. Проверьте HTTPS соединение
4. Очистите кэш браузера

## 🎉 Готово!

Теперь ваше приложение работает как нативное на iPhone и Android! 🎊

