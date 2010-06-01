
def loads(string):
    if type(string) not in [str, 'string']:
        raise TypeError('json can only parse strings '+ str(string))
    return window.JSON.parse(string)

def dumps(obj):
    return window.JSON.stringify(obj)

# vim: et sw=4 sts=4
