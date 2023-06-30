
from .ownership import  OwnerShip
BY_VALUE = OwnerShip(by_value=True)
BY_VALUE_AND_REFERENCE = OwnerShip(by_value=True, by_reference=True)
BY_VALUE_AND_OWNERSHIP = OwnerShip(by_value=True, by_ownership=True)
BY_ALL = OwnerShip(by_value=True, by_reference=True, by_ownership=True)
BY_REFERENCE = OwnerShip(by_reference=True)
BY_REFERENCE_AND_OWNERSHIP =OwnerShip(by_reference=True, by_ownership=True)
BY_OWNERSHIP = OwnerShip(by_ownership=True)

