"""
07.08 Spiking Neural Network: LIF neuron model simulation.
"""
import numpy as np
import matplotlib.pyplot as plt


class LIFNeuron:
    """Leaky Integrate-and-Fire neuron."""
    def __init__(self, tau=20.0, v_th=1.0, v_reset=0.0, r=1.0):
        self.tau = tau
        self.v_th = v_th
        self.v_reset = v_reset
        self.r = r
        self.v = v_reset

    def step(self, i_in, dt=1.0):
        dv = (-(self.v - self.v_reset) + self.r * i_in) / self.tau * dt
        self.v += dv
        spike = self.v >= self.v_th
        if spike:
            self.v = self.v_reset
        return spike, self.v


class SNNLayer:
    def __init__(self, n_neurons, tau=20.0, v_th=1.0):
        self.neurons = [LIFNeuron(tau, v_th) for _ in range(n_neurons)]
        self.n = n_neurons
        self.W = np.random.randn(n_neurons, n_neurons) * 0.1
        self.v_th = v_th

    def step(self, i_in, dt=1.0):
        spikes = []
        for j, neuron in enumerate(self.neurons):
            syn_in = i_in[j] + sum(self.W[j, k] * self.spike_history[k] for k in range(self.n))
            s, v = neuron.step(syn_in, dt)
            spikes.append(s)
        self.spike_history = np.array(spikes, dtype=float)
        return np.array(spikes), [n.v for n in self.neurons]


if __name__ == "__main__":
    np.random.seed(42)
    n_neurons = 5
    layer = SNNLayer(n_neurons)
    T = 200
    spike_raster = np.zeros((T, n_neurons))
    voltages = np.zeros((T, n_neurons))

    for t in range(T):
        i_in = np.random.randn(n_neurons) * 0.5
        if 50 < t < 80:
            i_in += 2.0  # pulse
        spikes, v = layer.step(i_in)
        spike_raster[t] = spikes
        voltages[t] = v

    plt.figure(figsize=(12, 5))
    plt.subplot(211)
    plt.eventplot([np.where(spike_raster[:, i])[0] for i in range(n_neurons)],
                  colors='k', linewidths=1)
    plt.ylabel('Neuron')
    plt.title('Spike raster plot')
    plt.subplot(212)
    for i in range(n_neurons):
        plt.plot(voltages[:, i], label=f'N{i}')
    plt.xlabel('Time step')
    plt.ylabel('Membrane potential')
    plt.legend(ncol=5, fontsize=8)
    plt.tight_layout()
    plt.savefig('../../assets/phase07/spiking_nn.png')
    plt.close()
    print("Saved spiking_nn.png")
