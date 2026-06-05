from skr.secret_key_rate import (
    SecretKeyRate
)

skr = SecretKeyRate()

for d in [

    2,
    4,
    8,
    16

]:

    result = skr.calculate(

        dimension=d,

        q11_z=1e-6,

        ex11=0.03,

        leak_ec=1e-8
    )

    print()
    print(result)