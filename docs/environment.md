# Окружения для экспериментов

На 2026-10-29 выбран стек **Python 3.12 + Isaac Sim 6.2.0 + Isaac Lab 3.0.0 + Isaac Lab-Arena main**. Arena `main` в закреплённом коммите указывает совместимость именно этой пары Lab/Sim. LeRobot используется в отдельном uv-окружении: его зависимости и среда симуляции MuJoCo отделены от Isaac Sim.

## Зафиксированные исходники

| Компонент | Ревизия / версия | Источник фиксации |
| --- | --- | --- |
| uv | `0.13.6` | `uv --version` на рабочей станции |
| Python | `3.12.16` (uv-managed CPython) | `uv python find 3.12` на рабочей станции |
| ОС / ядро | Ubuntu `24.04.5 LTS`, kernel `7.0.0-38-generic` | Снимок рабочей станции на 2026-10-29 |
| GPU / драйвер | NVIDIA RTX 5090, driver `595.99.02`, 32 GiB VRAM | `nvidia-smi`; перед симуляцией проверять доступную VRAM |
| Isaac Lab-Arena | `233754e5b8ba2875f90f31e3736cb4aecd945d52` | [коммит Arena](https://github.com/isaac-sim/IsaacLab-Arena/commit/233754e5b8ba2875f90f31e3736cb4aecd945d52) |
| Isaac Lab (подмодуль Arena) | `e3f7d9ff1f5d7f8280de3ece9000b7117f66bcf4` | Gitlink в указанном коммите Arena |
| Isaac-GR00T (подмодуль Arena) | `e29d8fc50b0e4745120ae3fb72447986fe638aa6` | Gitlink в указанном коммите Arena |
| Isaac Sim | `6.2.0.0` | `isaacsim` extra и `uv.lock` Arena |
| Arena `uv.lock` | SHA-256 `e446e6dc91539d657637c3bb2023c371d8b0a7490c3ece358854502ff330e6aa` | Снимок в [`docs/locks/arena-uv.lock`](locks/arena-uv.lock); добавлена отсутствовавшая запись `onnxruntime-gpu` для `gr00t-client` |
| LeRobot | `72e1d9e5e76ee719bacfc78bc34d817bee5fb521` | [коммит LeRobot](https://github.com/huggingface/lerobot/commit/72e1d9e5e76ee719bacfc78bc34d817bee5fb521) |
| LeRobot `uv.lock` | SHA-256 `7829d3350a9dd9e0832c441e5eeb44b0b71809232b2679218da6007600d67d02` | Снимок в [`docs/locks/lerobot-uv.lock`](locks/lerobot-uv.lock) и закреплённом коммите LeRobot |

Клон `IsaacLab/` на рабочей станции имеет `VERSION=3.0.0`, но его SHA `0ca25c56eec6fe7860fdcba44f8848f19693d6f6` отличается от Lab-подмодуля Arena. Для экспериментов с Arena использовать её закреплённый подмодуль, а существующий клон оставить отдельным.

## Isaac Sim, Isaac Lab и Arena

Выполнить из корня репозитория:

```bash
git clone https://github.com/isaac-sim/IsaacLab-Arena.git IsaacLab-Arena
git -C IsaacLab-Arena checkout 233754e5b8ba2875f90f31e3736cb4aecd945d52
git -C IsaacLab-Arena config submodule.submodules/IsaacLab.url https://github.com/isaac-sim/IsaacLab.git
git -C IsaacLab-Arena config submodule.submodules/Isaac-GR00T.url https://github.com/NVIDIA/Isaac-GR00T.git
GIT_LFS_SKIP_SMUDGE=1 git -C IsaacLab-Arena submodule update --init
cp docs/locks/arena-uv.lock IsaacLab-Arena/uv.lock
cd IsaacLab-Arena
uv python pin 3.12.16
uv venv --python 3.12.16
uv pip install --python .venv/bin/python cmake==4.1.2
PATH="$PWD/.venv/bin:$PATH" uv sync --locked --no-build-isolation-package egl-probe
```

Закреплённый Arena commit содержит lock-файл, который `uv 0.13.6` считает неполным для optional `gr00t-client`: отсутствует запись `onnxruntime-gpu`. В `docs/locks/arena-uv.lock` лежит минимально обновлённый lock; именно он проходит `uv sync --locked`. Для сборки `egl-probe` требуется CMake: установка закреплена на `4.1.2`, а сборка этого пакета идёт без изоляции, чтобы видеть CMake в проектном окружении. `pyproject.toml` фиксирует Python-пакеты, Isaac Sim и настройки разрешения зависимостей. Gitlinks фиксируют точные Isaac Lab и Isaac-GR00T. Вложенные репозитории GR00T не инициализируются: они нужны отдельным policy clients, которых нет в текущем стеке. `GIT_LFS_SKIP_SMUDGE=1` оставляет крупные файлы LFS как указатели, не загружая веса и демонстрации заранее. Не обновлять ревизии и lock-файл посреди серии экспериментов.

Для каждого запуска принимать лицензию Isaac Sim в текущем процессе и использовать тот же lock:

```bash
OMNI_KIT_ACCEPT_EULA=YES ACCEPT_EULA=Y uv run --locked python -c "import isaaclab, isaacsim; print('Isaac Lab and Isaac Sim import OK')"
```

Перед запуском симуляции проверить свободную видеопамять. Не останавливать чужие GPU-процессы.

## LeRobot и Unitree G1

Окружение LeRobot изолировано от Arena. Для него использовать отдельный клон и его зафиксированный `uv.lock`:

```bash
git clone https://github.com/huggingface/lerobot.git LeRobot
git -C LeRobot checkout 72e1d9e5e76ee719bacfc78bc34d817bee5fb521
cp docs/locks/lerobot-uv.lock LeRobot/uv.lock
cd LeRobot
uv python pin 3.12.16
uv sync --locked --extra unitree_g1
uv run --locked --extra unitree_g1 python -c "from lerobot.robots.unitree_g1 import UnitreeG1Config; print(UnitreeG1Config(embodiment='g1_29', end_effector='dex3'))"
```

LeRobot `unitree_g1` extra не включает пакет Unitree SDK2 Python: он нужен при подключении к физическому G1. Версию SDK устанавливать отдельно по инструкции LeRobot; не добавлять её в Isaac Lab/Arena environment.

## Что проверено и что осталось

- На рабочей станции уже есть Python `3.12.16`, uv `0.13.6`, Isaac Sim `6.2.0.0` и пакеты Isaac Lab; текущий Isaac Lab clone не совпадает по SHA с Arena submodule.
- Arena main заявляет совместимость Isaac Lab `3.0.0` / Isaac Sim `6.2.0` и предоставляет native uv lock.
- LeRobot G1 поддерживает `g1_29` и параметр `end_effector='dex3'`; его физическое управление кистями требует отдельной интеграционной проверки.
- Полные установки `uv sync --locked` выполняются; после их завершения запустить обе команды smoke-import выше. Isaac Sim GUI/simulation launch проводить после проверки доступной GPU-памяти.
