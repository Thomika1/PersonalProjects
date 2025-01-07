import numpy as np
from math import log, e
from scipy import stats


def calcula_b_s(stock_price, strike_price, time, vol, dividend = 0.0, rate=0.0):

        d1 = (log(stock_price/strike_price)+(rate-dividend+vol**2/2)*time)/(vol*time**.5)
        d2 = d1 - vol*time**.5
        
        call = stats.norm.cdf(d1) * stock_price*e**(-dividend*time)-stats.norm.cdf(d2)*strike_price*e**(-rate*time)
        put = stats.norm.cdf(-d2)*strike_price*e**(-rate*time)-stats.norm.cdf(-d1)*stock_price*e**(-dividend*time)
        
        return [call, put, d1, d2]
    
def delta_calc(d1): # calcula delta para call e para put
        "Calcula delta"
        
        delta_call = stats.norm.cdf(d1,0,1)
        
        delta_put = -stats.norm.cdf(-d1,0,1)
         
        return [delta_call, delta_put]
    
def gamma_calc(d1, stock_price, vol, time): # calcula gamma 
        "Calcula gamma"
        
        gamma = stats.norm.pdf(d1,0,1)/(stock_price*vol*np.sqrt(time))
        
        return gamma
        
def vega_calc( d1, stock_price, time):
        "calcula vega"
        
        vega = stock_price*stats.norm.pdf(d1,0,1)*np.sqrt(time)
        
        return vega*0.01
        
def theta_calc( d1, d2, stock_price, strike_price, time, rate, vol):
        "calcula theta"
        
        theta_call = -stock_price*stats.norm.pdf(d1,0,1)*vol/(2*np.sqrt(time)) - rate*stock_price*np.exp(-rate*time)*stats.norm.cdf(d2,0,1)
        
        theta_put = -stock_price*stats.norm.pdf(d1,0,1)*vol/(2*np.sqrt(time)) + rate*stock_price*np.exp(-rate*time)*stats.norm.cdf(-d2,0,1)
        
        return [theta_call/365 , theta_put/365 ]
    
def rho_calc( d2, strike_price, time, rate):
        "calcula roh"
        
        rho_call = strike_price*time*np.exp(-rate*time)*stats.norm.cdf(d2,0,1)
        
        rho_put = -strike_price*time*np.exp(-rate*time)*stats.norm.cdf(-d2,0,1)
        
        return [rho_call*0.01, rho_put*0.01]




