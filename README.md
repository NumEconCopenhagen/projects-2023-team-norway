# Team Norway

**Group members:**
- Mie Hustad
- Sivert Dahle


## Data analysis project

Our project is titled **US Presidential Elections**, and in this project we import data from the US Census Bureau using API codes in order to retrieve data about the US population. We merge this dataset with a dataset on the presidential elections from MIT Election Data. We do a Fixed Effect Estimation where we want to see how a one percent increase in a demographic, race, affects the elections results. However, we have not suceeded in visualizing this just yet. Therefore, we visualize the election results for the elections 2008-2020 in different ways in order to show how different visualizations can show different aspects of the election. 

The **results** of the project can be seen from running [dataproject.ipynb](dataproject.ipynb).

We apply the **following datasets**:

1. 1976-2020-president.csv (*https://electionlab.mit.edu/data#data*) 
2. API codes from the American Community Survey (*https://api.census.gov/data/2020/acs/acs5/variables.html*)

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires the following installations:

## Model analysis project

Our project is titled **SIR MODEL**, often used model in health economics, and it models the spread of a disease in the society. We first see how the virus spreads without access to vaccines before we also simulate what happens when vaccines are distributed. What is more, we optimize in order to find the optimal vaccination rate in order to flatten the infection curve the most. 

The **results** of the project can be seen from running [modelproject.ipynb](modelproject.ipynb).

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires no further packages.

## Inaugural project
In this project we solve a household model, for both discrete and continous choiches, where the agents maximize their utility. They can spend their time working in the market or at home. We also see how these decisions change for different levels of female wages while keeping male wages constant. Then we change alpha and sigma in order to minimize the measurement error between our regression estimate and the empirical work of Siminski and Yetsenga (2022). Lastly, we fixed the female productivity to 0,5 in order to have equality of home production productivity between genders and then minimized the error again.

The **results** of the project can be seen from running [inauguralproject.ipynb](inauguralproject.ipynb).

**Dependencies:** Apart from a standard Anaconda Python 3 installation, the project requires no further packages.
