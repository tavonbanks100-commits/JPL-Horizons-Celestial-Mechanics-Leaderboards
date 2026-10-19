# leaderboard.py
# Use: python leaderboard.py
# Compares all planets to chosen center, prints exact closest times

from astroquery.jplhorizons import Horizons
from astropy.time import Time, TimeDelta
import pandas as pd

from horizons_core import exact_closest, centers

planets = {"Mercury":"199","Venus":"299","Earth":"399","Mars":"499",
           "Jupiter":"5","Saturn":"6","Uranus":"7","Neptune":"8","Pluto":"9"}

center_choice = input("Choose center [1=Earth]: ").strip() or "1"
center = centers.get(center_choice, "399")
days = int(input("Days ahead [730]: ") or "730")

start = Time.now(); AU_to_km = 149597870.7; SEC_PER_DAY = 86400; results = []

for name,pid in planets.items():
    print(f"Querying {name}...")
    times, dists, speeds = [], [], []
    for i in range(days):
        t = start + TimeDelta(i, format='jd')
        try:
            v = Horizons(id=pid, location=center, epochs=t.jd).vectors()
            dist = ((v['x'][0]**2+v['y'][0]**2+v['z'][0]**2)**0.5)*AU_to_km/1e6
            spd = ((v['vx'][0]**2+v['vy'][0]**2+v['vz'][0]**2)**0.5)*AU_to_km/SEC_PER_DAY
            times.append(t.isot); dists.append(dist); speeds.append(spd)
        except: pass
    t_ex,d_ex = exact_closest(times, dists)
    results.append({"Planet":name,"Closest":t_ex.strftime("%Y-%m-%d %H:%M"),"Distance_M_km":round(d_ex,3)})

df = pd.DataFrame(results).sort_values("Distance_M_km")
df.to_csv("leaderboard.csv", index=False)
print(df.to_string(index=False))