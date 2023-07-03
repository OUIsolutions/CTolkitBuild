

class NotExpectedResult(Exception):

    def __int__(self,result, expected):
        self.mensage = f'the result is deiferent than expected'
        self.result = result
        self.expected = expected
