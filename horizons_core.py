# horizons_core.py
# Shared dictionaries and math for all your Horizons tools
# Put this in the same folder as horizons_any.py and leaderboard.py

from datetime import datetime, timedelta
import numpy as np

# --- bodies ---
bodies = {
    "mercury":"199","venus":"299","earth":"399","mars":"499",
    "jupiter":"5","saturn":"6","uranus":"7","neptune":"8","pluto":"9",
    "moon":"301","luna":"301",
    "voyager 1":"-31","voyager1":"-31",
    "voyager 2":"-32","voyager2":"-32",
    "199":"199","299":"299","399":"399","499":"499",
    "5":"5","6":"6","7":"7","8":"8","9":"9",
    "301":"301","-31":"-31","-32":"-32"
}
names = {
    "199":"Mercury","299":"Venus","399":"Earth","499":"Mars",
    "5":"Jupiter","6":"Saturn","7":"Uranus","8":"Neptune","9":"Pluto",
    "301":"Moon","-31":"Voyager 1","-32":"Voyager 2"
}

# --- centers ---
centers = {
    "1":"399","2":"@sun","3":"301","4":"499","5":"5",
    "6":"6","7":"7","8":"8","9":"9","10":"@0"
}
center_names = {
    "399":"Earth","@sun":"Sun","301":"Moon","499":"Mars",
    "5":"Jupiter","6":"Saturn","7":"Uranus","8":"Neptune",
    "9":"Pluto","@0":"SSB"
}

# --- exact time using derivative ---
def exact_extreme(dates_iso, values, mode="min"):
    idx = values.index(min(values) if mode=="min" else max(values))
    if idx==0 or idx==len(values)-1:
        return datetime.fromisoformat(dates_iso[idx]), values[idx]
    x = np.array([-1,0,1]); y = np.array(values[idx-1:idx+2])
    a,b,c = np.polyfit(x,y,2); x_ext = -b/(2*a)
    base = datetime.fromisoformat(dates_iso[idx])
    return base + timedelta(days=float(x_ext)), a*x_ext**2 + b*x_ext + c

def exact_closest(dates, distances):
    """for leaderboard compatibility"""
    return exact_extreme(dates, distances, "min")