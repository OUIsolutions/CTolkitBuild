
from .ownership import  OwnerShip
by_value = OwnerShip(by_value=True)
by_value_and_reference = OwnerShip(by_value=True,by_reference=True)
by_value_and_ownership = OwnerShip(by_value=True,by_ownership=True)
by_all = OwnerShip(by_value=True,by_reference=True,by_ownership=True)
by_reference = OwnerShip(by_reference=True)
by_reference_and_ownership =OwnerShip(by_reference=True,by_ownership=True)
by_ownership = OwnerShip(by_ownership=True)

