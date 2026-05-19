@echo off
chcp 65001 >nul
call .venv\Scripts\activate
python run_web.py
pause
