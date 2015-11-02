'''
Created on Oct 27, 2015

@author: wujz
'''
import threading,traceback,sys

class runScriptThread(threading.Thread): #The timer class is derived from the class threading.Thread
    def __init__(self, funcName, *args):
        threading.Thread.__init__(self)
        self.args = args
        self.funcName = funcName
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ''
    
    def run(self): #Overwrite run() method, put what you want the thread do here
        try:
            self._run()
        except Exception as e:
            self.exitcode = 1
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
    
    def _run(self):
        try:
            self.funcName(*(self.args)) 
        except Exception as e:
            raise e        