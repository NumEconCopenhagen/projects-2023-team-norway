import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

class SIRModel3:
    def __init__(self, population, infection_rate, recovery_rate, initial_infected, mortality_rate, vaccination_rate=0):
        self.N = population
        self.beta = infection_rate
        self.gamma = recovery_rate
        self.mu = mortality_rate
        self.I0 = initial_infected
        self.S0 = self.N - self.I0
        self.R0 = 0
        self.D0 = 0
        self.V0 = int(self.N * vaccination_rate)
        

    def simulate_novax(self, num_days):
        S = np.zeros(num_days)
        I = np.zeros(num_days)
        R = np.zeros(num_days)
        D = np.zeros(num_days)
        S[0], I[0], R[0], D[0] = self.S0, self.I0, self.R0, self.D0
        for t in range(1, num_days):
            dS = -self.beta * S[t-1] * I[t-1] / self.N
            dI = self.beta * S[t-1] * I[t-1] / self.N - (self.gamma + self.mu) * I[t-1]
            dR = self.gamma * I[t-1]
            dD = self.mu * I[t-1]
            S[t] = S[t-1] + dS
            I[t] = I[t-1] + dI
            R[t] = R[t-1] + dR
            D[t] = D[t-1] + dD
        return S, I, R, D

    def plot_novax(self, num_days):
        S, I, R, D = self.simulate_novax(num_days)
        plt.plot(S, label="Susceptible")
        plt.plot(I, label="Infected")
        plt.plot(R, label="Recovered")
        plt.plot(D, label="Deaths")
        plt.legend()
        plt.title("SIR Model Without Vaccination")
        plt.show()

                
    def simulate(self, num_days, vaccination_rate):
        S = np.zeros(num_days)
        I = np.zeros(num_days)
        R = np.zeros(num_days)
        D = np.zeros(num_days)
        V = np.zeros(num_days)
        S[0], I[0], R[0], D[0], V[0] = self.S0, self.I0, self.R0, self.D0, self.V0
        for t in range(1, num_days):
            dS = -(self.beta * S[t-1] * I[t-1] / self.N) - (vaccination_rate * S[t-1])
            dI = (self.beta * S[t-1] * I[t-1] / self.N) - ((self.gamma + self.mu) * I[t-1])
            dR = self.gamma * I[t-1]
            dD = self.mu * I[t-1]
            dV = vaccination_rate * S[t-1]
            S[t] = S[t-1] + dS
            I[t] = I[t-1] + dI
            R[t] = R[t-1] + dR
            D[t] = D[t-1] + dD
            V[t] = V[t-1] + dV
        return S, I, R, D, V
    

    def plot(self, num_days, vaccination_rate):
        S, I, R, D, V = self.simulate(num_days, vaccination_rate)
        plt.plot(S, label="Susceptible")
        plt.plot(I, label="Infected")
        plt.plot(R, label="Recovered")
        plt.plot(D, label="Deaths")
        plt.plot(V, label="Vaccinated")
        plt.legend()
        plt.show()

    def total_deaths(self, num_days, vaccination_rate):
        _, _, _, D, _ = self.simulate(num_days, vaccination_rate)
        return D[-1]
    
    def optimize_vaccination_rate(self, num_days):
        result = minimize_scalar(lambda x: self.total_deaths(num_days, x), bounds=(0, 1), method='bounded')
        return result
    