import pandas as pd
import numpy as np

# check if the library folder already exists, to avoid building everytime you load the pahe
# import streamlit as st
import requests
import os
import sys
import subprocess
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("ls -la /app/equity/")
    # build
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    # install
    os.system("make install")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib as ta
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/lib/", "--global-option=-I/home/appuser/include/", "ta-lib"])
finally:
    import talib as ta

    
def format_date(df):
    format = '%Y-%m-%d %H:%M:%S'
    df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format=format)
    df = df.set_index(pd.DatetimeIndex(df['Datetime']))
    df = df.drop('Datetime', axis=1)
    
    return df

# https://stackoverflow.com/questions/39684548/convert-the-string-2-90k-to-2900-or-5-2m-to-5200000-in-pandas-dataframe
def replace_vol(df):
    df.volume = (df.volume.replace(r'[KM]+$', '', regex=True).astype(float) * \
                df.volume.str.extract(r'[\d\.]+([KM]+)', expand=False)
                .fillna(1)
                .replace(['K','M'], [10**3, 10**6]).astype(int))
    return df

def get_all_features(df):
    #get_overlap_studies
    # BBANDS - Bollinger Bands
    df['bbub'], df['bbmb'], df['bblb'] = ta.BBANDS(df['close'])

    # DEMA - Double Exponential Moving Average
    df['DEMA_100'] = ta.DEMA(df['close'],timeperiod=100)
    df['DEMA_30'] = ta.DEMA(df['close'],timeperiod=30)
    df['DEMA_5'] = ta.DEMA(df['close'],timeperiod=5)

    # EMA - Exponential Moving Average
    df['EMA_100'] = ta.EMA(df['close'],timeperiod=100)
    df['EMA_30'] = ta.EMA(df['close'],timeperiod=30)
    df['EMA_5'] = ta.EMA(df['close'],timeperiod=5)

    # HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    df['HT_TRENDLINE'] = ta.HT_TRENDLINE(df['close'])

    # KAMA - Kaufman Adaptive Moving Average
    df['KAMA'] = ta.KAMA(df['close'])

    # MA - Moving average
    df['MA_100'] = ta.MA(df['close'],timeperiod=100)
    df['MA_30'] = ta.MA(df['close'],timeperiod=30)
    df['MA_5'] = ta.MA(df['close'],timeperiod=5)

    # MAMA - MESA Adaptive Moving Average
    df['MAMA'], df['FAMA'] = ta.MAMA(df['close'])

    # MIDPOINT - MidPoint over period
    df['MIDPOINT'] = ta.MIDPOINT(df['close'])

    # MIDPRICE - Midpoint Price over period
    df['MIDPRICE'] = ta.MIDPRICE(df.high, df.low, timeperiod=14)

    # SAR - Parabolic SAR
    df['SAR'] = ta.SAR(df.high, df.low, acceleration=0, maximum=0)

    # SAREXT - Parabolic SAR - Extended
    df['SAREXT'] = ta.SAREXT(df.high, df.low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)

    # SMA - Simple Moving Average
    df['SMA_100'] = ta.SMA(df['close'],timeperiod=100)
    df['SMA_30'] = ta.SMA(df['close'],timeperiod=30)
    df['SMA_5'] = ta.SMA(df['close'],timeperiod=5)

    # T3 - Triple Exponential Moving Average (T3)
    df['T3'] = ta.T3(df.close, timeperiod=5, vfactor=0)

    # TEMA - Triple Exponential Moving Average
    df['TEMA_100'] = ta.TEMA(df['close'],timeperiod=100)
    df['TEMA_30'] = ta.TEMA(df['close'],timeperiod=30)
    df['TEMA_5'] = ta.TEMA(df['close'],timeperiod=5)

    # TRIMA - Triangular Moving Average
    df['TRIMA_100'] = ta.TRIMA(df['close'],timeperiod=100)
    df['TRIMA_30'] = ta.TRIMA(df['close'],timeperiod=30)
    df['TRIMA_5'] = ta.TRIMA(df['close'],timeperiod=5)

    # WMA - Weighted Moving Average
    df['WMA_100'] = ta.WMA(df['close'],timeperiod=100)
    df['WMA_30'] = ta.WMA(df['close'],timeperiod=30)
    df['WMA_5'] = ta.WMA(df['close'],timeperiod=5)


    #get_momentum_indicator
    # ADX - Average Directional Movement Index
    df['ADX'] =  ta.ADX(df.high, df.low, df.close, timeperiod=14)

    # ADXR - Average Directional Movement Index Rating
    df['ADXR'] = ta.ADXR(df.high, df.low, df.close, timeperiod=14)

    # APO - Absolute Price Oscillator
    df['APO'] = ta.APO(df.close, fastperiod=12, slowperiod=26, matype=0)

    # AROON - Aroon
    df['AROON_DWN'],df['AROON_UP'] = ta.AROON(df.high, df.low, timeperiod=14)

    # AROONOSC - Aroon Oscillator
    df['AROONOSC'] = ta.AROONOSC(df.high, df.low, timeperiod=14)

    # BOP - Balance Of Power
    df['BOP'] = ta.BOP(df.open, df.high, df.low, df.close)

    # CCI - Commodity Channel Index
    df['CCI'] = ta.CCI(df.high, df.low, df.close, timeperiod=14)

    # CMO - Chande Momentum Oscillator
    df['CMO']= ta.CMO(df.close, timeperiod=14)

    # DX - Directional Movement Index
    df['DX'] = ta.DX(df.high, df.low, df.close, timeperiod=14)

    # MACD - Moving Average Convergence/Divergence
    df['MACD'], df['MACD_SGNL'], df['MACD_HIST'] = ta.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)

    # MACDFIX - Moving Average Convergence/Divergence Fix 12/26
    df['MACDF'], df['MACDF_SGNL'], df['MACDF_HIST'] = ta.MACDFIX(df.close)

    # MFI - Money Flow Index
    df['MFI'] = ta.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)

    # MINUS_DI - Minus Directional Indicator
    df['MINUS_DI'] = ta.MINUS_DI(df.high, df.low, df.close, timeperiod=14)

    # MINUS_DM - Minus Directional Movement
    df['MINUS_DM'] = ta.MINUS_DM(df.high, df.low, timeperiod=14)

    # MOM - Momentum
    df['MOM'] = ta.MOM(df.close, timeperiod=10)

    # PLUS_DI - Plus Directional Indicator
    df['PLUS_DI'] = ta.PLUS_DI(df.high, df.low, df.close, timeperiod=14)

    # PLUS_DM - Plus Directional Indicator
    df['PLUS_DM'] = ta.PLUS_DM(df.high, df.low, timeperiod=14)

    # PPO - Percentage Price Oscillator
    df['PPO'] = ta.PPO(df.close, fastperiod=12, slowperiod=26, matype=0)

    # ROC - Rate of change : ((price/prevPrice)-1)*100
    df['ROC'] = ta.ROC(df.close, timeperiod=10)

    # ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
    df['ROCP'] = ta.ROCP(df.close, timeperiod=10)

    # ROCR - Rate of change Percentage: (price-prevPrice)/prevPrice
    df['ROCR'] = ta.ROCR(df.close, timeperiod=10)

    # ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
    df['ROCR100'] = ta.ROCR100(df.close, timeperiod=10)

    # RSI - Relative Strength Index
    df['RSI'] = ta.RSI(df.close, timeperiod=14)

    # STOCH - Stochastic
    df['STOCH_SLWK'], df['STOCH_SLWD'] = ta.STOCH(df.high, df.low, df.close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    # STOCHF - Stochastic Fast
    df['STOCH_FSTK'], df['STOCH_FSTD'] = ta.STOCHF(df.high, df.low, df.close, fastk_period=5, fastd_period=3, fastd_matype=0)

    # STOCHRSI - Stochastic Relative Strength Index
    df['STOCHRSI_FSTK'], df['STOCHRSI_FSTD'] = ta.STOCHRSI(df.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

    # TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
    df['TRIX'] = ta.TRIX(df.close, timeperiod=30)

    # ULTOSC - Ultimate Oscillator
    df['ULTOSC'] = ta.ULTOSC(df.high, df.low, df.close, timeperiod1=7, timeperiod2=14, timeperiod3=28)

    # WILLR - Williams' %R
    df['WILLR'] = ta.WILLR(df.high, df.low, df.close, timeperiod=14)


    # get_volume_indicator
    # AD - Chaikin A/D Line
    df['AD'] = ta.AD(df.high, df.low, df.close, df.volume)

    # ADOSC - Chaikin A/D Oscillator
    df['ADOSC'] = ta.ADOSC(df.high, df.low, df.close, df.volume, fastperiod=3, slowperiod=10)

    # OBV - On Balance Volume
    df['OBV'] = ta.OBV(df.close, df.volume)


    # get_volatility_indicator
    # ATR - Average True Range
    df['ATR'] = ta.ATR(df.high, df.low, df.close, timeperiod=14)

    # NATR - Normalized Average True Range
    df['NATR'] = ta.NATR(df.high, df.low, df.close, timeperiod=14)

    # TRANGE - True Range
    df['TRANGE'] = ta.TRANGE(df.high, df.low, df.close)


    # get_transform_price
    # AVGPRICE - Average Price
    df['AVGPRICE'] = ta.AVGPRICE(df.open, df.high, df.low, df.close)

    # MEDPRICE - Median Price
    df['MEDPRICE'] = ta.MEDPRICE(df.high, df.low)

    # TYPPRICE - Typical Price
    df['TYPPRICE'] = ta.TYPPRICE(df.high, df.low, df.close)

    # WCLPRICE - Weighted Close Price
    df['WCLPRICE'] = ta.WCLPRICE(df.high, df.low, df.close)


    # get_cycle_indicator
    # HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
    df['HT_DCPERIOD'] = ta.HT_DCPERIOD(df.close)

    # HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
    df['HT_DCPHASE'] = ta.HT_DCPHASE(df.close)

    # HT_PHASOR - Hilbert Transform - Phasor Components
    df['HT_PHASOR_IP'], df['HT_PHASOR_QD'] = ta.HT_PHASOR(df.close)

    # HT_SINE - Hilbert Transform - SineWave
    df['HT_SINE'], df['HT_SINE_LEADSINE'] = ta.HT_SINE(df.close)

    # HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
    df['HT_TRENDMODE'] = ta.HT_TRENDMODE(df.close)

    return df

def feature_main(df):
    df['time'] = df['time'].map(lambda x: np.sum(list(map(int, str(x).split(':')))))

    df = get_all_features(df)
    values = {}
    for col in df.columns:
        idx = df.reset_index()[col].first_valid_index()
        values[col] = df.iloc[idx][col]
    df = df.fillna(value=values)
    return df