# -*- coding:utf8 -*-
import sys
try :
    reload(sys)
    sys.setdefaultencoding('utf8')
except :
    pass

import inspect
import re
import pprint

desired_width=600

from IPython.display import display, HTML

try:
    import numpy as np
    np.set_printoptions(linewidth=desired_width)
    import pandas as pd
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 10)
except ImportError:
    pass

class PrettyPrinter(pprint.PrettyPrinter):
        def format(self, _object, context, maxlevels, level):
        # if isinstance(_object, unicode):
        # 	return "'%s'" % _object.encode('utf8'), True, False
        # if isinstance(_object, str):
        # 	#_object = unicode(_object,'utf8')
        # 	return "'%s'" % _object.encode('utf8'), True, False
            return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)

def dprint(x, show=True, tag='unknown'):

    if show == False :
        return

    print ("-----------------------------------------------------------------------------------")
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    if tag == 'unknown' :
        tag = "line : %s " %(caller.lineno)
    else :
        tag = "line : %s / %s - " %(caller.lineno, tag)
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1).replace("display=True", "").replace(",", "")
    r = re.sub(r"tag=.+", "", r)
    #d = ("{} : {} = {}".format(tag, r,x))
    data_type = type(x)
    #if data_type is list or data_type is dict or data_type is tuple or data_type is set or data_type is pandas.core.series.Series :
    if not (data_type is int or data_type is float or data_type is str or data_type is tuple or data_type is list or data_type is dict) :
        try :
            d = ("{} : {} -> {} {}".format(tag, r, type(x), x.shape))
        except :
            d = ("{} : {} -> {}".format(tag, r, type(x)))
        print (d)
        PrettyPrinter().pprint(x)
    else :
        d = ("{} : {} = {} -> {}".format(tag, r, x, type(x)))
        print (d)


class cprint() :

    display = False

    def __init__(self, display) :
        self.display = display

    def init(self, display) :
        self.display = display

    def get_display(self) :
        return self.display

    def dfprint(self, df, head=10, embed=True):
        if embed == True :
            display(HTML(df.to_html()))
        else :
            css = """<style>
            table { border-collapse: collapse; border: 3px solid #eee; }
            table tr th:first-child { background-color: #eeeeee; color: #333; font-weight: bold }
            table thead th { background-color: #eee; color: #000; }
            tr, th, td { border: 1px solid #ccc; border-width: 1px 0 0 1px; border-collapse: collapse;
            padding: 3px; font-family: monospace; font-size: 10px }</style>
            """
            s  = '<script type="text/Javascript">'
            s += 'var win = window.open("", "Title", "toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=780, height=400, top="+(screen.height-400)+", left="+(screen.width-840));'
            s += 'win.document.body.innerHTML = \'' + (df.to_html() + css).replace("\n",'\\') + '\';'
            s += '</script>'
            print(df.head(head))
            return(HTML(s+css))

       
    def dprint(self, x, show=True,  force=False, tag='unknown'):

        # force True : display wins
        # force False : self.display wins

        if self.display == True and  show==True and force==True:
            _display = True
        elif self.display == True and  show==True and force==False:
            _display = True
        elif self.display == True and  show==False  and force==True:
            _display = False
        elif self.display == True and  show==False and force==False:
            _display = True
        elif self.display == False and  show==True and force==True:
            _display = True
        elif self.display == False and  show==True and force==False:
            _display = False
        elif self.display == False and  show==False  and force==True:
            _display = False
        elif self.display == False and  show==False and force==False:
            _display = False

        if _display == False :
            return
                
        print ("-----------------------------------------------------------------------------------")
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        if tag == 'unknown' :
            tag = "line : %s " %(caller.lineno)
        else :
            tag = "line : %s / %s - " %(caller.lineno, tag)
        frame = inspect.currentframe().f_back
        s = inspect.getframeinfo(frame).code_context[0]
        r = re.search(r"\((.*)\)", s).group(1).replace("display=True", "").replace(",", "")
        r = re.sub(r"tag=.+", "", r)
        #d = ("{} : {} = {}".format(tag, r,x))
        data_type = type(x)
        #if data_type is list or data_type is dict or data_type is tuple or data_type is set or data_type is pandas.core.series.Series :
        if not (data_type is int or data_type is float or data_type is str or data_type is tuple or data_type is list or data_type is dict) :
            try :
                d = ("{} : {} -> {} {}".format(tag, r, type(x), x.shape))
            except :
                d = ("{} : {} -> {}".format(tag, r, type(x)))
            print (d)
            PrettyPrinter().pprint(x)
        else :
            d = ("{} : {} = {} -> {}".format(tag, r, x, type(x)))
            print (d)

# def dprintPretty(x) :
#     PrettyPrinter().pprint(x)

