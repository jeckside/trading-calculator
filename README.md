# Trading Position Calculator

Калькулятор для расчёта размера позиции в трейдинге по зонам.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Возможности

- Расчёт точки входа, стоп-лосса и тейк-профита по зонам
- Поддержка таймфреймов: 1h, 2h, 4h
- Автоматический расчёт размера позиции под заданный риск
- Risk/Reward 1:1.8

## Параметры по таймфреймам

| Таймфрейм | Вход (от верха зоны) | Стоп (от низа зоны) | R:R |
|-----------|----------------------|---------------------|-----|
| 1h | 25% | 6% | 1:1.8 |
| 2h | 22% | 15% | 1:1.8 |
| 4h | 22% | 6% | 1:1.8 |

## Установка и запуск

### Вариант 1: Скачать готовый exe (Windows)

1. Перейди в [Releases](../../releases)
2. Скачай `TradingCalculator.exe`
3. Запусти двойным кликом

### Вариант 2: Запуск из исходников

```bash
# Клонируй репозиторий
git clone https://github.com/YOUR_USERNAME/trading-calculator.git
cd trading-calculator

# Установи зависимости
pip install -r requirements.txt

# Запусти
python calculator.py
```

### Вариант 3: Собрать exe самостоятельно

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "TradingCalculator" calculator.py
```

Готовый exe будет в папке `dist/`

## Как пользоваться

1. Введи **верхнюю границу зоны** (цена)
2. Введи **нижнюю границу зоны** (цена)
3. Выбери **таймфрейм** (1h / 2h / 4h)
4. Введи **депозит** и **риск в %**
5. Нажми **Рассчитать**

Получишь:
- Точку входа
- Стоп-лосс
- Тейк-профит
- Размер позиции
- Риск и потенциальную прибыль в $

## Скриншот

![Trading Calculator](screenshot.png)

## Лицензия

MIT
