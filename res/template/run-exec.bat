@echo off
:: #------------------------------------------------------------------------
:: # 빌드 된 바이너리 파일 실행. (Windows)
:: #------------------------------------------------------------------------

:: 한글 출력 설정.
chcp 65001 >nul 2>nul

:: 경로 설정.
call pyappcore-path.bat

:: 빌드 된 바이너리 파일 실행.
if exist "%BUILDFILEPATH%" (
    "%BUILDFILEPATH%" "all"
) else (
    echo "'%BUILDFILEPATH%' 파일이 존재하지 않습니다."
)

pause