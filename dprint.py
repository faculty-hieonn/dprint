# -*- coding:utf8 -*-
import sys
import inspect
import re
import pprint

desired_width = 600

try:
    from IPython.display import display, HTML
    import numpy as np
    np.set_printoptions(linewidth=desired_width)
    import pandas as pd
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 10)
except ImportError:
    pass

class PrettyPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):
        return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)

class DPrint:
    def __init__(self):
        self.show = True
        self.call_count = {}
        self.max_calls = 2
        self.last_context = None

    def config(self, show=None, cnt_loop=None):
        if show is not None:
            self.show = show
        if cnt_loop is not None:
            self.max_calls = cnt_loop

    def __call__(self, x, show=None, tag='unknown'):
        if show is not None:
            should_show = show
        else:
            should_show = self.show

        if not should_show:
            return

        # 현재 실행 컨텍스트 (파일명, 함수명, 라인 번호) 추출
        stack = inspect.stack()
        current_context = (stack[1].filename, stack[1].function, stack[1].lineno)

        # 컨텍스트에 대한 호출 횟수 초기화 또는 증가
        if current_context not in self.call_count:
            self.call_count[current_context] = 1
        else:
            self.call_count[current_context] += 1

        # 호출 횟수에 따른 출력 제어
        if self.call_count[current_context] <= self.max_calls:
            self._print_info(x, tag, current_context)
        elif self.call_count[current_context] == self.max_calls + 1:
            # print(f"Context {current_context}: ... (further output suppressed)")
            print(f"(...further output suppressed)")

        # 새로운 컨텍스트가 호출되면 이전 컨텍스트의 호출 횟수 초기화
        if self.last_context is not None and self.last_context != current_context:
            self.call_count[self.last_context] = 0

        self.last_context = current_context

    def _print_info(self, x, tag, context):
        print("-----------------------------------------------------------------------------------")
        if tag == 'unknown':
            tag = "line : %s " % (context[2])
        else:
            tag = "line : %s / %s - " % (context[2], tag)
        
        # if tag == 'unknown':
        #     tag = f"file: {context[0]}, function: {context[1]}, line: {context[2]}"
        # else:
        #     tag = f"{tag} - file: {context[0]}, function: {context[1]}, line: {context[2]}"

        frame = inspect.currentframe().f_back.f_back
        s = inspect.getframeinfo(frame).code_context[0]
        r = re.search(r"\((.*)\)", s).group(1).replace("display=True", "").replace(",", "")
        r = re.sub(r"tag=.+", "", r)

        if not isinstance(x, (int, float, str, tuple, list, dict)):
            try:
                d = ("{} : {} -> {} {}".format(tag, r, type(x), x.shape))
            except Exception:
                d = ("{} : {} -> {}".format(tag, r, type(x)))
            print(d)
            PrettyPrinter().pprint(x)
        else:
            d = ("{} : {} = {} -> {}".format(tag, r, x, type(x)))
            print(d)

# Create an instance of DPrint
dprint = DPrint()