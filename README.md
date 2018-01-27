# mtfree
Маленький скрипт для автоматической авторизации в Wi-Fi сети Московского Метрополитена.
## Установка
1. Создайте профиль в FireFox
2. Установите GreaseMonkey
3. Установите UserScript ``mtfree.user.js``
4. Откорректируйте константы в ``mtfree.py`` и ``mtfreed.sh``
5. Установите в ``mtfree.py`` корректный путь к профилю FireFox.
## Описание
``mtfree.user.js`` - скрипт, который автоматизирует процесс входа

``mtfree.py`` - маленький Python враппер над Firefox, который печатает ``ok`` или ``fail`` при успешной или неудачной авторизации

``mtfreed.sh`` - демон, который отслеживает состояние сети и запускает ``mtfree.py`` при подключении к сети ``MF_FREE``