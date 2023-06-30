

class OwnerShip:

    def __init__(self, by_value:bool=False, by_reference:bool=False, by_ownership:bool=False):
        self.by_value = by_value
        self.by_reference = by_reference
        self.by_ownership = by_ownership

        total_elements = 0
        if by_value:
            total_elements+=1

        if by_reference:
            total_elements+=1

        if by_ownership:
            total_elements+=1


        self.require_ownership_flag = False
        if total_elements > 1:
            self.require_ownership_flag = True


