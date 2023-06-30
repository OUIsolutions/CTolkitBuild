

car = Struct(
    
    name='Car',
    initializer='newCar',
    deleter='freeCar'
    values=[
        StructValue('type',int,required=True),
        StructPointer('aaaaa',required=True)
    ]
    
)

cars = ArrayOf(
    data_type= car
    by_value=True,
    by_reference=True,
    by_ownership=True
)





