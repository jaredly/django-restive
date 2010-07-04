
from django.utils import simplejson as json
from django.core import serializers
from django.http import HttpResponse

from django.conf.urls.defaults import patterns

import traceback

def process_data(data):
    if isinstance(data, dict) and data.has_key('_models'):
        data['_models'] = serializers.serialize('json', data['_models'])
    return HttpResponse(json.dumps(data), mimetype='application/json')


class Service:
    def __init__(self, prefix = ''):
        self.url_list = []
        self.prefix = prefix

    def add(self, function=None, prefix='', name=None):
        def actual_dec(function):
            def meta(request, *args, **kwargs):
                if request.POST.has_key('data'):
                    try:
                        data = json.loads(request.POST['data'])
                        kwargs.update(data)
                    except:
                        return process_data({'error': 'invalid arguments [not JSON]'})
                try:
                    res = function(request, *args, **kwargs)
                except TypeError:
                    res = {'error':'invalid arguments '+str(data), 'tb':traceback.format_exc()}
                except Exception,e:
                    res = {'error':str(e), 'tb':traceback.format_exc()}
                return process_data(res)

            fname = name
            if fname is None:
                fname = function.__name__
            self.url_list.append(['^' + self.prefix + prefix + fname + '/$', meta])
            return function
        if function is not None:
            return actual_dec(function)
        return actual_dec

    def urls(self):
        return patterns('', *self.url_list)

# vim: et sw=4 sts=4
