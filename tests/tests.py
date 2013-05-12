#encoding=utf8

import sys
sys.path.insert(0,"../")

import unittest

from jsonpickler import loads, dumps

import logging

log = logging.getLogger("jsonpickler")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#log.addHandler(ch)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s','%H:%M:%S')
ch.setFormatter(formatter)

class C1(object):
    def __init__(self):
        self.x=[1,2,3]


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_string(self):
        s="a string"
        d=loads(dumps(s))
        print s,d
        self.assertEqual(s, d)

    def test_dict(self):
        s={"a":"a string"}
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_dict_unicode(self):
        s={"a":u"æøå"}
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_dict_complex_key(self):
        s={(2,"a"):1234}
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_set(self):
        s=set([1,2,3,(4,5)])
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_list(self):
        s=[1,2,3,(4,5),{'a':'b'}]
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_merged(self):
        s=[1,2,3,(4,5),{'a':[1,'b',[{'c':'x'}]]}]
        d=loads(dumps(s))
        self.assertEqual(s, d)

    def test_class(self):
        s=[C1()]
        d=loads(dumps(s))
        self.assertEqual(s[0].x, d[0].x)



if __name__ == '__main__':
    unittest.main()
