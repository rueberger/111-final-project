
import matplotlib.pyplot as plt
import seaborn as sns

# some formatting for seaborn
sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (8, 4)})

def plot_run(x_prof, x_hist):
    assert len(x_prof) = len(x_hist)
    trial_length = len(x_prof)
    t = np.arange(trial_length)
    plt.plot(x_prof, t, label="Desired profile")
    plt.plot(x_hist, t, label="Measured profile")
    plt.legend()