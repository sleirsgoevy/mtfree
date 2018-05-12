# mtfree
Маленький скрипт для автоматической авторизации в Wi-Fi сети Московского Метрополитена.
## Установка
1. Откорректируйте константы в ``mtfreed.sh`` (если нужно)
2. Запустите скрипт ``mtfree.py``
3. Установите дополнение GreaseMonkey
4. Установите UserScript ``mtfree.user.js``
5. Пропишите ``mtfreed.sh`` в автозагрузку
## Описание
``mtfree.user.js`` - скрипт, который автоматизирует процесс входа

``mtfree.py`` - маленький Python враппер над Firefox, который печатает ``ok`` или ``fail`` при успешной или неудачной авторизации

``mtfreed.sh`` - демон, который отслеживает состояние сети и запускает ``mtfree.py`` при подключении к сети ``MF_FREE``
