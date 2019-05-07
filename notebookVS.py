
#%%
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
get_ipython().run_line_magic('matplotlib', 'inline')
np.set_printoptions(precision=2)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Lobster-Regular'

import matplotlib.font_manager
# matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')


#%%
lobster_csv = pd.read_csv('lobsterdata.csv')

# seasonally adjusted
CPI_csv = pd.read_csv('ConsumerPriceIndex.csv')

# I split this up before hand but it was just a column that has every row with lobster
lobster_csv.drop('Species',axis=1,inplace=True)

# No real need for pounds and tons, can just convert later.
lobster_csv.drop('Metric Tons',axis=1,inplace=True)

#%% [markdown]
# ### Handel CPI

#%%
CPI_csv.DATE = pd.to_datetime(CPI_csv.DATE)
CPI_csv.index = pd.DatetimeIndex(CPI_csv.DATE)
CPI_date_df = pd.DataFrame(CPI_csv['CPIAUCSL'])
CPI_yr_mean = CPI_date_df.groupby(CPI_date_df.index.year).mean()
CPI_yr_mean.drop(CPI_yr_mean.index[[0,-1,-2]],inplace=True)

#%% [markdown]
# ### Handel Lobsters

#%%
no_type = lobster_csv[['Year','Pounds','USD']].copy()
lob_year = no_type.groupby(['Year']).sum()
lob_year['PerPound'] = lob_year['USD']/lob_year['Pounds']
perpound_mean = lob_year['PerPound'].mean()

#%% [markdown]
# ### Vars to plot

#%%
pp_inflation = lob_year.iloc[-1,2]/ lob_year.iloc[0,2]
lob_year_log = lob_year.pct_change(periods=3)
avg_change = lob_year.pct_change().mean()
xmin = lob_year.index.min()+3
xmax = lob_year.index.max()
pp_norm = lob_year['PerPound'] / lob_year['PerPound'].iloc[0]
CPI_norm = CPI_yr_mean/ CPI_yr_mean.iloc[0]

#%% [markdown]
# ### King Krabz

#%%
lob_type_df = lobster_csv.groupby(['Type','Year']).mean()
spec_cleaned_df = lob_type_df.reset_index()
spec_cleaned_df = spec_cleaned_df.set_index('Year',drop=True)
spec_cleaned_df['PerPound'] = spec_cleaned_df['USD']/spec_cleaned_df['Pounds']
spec_cleaned_df.drop(['Pounds','USD'],axis=1,inplace=True)
lob_grop = spec_cleaned_df.groupby(['Type','Year']).sum()
unstuck = lob_grop.unstack(level=-1).T
xd = unstuck.reset_index()
xd.drop('level_0',axis=1,inplace=True)
lol = xd.set_index('Year')
cali_norm = lol['CALIFORNIA SPINY'] / lol['CALIFORNIA SPINY'].iloc[0]

#%% [markdown]
# ### Lobster Weight

#%%
weight_df = lobster_csv[['Year','Type','Pounds']].copy()

# All Types

all_types_df = weight_df.groupby('Year').sum()['Pounds']

# By Type 

by_type_df = weight_df.groupby(['Year','Type']).sum()
by_type_df = by_type_df.unstack(-1).reset_index()
by_type_df = by_type_df.set_index('Year')

#%% [markdown]
# ### Weight by Type Normalized

#%%
# pull out from multi index and into series
American = by_type_df['Pounds', 'AMERICAN']
banded_spiny = by_type_df['Pounds', 'BANDED SPINY']
california_spiny = by_type_df['Pounds', 'CALIFORNIA SPINY']
caribbean_spiny = by_type_df['Pounds', 'CARIBBEAN SPINY']
slipper = by_type_df['Pounds', 'SLIPPER']
spanish = by_type_df['Pounds', 'SPANISH']

# Clean off the Missing Years
American.dropna(inplace=True)
banded_spiny.dropna(inplace=True)
california_spiny.dropna(inplace=True)
caribbean_spiny.dropna(inplace=True)
slipper.dropna(inplace=True)
spanish.dropna(inplace=True)

# Normalize the Data
American_norm = American/American.iloc[0]
banded_spiny_norm = banded_spiny/banded_spiny.iloc[0]
california_spiny_norm = california_spiny/california_spiny.iloc[0]
caribbean_spiny_norm = caribbean_spiny/caribbean_spiny.iloc[0]
slipper_norm = slipper/slipper.iloc[0]
spanish_norm = spanish/spanish.iloc[0]

#%% [markdown]
# ## Plots

