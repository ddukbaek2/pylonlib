@echo off
:: #------------------------------------------------------------------------
:: # 단위 테스트 실행. (Windows)
:: #------------------------------------------------------------------------
echo __pyappcore-tests.bat__

rem 가상환경 활성화.
call venv-enable.bat

:: 경로 설정.
call pyappcore-path.bat 

:: 단위 테스트 스크립트 실행.
python "%TESTSPATH%\__main__.py"