
import json

class Client:
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.loading = 0
        self.queue = []
        self.listeners = {'start':[], 'end':[]}
        self.queueing = False

    def send(self, command, data, callback, from_queue = False):
        self.loading += 1
        window.jQuery.ajax({
            'cache': False,
            'data': {'data':json.dumps(data)},
            'dataType': 'text',
            'error': self.gen_error(callback, from_queue),
            'success': self.gen_callback(callback, from_queue),
            'type': 'POST',
            'url': self.prefix + command + '/',
        })
        for cb in self.listeners['start']:
            cb()

    def send_queued(self, command, data, callback):
        self.queue.append([command, data, callback])
        if not self.queueing:
            self.queueing = True
            self.advance_queue()

    def advance_queue(self):
        if not len(self.queue):
            self.queueing = False
            return
        args = self.queue.pop(0)
        self.send(*(args + [True]))

    def gen_error(self, callback, from_queue=False):
        def onerror(request, text, error):
            error = definedor(error, '')
            if from_queue:
                self.advance_queue()
            return callback({'error':'HTTP ERROR', 'text':text, 'errno':error})
        onerror._accept_undefined = True
        return onerror

    def gen_callback(self, callback, from_queue = False):
        def meta(text, status, request):
            self.loading -= 1
            if from_queue:
                self.advance_queue()
            try:
                data = dict(json.loads(text))
            except:
                return callback({'error': 'JSON ERROR', 'data': text})

            if data.has_key('_models'):
                data['_models'] = list(json.loads(data['_models']))

            callback(data)

            for cb in self.listeners['end']:
                cb()
        return meta

# vim: et sw=4 sts=4
