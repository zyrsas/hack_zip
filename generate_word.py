class BaseCharSet(object):
    def __init__(self):
        self.base_char_set = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~!@#$%^&*()_+=-`<>,./?;:\'"[]{}|\\ '

class SimpleEngine():
    def __init__(self,
                 char_list = BaseCharSet().base_char_set,
                 string_length = 3):
        self.string_len = string_length
        self.char_picklist = char_list
          
    def product(self, *args):
        if not args:
            return iter(((),)) # yield tuple()
        return (items + (item,) for items in self.product(*args[:-1]) for item in args[-1])

    def generator(self, direction='forward'):
        if direction == 'backward':
        ## return z-a
            return self.product(*[self.char_picklist[::-1] for i in range(self.string_len)])
        ## Return a-z
        else: return self.product(*[self.char_picklist for i in range(self.string_len)])
       
    def setStringLength(self, length):
        self.string_len = length

    def setCharList(self, charlist):
        self.char_picklist = charlist

    def charList(self):
        return self.char_picklist

    def stringLength(self):
        return self.string_len


class BeginsWithEngine(SimpleEngine):
    ''' This class is for creating passwords where you know the starting chars'''
    def __init__(self,
                 char_list = BaseCharSet().base_char_set,
                 string_length = 3,
                 begins_with = ''):
        SimpleEngine.__init__(self,
                              char_list = char_list,
                              string_length = string_length)
        self.begins_str = begins_with

    def setBeginsWithString(self, begins_with):
        self.begins_str = begins_with

    def beginsWithString(self):
        return self.begins_str

    def generator(self):
        args = [self.char_picklist for i in range(self.string_len - len(self.begins_str))]
        args.insert(0, [self.begins_str])
        return self.product(*args)
       
       
class EndsWithEngine(SimpleEngine):
    ''' This class is for creating passwords where you know the end chars'''
    def __init__(self,
                 char_list = BaseCharSet().base_char_set,
                 string_length = 3,
                 ends_with = ''):
        SimpleEngine.__init__(self,
                              char_list = char_list,
                              string_length = string_length)
        self.ends_str = ends_with

    def setEndsWithString(self, ends_with):
        self.ends_str = ends_with

    def endsWithString(self):
        return self.ends_str

    def generator(self):
        args = [self.char_picklist for i in range(self.string_len - len(self.ends_str))]
        args.append([self.ends_str])
        return self.product(*args)

class ContainsEngine(SimpleEngine):
    def __init__(self,
                 char_list = BaseCharSet().base_char_set,
                 string_length = 3,
                 contains = '',
                 mixed_case = False):
        SimpleEngine.__init__(self,
                              char_list = char_list,
                              string_length = string_length)
        self.contains_str = contains
        self.use_mixed_case = mixed_case
       
    def setContainsString(self, contains):
        self.contains_str = contains

    def containsString(self):
        return self.contains_str

    def _generator_(self):
        start_index = 0
        for pos in range((self.string_len +1) - len(self.contains_str)):
            args = [self.char_picklist for i in range(self.string_len - len(self.contains_str))]
            args.insert(pos, [self.contains_str])
            yield self.product(*args)
            start_index += 1

    def generator(self):
        for row in self._generator_():
            for value in row:
                yield value


