from skr.secret_key_rate import (
    SecretKeyRate
)

skr = SecretKeyRate()

result = skr.calculate(

    pulse_rate_hz=1e8,

    bsm_probability=0.25,

    qber=0.01
)

print()
print(result)