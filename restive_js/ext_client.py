
from client import Client

class ExtClient(Client):
    ERROR_MESSAGES = {
        'timeout' : '''Couldn\'t reach the server.
    Check your internet connection and/or try again later. Sorry.
    ''',
        'server' : 'Sorry, a server error occurred. Please reload the page and try again. ',
    }
    def gen_error(self, callback, from_queue):
        if from_queue:
            return self.onerror_queue
        else:
            return self.onerror

    def onerror_queue(self, *args):
        self.advance_queue()
        self.onerror(*args)
    onerror_queue._accept_undefined = True
    
    def onerror(self, request, text, error):
        error = definedor(error, '')
        if text == 'timeout':
            message = self.ERROR_MESSAGES['timeout'] + str(error)
        else:
            message = self.ERROR_MESSAGES['server'] + str(error)
        mb = window.Ext.MessageBox

        def doreload(*a):
            window.location.reload()

        js.mb.alert('Error', message, doreload)
        js.mb.setIcon(mb.ERROR)
    onerror._accept_undefined = True

# vim: et sw=4 sts=4
