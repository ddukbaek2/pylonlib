@echo off
:: #------------------------------------------------------------------------
:: # 프로젝트 소스 실행. (Windows)
:: #------------------------------------------------------------------------

:: 빌드 전 처리 실행.
call pyappcore-prebuild.bat

:: 실행 스크립트 실행.
python "%LAUNCHERFILEPATH%" "%1" "%2" "%3" "%4" "%5" "%6" "%7" "%8" "%9"