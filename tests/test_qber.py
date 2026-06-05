from statistics.qber import (
    QBERCalculator
)

qber = QBERCalculator()

alice = [

    0,1,0,1,
    0,1,0,1
]

bob = [

    1,0,1,0,
    1,0,1,0
]

success = [

    True,True,True,True,
    True,True,True,True
]

result = qber.calculate(

    alice,

    bob,

    success
)

print()
print(result)