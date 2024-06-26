
from types import SimpleNamespace

import numpy as np
from scipy import optimize
from scipy.optimize import minimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdSpecializationModelClass:

    def __init__(self):
        """ setup model """
        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.rho = 2.0
        par.nu = 0.001
        par.epsilon = 1.0
        par.omega = 0.5 

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)
        par.wM_vec = np.linspace(1,1,5)

        # e. targets
        par.beta0_target = 0.4
        par.beta1_target = -0.1

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan
        
        #  Extension
        par.work_disutility_gap = 0.0


    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if par.sigma == 0:
            H = min(HM, HF)
        elif par.sigma == 1:
            H = HM**(1-par.alpha)*HF**par.alpha 
        else: 
            H = ((1 - par.alpha )*HM**((par.sigma - 1)/par.sigma) + par.alpha * HF**((par.sigma - 1)/par.sigma))**(par.sigma/(par.sigma-1))

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutlity of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        #disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        disutility = par.nu * (TM ** epsilon_ / epsilon_ + (1 + par.work_disutility_gap) * TF ** epsilon_ / epsilon_)

        
        return utility - disutility

    def solve_discrete(self, do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) 
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt


    def solve_continuous(self, pay_gap=0.0, do_print=False):
        """ solve model continuously """

        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

        # a. Define the objective function to maximize
        def objective(x):
            LM, HM, LF, HF = x
            return -self.calc_utility(LM, HM, LF, HF)

        # b. Define the constraints
        cons = [{'type': 'ineq', 'fun': lambda x: 24 - x[0] - x[1]}, 
                {'type': 'ineq', 'fun': lambda x: 24 - x[2] - x[3]}]

        # c. Define the bounds
        bounds = [(0, 24), (0, 24), (0, 24), (0, 24)]

        # d. Use the SLSQP optimization algorithm to find the solution
        res = minimize(objective, x0=[12, 12, 12, 12], method='SLSQP', bounds=bounds, constraints=cons)
        res = minimize(objective, x0=[12, 12, 12, 12], method='Nelder-Mead', bounds=bounds, constraints=cons)

        # e. Set the optimal values
        opt.LM = res.x[0]
        opt.HM = res.x[1]
        opt.LF = res.x[2]
        opt.HF = res.x[3]

        # f. Print the results if do_print is True
        if do_print:
            for k, v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt


    
    def solve_wF_vec(self, discrete=False):
        """ 
        solve model for vector of female wages and fixed male wage
        """

        par = self.par
        sol = self.sol
        wF = self.par.wF_vec

        # a. loop over wF and wM and solve model
        for j, val in enumerate(wF):
            par.wF = val
            #par.wM = np.linspace(1,1,5)
            if discrete == True: # for discrete choice model
                results = self.solve_discrete()
            else: #for continuous choice model
                results = self.solve_continuous()
            # store results
            sol.LM_vec[j] = results.LM
            sol.HM_vec[j] = results.HM
            sol.LF_vec[j] = results.LF
            sol.HF_vec[j] = results.HF
        
    def run3_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol

        x = np.log(par.wF_vec)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T

        sol.beta0, sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
    

    def objective(self, x):
        """Function to minimize the error by changing alpha and sigma"""

        self.par.alpha, self.par.sigma = x
        self.par.beta0_target = 0.4
        self.par.beta1_target = -0.1
        self.solve_wF_vec()
        self.run3_regression()

        return (self.par.beta0_target - self.sol.beta0)**2 + (self.par.beta1_target - self.sol.beta1)**2


    def estimate(self):
        """Estimate alpha and sigma"""

        bounds = [(0.0001, 2), (0.0001, 10)]
        res = minimize(self.objective, x0=[0.5, 0.5],  method='Nelder-Mead', bounds=bounds)
        self.par.alpha, self.par.sigma = res.x
        
        return res 
    

    def estimate2(self):
        """Estimate sigma while keeping alpha constant at 0.5"""

        # Defines the objective function to minimize
        def objective(x):
            self.par.sigma = x[0]
            self.par.alpha = 0.5
            self.par.beta0_target = 0.4
            self.par.beta1_target = -0.1
            self.solve_wF_vec()
            self.run3_regression()

            print(f"alpha = {self.par.alpha}, sigma = {self.par.sigma}")
            print(f"beta0 = {self.sol.beta0}, beta1 = {self.sol.beta1}")

            return (self.par.beta0_target - self.sol.beta0)**2 + (self.par.beta1_target - self.sol.beta1)**2

        # Defines the bounds
        bounds = [(0.0001, 10)]

        # Using the Nelder-Mead optimization algorithm to find the solution of the minimization
        res = minimize(objective, x0=[0.5], method='Nelder-Mead', bounds=bounds)

        # Setting the optimal value of sigma
        self.par.sigma = res.x[0]

        return res
        
        # Making the disutility function
    def set_work_disutility_gap(self, value):
        self.par.work_disutility_gap = value

    

    

