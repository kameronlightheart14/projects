# Kameron Lightheart
# 01/21/2020
# MATH 405

from scipy.stats.distributions import norm
from scipy.optimize import fmin
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARMA
from pydataset import data as pydata
from statsmodels.tsa.stattools import arma_order_select_ic as order_select
import pandas as pd

def arma_forecast_naive(file='weather.npy',p=2,q=1,n=20):
    """
    Perform ARMA(1,1) on data. Let error terms be drawn from
    a standard normal and let all constants be 1.
    Predict n values and plot original data with predictions.

    Parameters:
        file (str): data file
        p (int): order of autoregressive model
        q (int): order of moving average model
        n (int): number of future predictions
    """
    # Load the data
    data = np.load(file)
    N = len(data)
    # Compute time series (differences of data points)
    data = np.array([data[t] - data[t-1] for t in range(1, N)])
    N = len(data)

    # Create empty array to fill with predictions
    Z = np.zeros(n+2)

    # Adjustable parameters
    phi, theta = 0.5, 0.1

    # Grab normally distributed epsilon
    epsilon = norm(0, 1).rvs(n+2)
    Z[:2] = data[N-2:]
    
    # Make predictions using ARMA formula
    for i in range(2, n+2):
        phi_vals = np.sum([phi * Z[i-j] for j in range(1, p+1)])
        theta_vals = np.sum([theta * epsilon[i-j] for j in range(2,q+2)])
        Z[i] = phi_vals + epsilon[i-1] + theta_vals

    # Plot the data along with the predictions
    domain = np.arange(N, N+n)
    plt.plot(domain, Z[2:], label="Predictions")
    plt.plot(data, label="Actual")
    plt.xlabel("t")
    plt.ylabel("Z_t")
    plt.legend()
    plt.title("ARMA({},{}) Naive Forcast".format(p, q))
    plt.show()

def arma_likelihood(file='weather.npy', phis=np.array([0]), thetas=np.array([0]), mu=0., std=1.):
    """
    Transfer the ARMA model into state space. 
    Return the log-likelihood of the ARMA model.

    Parameters:
        file (str): data file
        phis (ndarray): coefficients of autoregressive model
        thetas (ndarray): coefficients of moving average model
        mu (float): mean of errorm
        std (float): standard deviation of error

    Return:
        log_likelihood (float)
    """
    # Load the data
    data = np.load(file)
    N = len(data)
    # Compute time series (differences of data points)
    data = np.array([data[t] - data[t-1] for t in range(1, N)])
    N = len(data)

    # n = dim_states, m = dim_time_series
    F, Q, H, _, _ = state_space_rep(phis, thetas, mu, std)

    # Get x_k|k-1 and P_k|k-1 for each k <= N
    x, P = kalman(F, Q, H, data - mu)

    # Compute the log likelihood probability 
    prob = 0
    for i in range(N):
        normal = norm(H @ x[i] + mu, np.sqrt(H @ P[i] @ H.T))
        prob += np.log(normal.pdf(data[i]))
    
    return prob

def model_identification(file='weather.npy',p=4,q=4):
    """
    Identify parameters to minimize AIC of ARMA(p,q) model

    Parameters:
        file (str): data file
        p (int): maximum order of autoregressive model
        q (int): maximum order of moving average model

    Returns:
        phis (ndarray (p,)): coefficients for AR(p)
        thetas (ndarray (q,)): coefficients for MA(q)
        mu (float): mean of error
        std (float): std of error
    """
    # Load the data and compute differences (time series)
    data = np.load(file)
    N = len(data)
    time_series = np.array([data[t] - data[t-1] for t in range(1, N)])
    n = len(time_series)

    likelihood_dict = dict()
    p_q_dict = dict()

    for p in range(1, p):
        for q in range(1, q):
            # assume p, q, and time_series are defined
            def f(x): # x contains the phis, thetas, mu, and std
                return -1*arma_likelihood(file, phis=x[:p], thetas=x[p:p+q], mu=x[-2],std=x[-1])

            # create initial point
            x0 = np.zeros(p+q+2)
            x0[-2] = time_series.mean()
            x0[-1] = time_series.std()

            # Use scipy optimize function to find optimal parameters
            sol = fmin(f,x0,maxiter=10000, maxfun=10000)
            
            # Compute the AIC
            k = 2 + p + q
            # Since f(sol) returns neg log likelihood, make it positive
            aic = 2 * k * (1 + ((k+1)/(n-k))) + 2 * f(sol)

            # Add optimal parameters and aic to dictionaries to find min later
            p_q_dict[(p,q)] = sol
            likelihood_dict[(p,q)] = aic

    # Find parameters p and q associated with the minimum aic
    p_q_val = min(likelihood_dict, key=lambda key: likelihood_dict[key])
    
    # Use the other dictionary to return the parameters associated
    return p_q_dict[p_q_val]
        


