import sys
import datetime
import json
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.NullHandler())


class jpickleEncoder(json.JSONEncoder):
    """ A JSONEncoder which can encode objects,
    dicts with advanced keys and tuples """

    def default(self, obj):

        log.debug('Encoding %s' % str(obj))

        if isinstance(obj, (bool, int, long, float, basestring)):
            return obj

        elif isinstance(obj, dict):
            obj = obj.copy()
            newobj={}
            for key in obj:
                if isinstance(key, (bool, int, long, float, basestring)):
                    newobj[key]=self.default(obj[key])
                else:
                    newobj["__decode__"+json.dumps(self.default(key))]=self.default(obj[key])
            return newobj

        elif isinstance(obj, list):
            return [self.default(item) for item in obj]

        elif isinstance(obj, tuple):
            r={'__method__':'reduce','__type__':'tuple','__module__':'__builtin__','args':[[self.default(item) for item in obj]]}
            return r

        if isinstance(obj, datetime.datetime):
            r={'__method__':'specielcase','__type__':'datetime','__module__':'datetime','args':obj.isoformat()}
            return r

        elif hasattr(obj, '__dict__'):
            r={'__method__':'objectinit','__type__':obj.__class__.__name__,'__module__':obj.__module__,'args':self.default(obj.__dict__)}
            return r

        else:
            reduce=obj.__reduce__()
            r={'__method__':'reduce','__type__':reduce[0].__name__,'__module__':reduce[0].__module__,'args':reduce[1]}
            return r

    def encode(self, obj):
        return super(jpickleEncoder, self).encode(self.default(obj))




def decode_object_hook(d):

    """ Object_hook used by json.loads to decode objects,
    dicts with advanced keys and tuples """

    def unpack(v):
        if isinstance(v, basestring):
            if v.startswith("__decode__"):
                v=json.loads(v[10:])
            else:
                v = v
        if isinstance(v, (bool, int, long, float)):
            v = v
        elif isinstance(v, (dict, list)):
            v = unserialize(v)
        return v

    def object_init(d):
        typestr=d['__type__']
        modulestr=d['__module__']
        cls=getattr(sys.modules[modulestr],typestr)
        obj=cls()
        for k,v in d['args'].items():
            obj.__dict__[unserialize(k)]=unserialize(v)
        return obj

    def object_init_reduce(d):
        typestr=d['__type__']
        modulestr=d['__module__']
        cls=getattr(sys.modules[modulestr],typestr)
        obj=cls(*unserialize(d['args']))
        return obj


    def unserialize(d):

        log.debug('Decoding %s' % str(d))

        if isinstance(d, basestring):
            return unicode(d)

        if isinstance(d, (bool, int, long, float)):
            return d

        if isinstance(d, list):
            result = []
            for v in d:
                result.append(unpack(v))
            return result

        elif isinstance(d, dict):
            if "__type__" in d.keys():
                if d['__type__']=='datetime' and d['__module__']=='datetime':
                    return datetime.datetime.strptime(d['args'], '%Y-%m-%dT%H:%M:%S.%f')
                if d['__method__']=='reduce':
                    return object_init_reduce(d)
                if d['__method__']=='objectinit':
                    return object_init(d)
                return "Unknown(%s)" % d['__type__']
            else:
                result = []
                for k,v in d.items():
                    result.append((unpack(k), unpack(v)))
                return dict(result)

        return d

    return unserialize(d)


def dumps(data,cls=jpickleEncoder,indent=4):
    return json.dumps(data,cls=cls, indent=indent)

def loads(strdata, object_hook=decode_object_hook):
    return json.loads(strdata, object_hook=object_hook)


if __name__=='__main__':

    import collections

    # Some basic testing

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%H:%M:%S')
    ch.setFormatter(formatter)

    class Test2(object):
        def __init__(self):
            self.y=(1,2,3)

    class Test(object):
        def __init__(self):
            self.x=13
            self.t=Test2()

    #s=['a','b',(1,2,3),'c',{(1,'x'):'xyz'},Test(),collections.deque(['d','e']),datetime.datetime.now()]
    s={'a':'demo',(1,2):{3:4},'obj':Test()}
    print "RAW:"
    print s
    print "DUMPING..."
    j=json.dumps(s,cls=jpickleEncoder, indent=4)
    print "JSON ENCODED:"
    print j
    print "LOADING..."
    d=json.loads(j, object_hook=decode_object_hook)
    print "DECODED RAW:"
    print d

