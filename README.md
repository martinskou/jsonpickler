JSONpickler
===========

Version 0.1

Python JSON encoder and decoder supporting objects, tuples and complex keys.


    from jsonpickler import dumps, loads

    s={'a':'demo',(1,2):{3:4},'obj':Test()}

    jsonstr=dumps(s)

    decodeddata=loads(jsonstr)



