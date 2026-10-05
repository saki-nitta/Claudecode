@echo off
chcp 65001 >nul
python "%~dp0pdf_lock.py" %*
