#    
#    factory.py ... Factory pattern generator.
#    Copyright (C) 2010  KennyTM~ <kennytm@gmail.com>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    

import sys

class factorySuffix(object):
    """A class decorator that make a class adopts the `factory pattern
    <http://en.wikipedia.org/wiki/Factory_method_pattern>`_ distinguished by a
    keyword. Factories are registered at runtime, allowing plug-ins to provide
    extra capabilities without modifying the base source code::
    
        @factory
        class Image(object):
            def __init__(self, typ, width, height):
                ...

        class PNGImage(Image):
            ...
            
        class JPGImage(Image):
            ...
            
        Image.registerFactory("png", PNGImage)
        Image.registerFactory("jpg", JPGImage)
        
        pngImg = Image.create("png", 100, 100)
        jpgImg = Image.create("jpg", 800, 600)
        genericImg = Image.create("gif", 20, 20)
        
        assert type(pngImg) is PNGImage
        assert type(jpgImg) is JPGImage
        assert type(genericImg) is Image
    
    User may provide a suffix so that the class may be generated by different
    factories::
    
        @factory
        class Foo(object):
            ...
        
        @factorySuffix(suffix='More')
        class Bar1(Foo):
            @classmethod
            def _createBar(cls, keywordA, keywordB):
                return cls.createMore(keywordB, keywordA)
        
            def __init__(self, keywordB, keywordA):
                ...
        
        class Baz(Bar1):
            ...
        
        Foo.registerFactory(1, Bar1._createBar)
        Bar1.registerFactoryMore('baz', Baz)
    
        obj = Foo.create(1, 'baz')
        # calls Bar1._createBar(1, 'baz')
        # calls Bar1.createMore('baz', 1)
        # calls Baz('baz', 1)
    
    The following class methods are added to a class adopting the this
    decorator. If *suffix* is provided, the methods added will be named as
    ``cls.registerFactorySuffix``, etc.
    """

    @classmethod
    def registerFactory(cls, keyword, cons):
        '''Register a keyword with a subclass *cons* of the class *cls*. The
        subclass's constructor's signature should be::

            @classmethod
            def constructor(cls, keyword, ...):
                ...
        '''

    @classmethod
    def getFactory(cls, keyword):
        '''Returns the subclass registered with *keyword*. The base class
        *cls* will be returned if that keyword is unregistered.'''
    
    @classmethod
    def create(cls, keyword, *args, **kargs):
        '''Create an instance, specialize to a subclass based on the
        *keyword*.'''

    def __init__(self, suffix='', defaultConstructor='__call__'):
        self.suffix = suffix
        self.defcon = defaultConstructor
    
    def __call__(self, clsx):
        suffix = self.suffix
        factoryName = '_factories' + suffix
        getFactoryName = 'getFactory' + suffix
        defcon = self.defcon
    
        if 'sphinx-build' in sys.argv[0]:
            @classmethod
            def nop(k, *args, **kwargs):
                pass
            rf = gf = cf = nop
        
        else:
            @classmethod
            def rf(cls, keyword, cons):
                getattr(cls, factoryName)[keyword] = cons
            
            @classmethod
            def gf(cls, keyword):
                return getattr(cls, factoryName).get(keyword, getattr(cls, defcon))
            
            @classmethod
            def cf(cls, keyword, *args, **kargs):
                return getattr(cls, getFactoryName)(keyword)(keyword, *args, **kargs)
            
        setattr(clsx, 'registerFactory' + suffix, rf)
        setattr(clsx, getFactoryName, gf)
        setattr(clsx, 'create' + suffix, cf)
        setattr(clsx, factoryName, {})
        
        return clsx

            
def factory(cls):
    '''Equivalent to :class:`factorySuffix` with no suffix.'''
    return factorySuffix()(cls)


if __name__ == '__main__':
    @factory
    class A(object):
        def __init__(self, index, value):
            self.index = index
            self.value = value
            
        def __str__(self):
            return "{}: {}={}".format(type(self), self.index, self.value)
    
    class B(A):
        def __init__(self, index, value):
            super().__init__(index, value)
            print("constructing B")
    
    class C(A):
        def __init__(self, index, value):
            super().__init__(index, value)
            print("constructing C")
    
    A.registerFactory(4, B)
    A.registerFactory(7, B)
    A.registerFactory(6, C)
    
    print (A.create(3, 6))
    print (A.create(4, 7))
    print (A.create(5, 8))
    print (A.create(6, 9))
    print (A.create(7, 10))
    print (A.create(8, 11))
    
