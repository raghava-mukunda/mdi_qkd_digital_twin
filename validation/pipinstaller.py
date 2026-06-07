import matplotlib.pyplot as plt
import numpy as np

cm = np.array([
    [825,48,0],
    [87,947,10],
    [0,11,72]
])

plt.figure(figsize=(6,5))

plt.imshow(
    cm,
    cmap="Blues"
)

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            str(cm[i,j]),
            ha="center",
            va="center"
        )

plt.xticks(
    [0,1,2],
    ["d=4","d=8","d=16"]
)

plt.yticks(
    [0,1,2],
    ["d=4","d=8","d=16"]
)

plt.xlabel("Predicted")
plt.ylabel("True")

plt.title(
    "Confusion Matrix"
)

plt.colorbar()

plt.tight_layout()

plt.show()