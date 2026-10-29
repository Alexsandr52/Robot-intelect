# robot-move

Рабочий репозиторий проекта [Unitree G1 — подъём коробки и система манипуляции](https://linear.app/aelxsandr/project/unitree-g1-poduyom-korobki-i-sistema-manipulyacii-886951495be0/issues).

Первый результат — воспроизводимый захват, подъём и удержание коробки роботом G1 в симуляции. Дальнейшие этапы включают перенос на реального робота и более общую систему планирования манипуляций. Порядок задач и критерии готовности находятся в Linear; начинать с [AEL-73](https://linear.app/aelxsandr/issue/AEL-73/proverit-konfiguraciyu-g1-i-tekushee-sostoyanie-proekta).

## Структура

- `docs/` — документация проекта и решения по настройке.
- `isaac_sc/` — локальные материалы сцены, не отслеживаемые корневым Git.
- `IsaacLab/` — локальный клон upstream Isaac Lab. Это отдельный репозиторий, не входящий в историю `robot-move`.

Новый код проекта пишем преимущественно на Python. Веса и крупные бинарные файлы отслеживаются через Git LFS; результаты запусков и кэши исключены из Git. Подробности — в [docs/README.md](docs/README.md) и [AGENTS.md](AGENTS.md).
