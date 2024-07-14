#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
import builtins
import unittest
import os
import sys
from pyappcore import TestsLaunching


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
CURRENTFILEPATH : str = os.path.abspath(__file__)
TESTSPATH : str = os.path.dirname(CURRENTFILEPATH).replace("\\", "/")
ROOTPATH : str = os.path.dirname(TESTSPATH).replace("\\", "/")


#------------------------------------------------------------------------
# 파일 진입점.
#------------------------------------------------------------------------
if __name__ == "__main__":
	TestsLaunching(ROOTPATH)