#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union
import builtins
import debugpy # type: ignore
import importlib
import os
import sys
import application
from .application import Application
import str_util



#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
FROZEN : str = "frozen"
MAIN : str = "__main__"


#------------------------------------------------------------------------
# 시작.
#------------------------------------------------------------------------
def Launching() -> int:
	builtins.print("pyappcore.launcher.Launch()")

	# 실행 환경 체크.
	try:
		isBuild : bool = builtins.getattr(sys, FROZEN, False)
	except Exception as exception:
		isBuild : bool = False

	# 빌드인 경우 경로.
	if isBuild:
		# 실행파일에서 생성되는 임시 루트 경로.
		# 리소스를 위한 캐시폴더로 실제 실행파일의 위치가 아님.
		launcherPath : str = str()
		cachePath : str = sys._MEIPASS
		rootPath : str = os.path.dirname(sys.executable)
		sourcePath : str = os.path.join(cachePath, "src")
		resPath : str = os.path.join(cachePath, "res")
		testPath : str = str() # 빌드시 제외.
	# 빌드가 아닌 경우 경로.
	else:
		# 현재 프로젝트를 기준으로 한 경로.
		launcherPath : str = os.path.dirname(os.path.abspath(sys.modules[MAIN].__file__))
		rootPath : str = os.path.dirname(launcherPath)
		sourcePath : str = os.path.join(rootPath, "src")
		resPath : str = os.path.join(rootPath, "res")
		testPath : str = os.path.join(rootPath, "tests")

	# 런처 및 소스 폴더 추가.
	if sourcePath and sourcePath not in sys.path: sys.path.append(sourcePath)
	if testPath and testPath not in sys.path: sys.path.append(testPath)
	if launcherPath and launcherPath not in sys.path: sys.path.append(launcherPath)

	# 프로젝트 값 설정.
	Application._Application__SetBuild(isBuild)
	Application._Application__SetRootPath(rootPath)
	Application._Application__SetResPath(resPath)

	# 프로젝트 값 출력.
	builtins.print(f"Application.IsBuild(): {Application.IsBuild()}")  
	builtins.print(f"Application.GetRootPath(): {Application.GetRootPath()}")
	builtins.print(f"Application.GetResPath(): {Application.GetResPath()}")

	# 시도.
	try:
		# 실행파일 빌드.
		if Application.IsBuild():
			# 실행된 파일 이름 설정.
			Application._Application__SetExecuteFileName(sys.argv[0])
			sys.argv = sys.argv[1:]

			# 심볼 설정.
			# import __include_in_build__ # type: ignore
			# import __symbols_in_build__ # type: ignore
			# symbols = __symbols_in_build__.SYMBOLS
			symbols : str = ""
			Application._Application__SetSymbols(symbols) # 심볼 설정.

			# 디버그 모드 설정.
			Application._Application__SetDebug(False) # 빌드는 DEBUG 심볼이 있던 없던 무조건 False.
			builtins.print(f"Application.IsDebug() : {Application.IsDebug()}")

		# 빌드 외.
		else:
			# PYCHARM.
			# MANUAL.
			# 둘은 일단 상황 제외.

			# VSCODE.
			# run.bat을 통한 실행일 경우 최대 9개의 미사용 인수가 넘어오므로.
			# 빈 문자열들은 안쓰는 값으로 간주하고 제거.
			sys.argv = sys.argv[3:]
			sys.argv = [argument for argument in sys.argv if argument]

			# 실행된 파이썬 스크립트 파일 설정.
			Application._Application__SetExecuteFileName(sys.argv[0])
			sys.argv = sys.argv[1:]

			# 심볼 설정.
			symbols = sys.argv[0]
			Application._Application__SetSymbols(symbols)
			sys.argv = sys.argv[1:]

			# 디버그 모드 설정.
			useDebug : bool = Application.HasSymbol(application.PYAPPCORE_SYMBOL_DEBUG)
			Application._Application__SetDebug(useDebug)
			builtins.print(f"Application.IsDebug() : {Application.IsDebug()}")

			# 디버그 모드 일 경우 원격 디버거 실행.
			# 콘솔에 출력되는 해당 문자열을 감지해서 디버그 대기와 시작을 판단하므로 수정금지.
			if Application.IsDebug():
				builtins.print("PYAPPCORE.DEBUGPY.START")
				remotePort : int = 4885 # vscodeSettings["launcher"]["debug"]["remotePort"]
				debugpy.listen(("localhost", remotePort))
				builtins.print("PYAPPCORE.DEBUGPY.WAIT")
				debugpy.wait_for_client()
				builtins.print("PYAPPCORE.DEBUGPY.STARTED")

		# 공통.
		# 인자 재조립 처리.
		# VSCODE 상황일때의 인자 목록은 문자열 리스트가 아닌 콤마로 합쳐진 형태로 넘어올 수 있음.
		# 어찌 되었건 쉼표 또한 구분자로 인정하고 공통 처리.
		if not Application.IsBuild() and sys.argv:
			sys.argv = str_util.CreateStringListFromSeperatedStringLists(sys.argv)	

		# 인자 출력.
		builtins.print("sys.argv")
		if sys.argv:
			index = 0
			for arg in sys.argv:
				builtins.print(f" - [{index}] {arg}")
				index += 1

		# 로그 설정.
		# 순서 : DEBUG < INFO < WARNING < ERROR < CRITICAL.
		useLog : bool = Application.HasSymbol(application.PYAPPCORE_SYMBOL_LOG)
		if useLog:
			pass

	# 예외.
	except Exception as exception:
		builtins.print(exception)
		return 1
		
	# 시작.
	try:
		moduleName : str = "main"
		functionName : str = "Main"
		module = importlib.import_module(moduleName)
		function = builtins.getattr(module, functionName)
		exitCode : int = function(sys.argv)
		return exitCode
	# 예외.
	except Exception as exception:
		useLog : bool = Application.HasSymbol(application.PYAPPCORE_SYMBOL_LOG)
		if useLog:
			Application.LogException(exception)
		else:
			builtins.print(exception)
		return 1

#------------------------------------------------------------------------
# 파일 진입점.
#------------------------------------------------------------------------
if __name__ == "__main__":
	exitCode = Launching()
	sys.exit(exitCode)