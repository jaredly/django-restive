
from django.utils import simplejson as json
from django.core import serializers
from django.http import HttpResponse

from django.conf.urls.defaults import patterns

import traceback

class Service:
    def __init__(self, name, prefix = ''):
        self.url_list = []
        self.name = name
        self.prefix = prefix

    def add(self, function=None, prefix='', name=None):
        def actual_dec(function):
            def meta(request):
                try:
                    data = json.loads(request.POST['data'])
                except:
                    res = {'error': 'invalid arguments [not JSON]'}
                else:
                    try:
                        res = function(request, **data)
                    except TypeError:
                        res = {'error':'invalid arguments '+str(data), 'tb':traceback.format_exc()}
                    except Exception,e:
                        res = {'error':str(e), 'tb':traceback.format_exc()}
                    else:
                        if not res.has_key('error'):
                            res['error'] = None
                if res.has_key('_models'):
                    res['_models'] = serializers.serialize('json', res['_models'], use_natural_keys=True)
                return HttpResponse(json.dumps(res))
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
