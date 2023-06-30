

car = Struct(
    name='Car',
    values=[
        StructInt('type'),
        StructPointer('aaaaa',by_value=True,by_reference=True,by_ownership=True)
    ]
    
)



