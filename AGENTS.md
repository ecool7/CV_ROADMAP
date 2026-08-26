# Agent handoff — CV_ROADMAP

This file is for **any Cursor account** that opens this repo. Read it before planning or writing code.

Repo: https://github.com/ecool7/CV_ROADMAP
Local folder on the student's machine: `CV_ENGINEER` (same project).

## Who

- Student: **hmmml**, software engineer.
- Target job: Junior Computer Vision / Perception Engineer, **Camera + IMU (sensor fusion)**.
- Not in a hurry. Quality over speed.

## Starting level (2026-08-26)

- Python — basic
- NumPy — weak
- Linear algebra — matrices and vectors OK
- IMU development — has real experience (use it, do not reteach IMU hardware)
- Computer Vision — almost zero
- Deep Learning — almost zero
- C++ — not started in this track yet (phase starts week 13)

## Schedule

- Monday–Friday: **max 2 hours**, timer on
- Saturday: **full rest** — no tasks
- Sunday: repetition + one small upgrade + `PROGRESS.md` + push
- Theory: only what is required to write that week's code
- Notebook: student may conspect facts on paper

## Track (42 weeks, ~10–11 months)

| Phase | Weeks | Content |
|---|---|---|
| 1 Foundation | 1–4 | NumPy, SO(3), quaternions/frames, IMU dead reckoning |
| 2 Camera | 5–8 | OpenCV Python, pinhole, calibration, ORB |
| 3 VO | 9–12 | Epipolar, PnP, optical flow, VO + ATE/RPE |
| 4 C++ | 13–20 | C++17, CMake, Eigen, OpenCV C++, small binary |
| 5 Fusion | 21–24 | Attitude filters, EKF, camera–IMU extrinsics |
| 6 Deep Learning | 25–34 | Real PyTorch: train loop, CNN, YOLO, seg, SuperPoint, LightGlue |
| 7 VIO | 35–38 | Toy VIO, EuRoC, eval |
| 8 Job-ready | 39–42 | ROS2 **C++** node, capstone, interview sheet |

Out of scope: C++ template metaprogramming, Boost, GANs, LLMs, diffusion, writing VINS-Mono from scratch.

## How a week is run

1. The only plan for the active week is `weeks/week-XX-*/README.md`.
2. Student works from that file. Mentor does not dump the rest of the roadmap in chat every time.
3. When the student writes **«Неделя N готова»**, deliver **Week N+1** in this exact format:
   - Название недели
   - Цель недели
   - Задачи Пн–Пт (1–2 часа каждая, конкретные файлы)
   - Задание на воскресенье
   - Что должно получиться в Git
4. Put the new week in `weeks/week-XX-.../` with starter files (TODOs, not solutions).
5. Tick/update `PROGRESS.md` (student fills “what was hard”).

## Current state

- **Week 01 started Wednesday 2026-08-26** (short week: Wed–Fri + Sunday).
- Folder: `weeks/week-01-numpy-imu/`
- Env is ready: Python 3.13, `.venv`, numpy, matplotlib. Use `python`, not `py -3`.
- Today’s student task: close TODOs in `src/01_arrays.py` until `ALL PASSED`.
- GitHub remote: `origin` → `https://github.com/ecool7/CV_ROADMAP.git` branch `main`.

### Short week 01 remaining

| Day | Task |
|---|---|
| Wed 26.08 | `01_arrays.py` ALL PASSED |
| Thu 27.08 | `02_linalg.py` ALL PASSED |
| Fri 28.08 | `generate_imu.py` + `03_visualize.py` + `imu_lab.py` → png |
| Sat 29.08 | rest |
| Sun 30.08 | notes + `np.convolve` + PROGRESS + push |

## Mentoring rules

- Speak **Russian** to the student. Function names stay English. Comments and docstrings in `weeks/**` exercise files: **Russian**.
- **Never implement** `TODO` / `NotImplementedError` in week exercises.
- Do not skip to OpenCV, C++, or DL during weeks 1–4.
- Do not start Saturday work.
- After a real study session: `python tools/streak.py log --hours H --note "..."` then the SVG in README updates.
- Commit when the student asks or when a day/week is closed. Never force-push `main`.

## Commands (Windows)

```powershell
.\.venv\Scripts\Activate.ps1
python weeks/week-01-numpy-imu/src/01_arrays.py
python tools/streak.py log --hours 1.5 --note "01_arrays passed"
git add -A
git commit -m "week 01: ..."
git push
```
