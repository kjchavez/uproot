from lazytree import *
import matplotlib.pyplot as plt

events = Event.iterator("data/00*.xml")
ets = [event.data.Jet.et if 'Jet' in event.data else []
       for event in events]

plt.hist(np.concatenate(ets), bins=20)
plt.title("Transverse Energy")
plt.xlabel("Energy (MeV)")
plt.ylabel("Count")
plt.show()

#weights = identity_weights(ets)
#weights[0][0] = 2


