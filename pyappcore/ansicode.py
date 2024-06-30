#------------------------------------------------------------------------
# 참조 모듈 목록.
#------------------------------------------------------------------------
from __future__ import annotations
import builtins
import re


#------------------------------------------------------------------------
# 전역 상수 목록.
#------------------------------------------------------------------------
TAG_PATTERN : str = "<(\\w+)>(.*?)</\\1>"
ANSICODES : dict = {
    "clear" : "\033[0m", # 적용된 속성 초기화.
    "c" : "\033[0m", # 적용된 속성 초기화.

    "bold" : "\033[1m", # 두껍게.
    "b" : "\033[1m", # 두껍게.

    # "faint" : "\033[2m", # 어둡게.

    "italic" : "\033[3m", # 기울임.
    "i" : "\033[3m", # 기울임.

    "underline" : "\033[4m", # 밑줄.
    "u" : "\033[4m", # 밑줄.

    # "blink_slow" : "\033[5m", # 천천히 깜빡임.
    # "blink_rapid" : "\033[6m", # 빠르게 깜빡임.
    # "inverse" : "\033[7m", # 이미지 반전.
    # "hidden" : "\033[8m", # 숨김.

    "strike" : "\033[9m", # 취소선.
    "s" : "\033[9m", # 취소선.

    "black" : "\033[30m", # 글자-검은색.
    "red" : "\033[31m", # 글자-빨간색.
    "green" : "\033[32m", # 글자-초록색.
    "yellow" : "\033[33m", # 글자-노란색.
    "blue" : "\033[34m", # 글자-파란색.
    "magenta" : "\033[35m", # 글자-자주색.
    "cyan" : "\033[36m", # 글자-청록색.
    "white" : "\033[37m", # 글자-하얀색.

    "bg_black" : "\033[40m", # 배경-검은색.
    "bg_red" : "\033[41m", # 배경-빨간색.
    "bg_green" : "\033[42m", # 배경-초록색.
    "bg_yellow" : "\033[43m", # 배경-노란색.
    "bg_blue" : "\033[44m", # 배경-파란색색.
    "bg_magenta" : "\033[45m", # 배경-자주색.
    "bg_cyan" : "\033[46m", # 배경-청록색.
    "bg_white" : "\033[47m", # 배경-하얀색.
}


#------------------------------------------------------------------------
# 태그 처리용 스택.
#------------------------------------------------------------------------
class ANSIStyleStack:
	#------------------------------------------------------------------------
	# 멤버 변수 목록.
	#------------------------------------------------------------------------
    __stack : list
    __current : str

	#------------------------------------------------------------------------
	# 초기화.
	#------------------------------------------------------------------------
    def __init__(self) -> None:
        self.__stack = list()
        self.__current = str()

	#------------------------------------------------------------------------
	# 넣기.
	#------------------------------------------------------------------------
    def Push(self, style):
        self.__stack.append(self.__current)
        self.__current += ANSICODES[style]

	#------------------------------------------------------------------------
	# 빼기.
	#------------------------------------------------------------------------
    def Pop(self):
        if self.__stack:
            self.__current = self.__stack.pop()
        else:
            self.__current = ANSICODES["clear"]

	#------------------------------------------------------------------------
	# 전체 스택 초기화.
	#------------------------------------------------------------------------
    def Clear(self):
        self.__stack = list()
        self.__current = str()

	#------------------------------------------------------------------------
	# 현재 스택.
	#------------------------------------------------------------------------
    @property
    def Current(self):
        return self.__current


#------------------------------------------------------------------------
# 태그 파싱용 정규식 패턴.
#------------------------------------------------------------------------
__Pattern = re.compile(TAG_PATTERN)


#------------------------------------------------------------------------
# 태그 처리용 스택.
#------------------------------------------------------------------------
__Stack = ANSIStyleStack()


#------------------------------------------------------------------------
# 텍스트 파싱.
#------------------------------------------------------------------------
def ParseANSICode(match) -> None:
    tag = match.group(1)
    content = match.group(2)
    __Stack.Push(tag)
    startTag = __Stack.Current
    __Stack.Pop()
    endTag = __Stack.Current
    return f"{startTag}{content}{endTag}"


#------------------------------------------------------------------------
# 텍스트 전체 파싱.
#------------------------------------------------------------------------
def ParseAllANSICodes(text : str) -> None:
    __Stack.Clear()
    return __Pattern.sub(ParseANSICode, text) + ANSICODES["clear"]


#------------------------------------------------------------------------
# ANSICODE 기반 텍스트 출력.
#------------------------------------------------------------------------
def Print(text : str) -> None:
    parsedText = ParseAllANSICodes(text)
    builtins.print(parsedText)


#------------------------------------------------------------------------
# ANSICODE 기반 붉은색 텍스트 출력.
#------------------------------------------------------------------------
def PrintWithBold(text : str) -> None:
    Print(f"<b>{text}</b>")

 
#------------------------------------------------------------------------
# ANSICODE 기반 붉은색 텍스트 출력.
#------------------------------------------------------------------------
def PrintWithRed(text : str) -> None:
    Print(f"<red>{text}</red>")


#------------------------------------------------------------------------
# ANSICODE 기반 초록색 텍스트 출력.
#------------------------------------------------------------------------
def PrintWithGreen(text : str) -> None:
    Print(f"<green>{text}</green>")


#------------------------------------------------------------------------
# ANSICODE 기반 파란색 텍스트 출력.
#------------------------------------------------------------------------
def PrintWithGreen(text : str) -> None:
    Print(f"<blue>{text}</blue>")
    
    
#------------------------------------------------------------------------
# ANSICODE 기반 노란색 텍스트 출력.
#------------------------------------------------------------------------
def PrintWithGreen(text : str) -> None:
    Print(f"<yellow>{text}</yellow>")