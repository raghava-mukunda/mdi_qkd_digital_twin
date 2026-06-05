from protocol.frame_engine import (
    FrameEngine
)

from skr.secret_key_rate import (
    SecretKeyRate
)

engine = FrameEngine()

skr = SecretKeyRate()

print()
print("="*80)
print("FRAME SWEEP")
print("="*80)

for d in [

    2,
    4,
    8,
    16

]:

    successes = 0

    windows = 0

    N = 10000

    for _ in range(N):

        result = (
            engine.run_frame(d)
        )

        successes += (
            result.successful_bsm
        )

        windows += (
            result.windows
        )

    q11 = (
        successes
        /
        windows
    )

    r = skr.calculate(

        dimension=d,

        q11_z=q11,

        ex11=0.03,

        leak_ec=1e-4*q11
    )

    print()

    print(
        f"d={d}"
    )

    print(
        f"Q11={q11:.6f}"
    )

    print(
        f"SKR={r.secret_key_rate:.6f}"
    )