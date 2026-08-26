# Неделя 1 — NumPy: IMU как массивы

## Цель недели

Научиться держать IMU-сигнал как массив NumPy `(N, 3)`: индекс, маска, норма, матричное умножение, график. Без циклов `for` по отсчётам.

Теория — только то, что нужно, чтобы понять `shape`, broadcasting и `matmul`. Computer Vision на этой неделе нет.

## Короткая неделя (старт со среды 26.08)

Пн–вт уже прошли — не догоняем их отдельно. Цель недели та же, дни сжаты. Таймер 1–2 часа, остановись по звонку.

| День | Что сделать | Готово когда |
|---|---|---|
| **Ср (сегодня)** | venv + `01_arrays.py` | `check_env.py` → `env: OK`, `01_arrays.py` → `ALL PASSED` |
| **Чт** | `02_linalg.py` | `ALL PASSED` |
| **Пт** | `generate_imu.py` + `03_visualize.py` + ядро `imu_lab.py` | есть `imu_raw.png` и `imu_lab.png` |
| **Сб** | отдых | — |
| **Вс** | конспект + moving average + `PROGRESS.md` + git | `imu_lab_smoothed.png` запушен |

GitHub можно завести в воскресенье, если сегодня время уйдёт на NumPy. Среда важнее кода, чем репозитория.

---

## Задачи по дням (полный вариант Пн–Пт, если начнёшь с понедельника)

### Понедельник — среда и репозиторий

1. Поставь Python 3.11+ если его нет: https://www.python.org/downloads/ (галочка **Add python.exe to PATH**).
2. В корне проекта (папка `CV_ENGINEER`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python weeks/week-01-numpy-imu/src/check_env.py
```

Если PowerShell ругается на скрипты: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

3. Создай репозиторий на GitHub (Public), затем:

```powershell
git init
git add README.md PROGRESS.md requirements.txt .gitignore weeks
git commit -m "week 01: repo skeleton and numpy env"
git branch -M main
git remote add origin https://github.com/<you>/cv-perception.git
git push -u origin main
```

Готово, когда `check_env.py` печатает версии numpy/matplotlib и нет ошибок.

Конспект (5 минут): что такое virtualenv и зачем он нужен.

---

### Вторник — массивы NumPy

Открой `src/01_arrays.py`. Закрой все `TODO`. Запусти:

```powershell
python weeks/week-01-numpy-imu/src/01_arrays.py
```

Должно напечатать `01_arrays: ALL PASSED`.

Читать только это (не весь учебник):
- https://numpy.org/doc/stable/user/absolute_beginners.html
  разделы: create arrays, indexing, slicing, `shape`

Конспект: чем `shape (N, 3)` отличается от трёх списков `ax, ay, az`.

Запрещено: `for i in range(len(accel))`. Если хочется цикл — ищи numpy-операцию.

---

### Среда — линейная алгебра в NumPy

Файл `src/02_linalg.py`. Снова все `TODO` + `ALL PASSED`.

Ты уже знаешь матрицы. Сегодня это те же вещи в коде:

- `np.dot` / `@` / `np.matmul`
- норма вектора (`np.linalg.norm`)
- поворот вектора матрицей `R @ v`
- broadcasting: вычесть среднее по осям из всей записи

Конспект: формула `v' = R v` и почему в NumPy пишут `R @ accel.T` или `accel @ R.T`.

---

### Четверг — графики

1. Сгенерируй учебный CSV (один раз):

```powershell
python weeks/week-01-numpy-imu/src/generate_imu.py
```

Появится `data/synthetic_imu.csv` (100 Гц, 12 секунд, участки «стоит / разгон / едет / торможение / стоит»).

2. Закрой `TODO` в `src/03_visualize.py`. Запусти. В `outputs/` должен появиться `imu_raw.png`: три оси accel + magnitude.

Конспект: как по magnitude отличить покой от движения, если в покое есть сила тяжести.

---

### Пятница — лаборатория (главный артефакт недели)

Файл `src/imu_lab.py`. Это то, что пойдёт в GitHub как «я умею».

Скрипт должен:

1. Загрузить CSV.
2. Посчитать magnitude.
3. Оценить g по медиане magnitude на первой секунде (там покой).
4. Пометить `moving`, если `|magnitude - g| > порог` (подбери порог, начни с `0.3`).
5. Сохранить `outputs/imu_lab.png` (сигнал + маска) и напечатать: сколько секунд moving, mean/std magnitude.

Не пиши нейросети, фильтры Калмана и OpenCV. Только NumPy + matplotlib.

---

## Воскресенье — повтор + улучшение

Суббота — отдых, файлы не трогать.

1. В тетради, не глядя в код, напиши 5 пунктов:
   - что такое `shape` и `dtype`
   - что делает broadcasting
   - как посчитать magnitude трёхосного accel одной строкой
   - зачем `R @ v`
   - почему интеграл IMU без камеры уплывает (интуиция, формул много не надо)
2. Улучшение (~40 мин): в `imu_lab.py` добавь скользящее среднее magnitude через `np.convolve` (окно 10 сэмплов). Нарисуй сырой и сглаженный сигнал на одном графике. Сохрани `outputs/imu_lab_smoothed.png`.
3. Заполни блок Week 01 в `PROGRESS.md`.
4. Коммит и пуш:

```powershell
git add weeks/week-01-numpy-imu PROGRESS.md
git commit -m "week 01: numpy IMU lab with still/moving mask"
git push
```

---

## Что должно получиться в Git к концу недели

```
weeks/week-01-numpy-imu/
  README.md                 ← этот план
  data/synthetic_imu.csv    ← сгенерированные данные
  outputs/imu_raw.png
  outputs/imu_lab.png
  outputs/imu_lab_smoothed.png
  src/check_env.py
  src/generate_imu.py
  src/01_arrays.py          ← без TODO, все тесты зелёные
  src/02_linalg.py
  src/03_visualize.py
  src/imu_lab.py            ← лаборатория + moving average
PROGRESS.md                 ← галочки и 3 коротких поля
```

Если что-то не успел в будни — доделывай в воскресенье, не переноси на следующую неделю.

Когда закончишь, напиши: «Неделя 1 готова» и прикрепи скрин `imu_lab.png` или вставь 3 строки из `PROGRESS.md`.
