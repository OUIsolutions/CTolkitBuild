
import CToolKit as ct
car = ct.Struct(
    type_name='Car',

)

cars = ArrayOf(
    data_type= car
    by_value=True,
    by_reference=True,
    by_ownership=True
)





