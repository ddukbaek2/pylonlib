@echo off

rem unittest 패키지를 활용한 유닛테스트.

rem .venv\Scripts\activate

python --version
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install --user -r requirements.txt
python -m pip list

python -m unittest discover -s tests