from bsm.charlie_receiver import (
    CharlieReceiver
)

charlie = CharlieReceiver()

success = 0

N = 10000

for k in range(N):

    result = charlie.process_trial(

        alice_mu=0.4,

        bob_mu=0.4,

        visibility=0.95,

        timestamp_ps=k*100000
    )

    if result.psi_minus:

        success += 1

print()

print(
    "Trials:",
    N
)

print(
    "Psi- Events:",
    success
)

print(
    "BSM Success Probability:",
    success / N
)