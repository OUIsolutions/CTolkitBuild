

class NotExpectedResult(Exception):

    def __int__(self,result, expected):

        self.result = result
        self.expected = expected
        super().__init__(f'the result is deiferent than expected')