#%%
fig,ax = plt.subplots()

ax.axes.axhline(y=perpound_mean,color='red')

per_pound = ax.plot( lob_year.index, lob_year['PerPound'])



plt.xlim(lob_year.index.min(),lob_year.index.max())
plt.grid(True)
plt.legend(['Mean','Lobster Price'])


plt.title('Price Per Pound by the Year')
plt.ylabel('$ Per Pound')
plt.xlabel('Year')

fig.set_size_inches(8, 5)
fig.set_dpi(600)
plt.savefig('images/price_per_pound_change_art')
plt.show();


#%%
fig,ax = plt.subplots()

per_pound = ax.plot( lob_year_log.index, pp_norm)

CPI = ax.plot( lob_year_log.index, CPI_norm)



plt.title('Lobsters Vs Consumer Price Index',fontname='Lobster')
plt.ylabel('Normalized Change')
plt.xlabel('Year')

plt.xlim(xmin,xmax)
plt.grid(True)
plt.legend(['Per Pound','CPI'])

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/NormCPIvLob')
plt.show();


#%%

fig,ax = plt.subplots()

ax.axes.axhline(y=avg_change[2],color='red')

per_pound = ax.plot( lob_year_log.index, lob_year_log['PerPound'])


plt.xlim(xmin,xmax)
plt.grid(True)
plt.legend(['Mean','Percent Change Daily'])

plt.title('Yearly % Change')
plt.ylabel('% Change')
plt.xlabel('Year')

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/pctchange daily')
plt.show();


#%%
fig,ax = plt.subplots()


MERICA = ax.plot(lol.index, lol['AMERICAN'])

bran_spiny = ax.plot(lol.index, lol['BANDED SPINY'])

cali = ax.plot(lol.index, lol['CALIFORNIA SPINY'])

caribbean = ax.plot(lol.index, lol['CARIBBEAN SPINY'])

slipper = ax.plot(lol.index, lol['SLIPPER'])

spanish = ax.plot(lol.index, lol['SPANISH'])


plt.xlim(lob_year.index.min(),lob_year.index.max())
plt.grid(True)
plt.legend()

plt.title('Best Gaining')
plt.ylabel('$ Per Pound')
plt.xlabel('Year')

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/BestCrabs')
plt.show();


#%%
fig,ax = plt.subplots()

CPI = ax.plot( lob_year_log.index, CPI_norm)

MERICA = ax.plot(lol.index, cali_norm)


plt.xlim(lob_year.index.min(),lob_year.index.max())
plt.grid(True)
plt.legend(['California Spiny','CPI'])

plt.title('Best Investment Banking Crab')
plt.ylabel('Normalized Change')
plt.xlabel('Year')

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/BestCrabVsCPI')
plt.show();


#%%
print(f'Cali Spiny: {cali_norm.iloc[-1]} CPI: {CPI_norm.iloc[-1,0]} ')


#%%
fig,ax = plt.subplots()

all_types = ax.plot( lob_year_log.index, (all_types_df/100000))

by_type = ax.plot(lol.index,(by_type_df/100000))


plt.xlim(lob_year.index.min(),lob_year.index.max())
plt.grid(True)
plt.legend(['TOTAL','AMERICAN', 'BANDED SPINY', 'CALIFORNIA SPINY', 'CARIBBEAN SPINY', 'SLIPPER', 'SPANISH'])

plt.title('Lobsters Captured By Weight')
plt.ylabel('Per 100,000 Pounds')
plt.xlabel('Year')
plt.ylim(-1)

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/Lobsters Captured By Weight')
plt.show();


#%%
fig,ax = plt.subplots()


MERICA = ax.plot(American_norm.index, American_norm)

bran = ax.plot(banded_spiny_norm.index, banded_spiny_norm)

cal = ax.plot(california_spiny_norm.index, california_spiny_norm)

carib = ax.plot(caribbean_spiny_norm.index, caribbean_spiny_norm)

#slip = ax.plot(slipper_norm.index, slipper_norm)

span = ax.plot(spanish_norm.index, spanish_norm)



plt.xlim(lob_year.index.min(),lob_year.index.max())
plt.grid(True)
plt.legend(['AMERICAN', 'BANDED SPINY', 'CALIFORNIA SPINY', 'CARIBBEAN SPINY', 'SPANISH'])

plt.title('Change in Weight Excluding Slipper')
plt.ylabel('Normalized Change')
plt.xlabel('Year')

fig.set_size_inches(8, 5)
fig.set_dpi(500)
plt.savefig('images/ChangeInWeight')
plt.show();


