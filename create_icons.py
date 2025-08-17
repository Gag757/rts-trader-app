from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Создает иконку заданного размера"""
    # Создаем изображение с градиентным фоном
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Создаем градиент (упрощенная версия)
    for y in range(size):
        # Градиент от #667eea к #764ba2
        r = int(102 + (118 - 102) * y / size)
        g = int(126 + (75 - 126) * y / size)
        b = int(234 + (162 - 234) * y / size)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Добавляем символ графика
    symbol_size = size // 3
    symbol_x = (size - symbol_size) // 2
    symbol_y = (size - symbol_size) // 2
    
    # Рисуем простой график
    points = [
        (symbol_x, symbol_y + symbol_size),
        (symbol_x + symbol_size // 4, symbol_y + symbol_size // 2),
        (symbol_x + symbol_size // 2, symbol_y + symbol_size // 4),
        (symbol_x + 3 * symbol_size // 4, symbol_y + symbol_size // 3),
        (symbol_x + symbol_size, symbol_y)
    ]
    
    # Рисуем линии графика
    draw.line(points, fill=(255, 255, 255, 255), width=max(2, size // 32))
    
    # Добавляем точки на график
    for point in points:
        draw.ellipse([
            point[0] - size // 32, 
            point[1] - size // 32,
            point[0] + size // 32, 
            point[1] + size // 32
        ], fill=(255, 255, 255, 255))
    
    # Сохраняем иконку
    img.save(f'static/{filename}', 'PNG')
    print(f'Создана иконка: {filename} ({size}x{size})')

def main():
    """Создает все необходимые иконки"""
    # Создаем папку static если её нет
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Размеры иконок для PWA
    icon_sizes = [
        (72, 'icon-72x72.png'),
        (96, 'icon-96x96.png'),
        (128, 'icon-128x128.png'),
        (144, 'icon-144x144.png'),
        (152, 'icon-152x152.png'),
        (192, 'icon-192x192.png'),
        (384, 'icon-384x384.png'),
        (512, 'icon-512x512.png')
    ]
    
    for size, filename in icon_sizes:
        create_icon(size, filename)
    
    print('\n✅ Все иконки созданы!')
    print('📱 Теперь ваше приложение готово для установки на iPhone')

if __name__ == '__main__':
    main()

