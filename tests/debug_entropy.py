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

    print()
    print("d =", d)

    for e in [

        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.49,
        0.499,
        0.5

    ]:

        h = skr.hd_entropy(
            e,
            d
        )

        print(
            e,
            h
        )