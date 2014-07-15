import sys
from datetime import datetime as time
class Logger:
    
    def __init__(self,component):
        self.component =component
        
    def i(self,TAG,message):
        print '\n'+str(time.now()), '\t', self.component , '\t', TAG , '\t', message
        
    def e(self,TAG,message):
        sys.stderr.write('\n'+str(time.now())+'\t'+  self.component + '\t' +TAG + '\t' + message)

if __name__ == "__main__":
    log= Logger('logger')
    log.e('__main__', 'This is an error')
    log.i('__main__', 'This is a regular log')