def arma_forecast(file='weather.npy', phis=np.array([0]), thetas=np.array([0]), mu=0., std=0., n=30):
    """
    Forecast future observations of data.
    
    Parameters:
        file (str): data file
        phis (ndarray (p,)): coefficients of AR(p)
        thetas (ndarray (q,)): coefficients of MA(q)
        mu (float): mean of ARMA model
        std (float): standard deviation of ARMA model
        n (int): number of forecast observations

    Returns:
        new_mus (ndarray (n,)): future means
        new_covs (ndarray (n,)): future standard deviations
    """
    # Load the data
    data = np.load(file)
    N = len(data)
    # Compute time series (differences of data points)
    data = np.array([data[t] - data[t-1] for t in range(1, N)])
    N = len(data)

    # n = dim_states, m = dim_time_series
    F, Q, H, _, _ = state_space_rep(np.array([phis]), np.array([thetas]), mu, std)

    # Get x_k|k-1 and P_k|k-1 for each k <= N
    x, P = kalman(F, Q, H, data - mu)

    # Update step
    y = data[-1] - H @ x[-1]
    S_k = H @ P[-1] @ H.T + std
    K_k = P[-1] @ H.T @ np.linalg.inv(S_k)
    x_given = x[-1] + K_k @ y
    P_given = (np.eye(len(K_k)) - K_k @ H) @ P[-1]

    # Predictive step
    pred = np.zeros((n,len(x_given)))
    pred[0] = F @ x_given 
    pred_P = np.zeros_like(P)
    pred_P[0] = F @ P_given @ F.T + Q
    Z = np.zeros(n)
    var = np.zeros(n)
    for i in range(1, n):
        # Predict
        pred[i] = F @ pred[i-1] 
        pred_P[i] = F @ pred_P[i-1] @ F.T + Q
        Z[i] = H @ pred[i]
        var[i] = H @ pred_P[i] @ H.T

    # Plot the data
    plt.figure()
    domain = np.arange(N+1, N+n)
    var = np.sqrt(var)
    plt.plot(domain, Z[1:], 'y--', label="forecast")
    plt.plot(domain, Z[1:] + 2*var[1:], 'r', label=r'95 % Confidence Interval')
    plt.plot(domain, Z[1:] - 2*var[1:], 'r')
    plt.plot(data, label="Actual")
    plt.xlabel("t")
    plt.ylabel("Z_t")
    plt.legend()
    plt.title(r"ARMA Mean Forcast w/ 95% confidence interval")
    plt.show()

    return Z, var

def sm_arma(file = 'weather.npy', p=4, q=4, n=30):
    """
    Build an ARMA model with statsmodel and 
    predict future n values.

    Parameters:
        file (str): data file
        p (int): maximum order of autoregressive model
        q (int): maximum order of moving average model
        n (int): number of values to predict

    Return:
        aic (float): aic of optimal model
    """
    # Load the data
    data = np.load(file)
    N = len(data)
    # Compute time series (differences of data points)
    data = np.array([data[t] - data[t-1] for t in range(1, N)])
    N = len(data)

    # Compute the optimal p, q using aic
    params = order_select(data, p, q, ic=['aic'])
    p, q = params.aic_min_order

    # Use statsmodels ARMA model to make predictions
    model = ARMA(data,order=(p,q))
    result = model.fit(method='mle', trend='c')
    pred = result.predict(start=0,end=len(data)+n)

    # Plot the predictions
    plt.plot(data, label="Actual")
    plt.plot(pred, label='Prediction')
    plt.title("Statsmodel ARMA(1,1)")
    plt.xlabel("Day of Month")
    plt.ylabel("Change in Temp (C) - mu=0")
    plt.legend()

    return result.aic

def manaus(start='1983-01-31',end='1995-01-31',p=4,q=4):
    """
    Plot the ARMA(p,q) model of the River Negro height
    data using statsmodels built-in ARMA class.

    Parameters:
        start (str): the data at which to begin forecasting
        end (str): the date at which to stop forecasting
        p (int): max_ar parameter
        q (int): max_ma parameter
    Return:
        aic_min_order (tuple): optimal order based on AIC
        bic_min_order (tuple): optimal order based on BIC
    """
    # Get dataset
    raw = pydata('manaus')
    # Make DateTimeIndex
    manaus = pd.DataFrame(raw.values,index=pd.date_range('1903-01','1993-01',freq='M'))
    manaus = manaus.drop(0,axis=1)

    # Reset column names
    manaus.columns = ['Water Level']

    data = manaus.values

    # Get the best params under aic
    params = order_select(data, p, q, ic=['aic', 'bic'])
    p1, q1 = params.aic_min_order

    # Make predictions using statsmodels ARMA model
    model = ARMA(manaus,order=(p1,q1))
    result1 = model.fit(method='mle', trend='c')

    # Plot predictions
    fig, ax = plt.subplots(figsize=(13,7))
    fig = result1.plot_predict(start=start, end=end, ax=ax)
    ax.set_title('Sunspot Dataset')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sunspots')

    # Get the best params using bic
    p, q = params.bic_min_order

    # Use statsmodel ARMA model to predict 
    model = ARMA(manaus,order=(p,q))
    result2 = model.fit(method='mle', trend='c')

    # Plot the predictions
    fig, ax = plt.subplots(figsize=(13,7))
    fig = result2.plot_predict(start=start, end=end, ax=ax)
    ax.set_title('Sunspot Dataset')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Sunspots')

    plt.show()

    return (p1, q1), (p, q)
    

###############################################################################
    
def kalman(F, Q, H, time_series):
    # Get dimensions
    dim_states = F.shape[0]

    # Initialize variables
    # covs[i] = P_{i | i-1}
    covs = np.zeros((len(time_series), dim_states, dim_states))
    mus = np.zeros((len(time_series), dim_states))

    # Solve of for first mu and cov
    covs[0] = np.linalg.solve(np.eye(dim_states**2) - np.kron(F,F),np.eye(dim_states**2)).dot(Q.flatten()).reshape(
            (dim_states,dim_states))
    mus[0] = np.zeros((dim_states,))

    # Update Kalman Filter
    for i in range(1, len(time_series)):
        t1 = np.linalg.solve(H.dot(covs[i-1]).dot(H.T),np.eye(H.shape[0]))
        t2 = covs[i-1].dot(H.T.dot(t1.dot(H.dot(covs[i-1]))))
        covs[i] = F.dot((covs[i-1] - t2).dot(F.T)) + Q
        mus[i] = F.dot(mus[i-1]) + F.dot(covs[i-1].dot(H.T.dot(t1))).dot(
                time_series[i-1] - H.dot(mus[i-1]))
    return mus, covs

def state_space_rep(phis, thetas, mu, sigma):
    # Initialize variables
    dim_states = max(len(phis), len(thetas)+1)
    dim_time_series = 1 #hardcoded for 1d time_series

    F = np.zeros((dim_states,dim_states))
    Q = np.zeros((dim_states, dim_states))
    H = np.zeros((dim_time_series, dim_states))

    # Create F
    F[0][:len(phis)] = phis
    F[1:,:-1] = np.eye(dim_states - 1)
    # Create Q
    Q[0][0] = sigma**2
    # Create H
    H[0][0] = 1.
    H[0][1:len(thetas)+1] = thetas

    return F, Q, H, dim_states, dim_time_series