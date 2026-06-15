#!/usr/bin/env python3
import sys
import requests

BASE = "http://localhost:5001"

steps = [
    ("/loader/load",           {
        "csv_path": "data/seeds_dataset.txt",
        "target_col": "Class",
        "col_names": ["area","perimeter","compactness","kernel_length","kernel_width","asymmetry_coef","groove_length","Class"]
    }),
    ("/cleaner/configure",     {}),
    ("/cleaner/fit_transform", {}),
    ("/encoder/configure",     {}),
    ("/encoder/fit_transform", {}),
    ("/kmeans/search",         {}),
    ("/kmeans/plot/elbow",     {}),
    ("/kmeans/fit",            {}),
    ("/kmeans/plot/pca2d",     {}),
    ("/kmeans/plot/profiles",  {}),
    ("/kmeans/plot/pairplot",  {}),
]

for path, body in steps:
    r = requests.post(BASE + path, json=body)
    print("OK " if r.ok else "ERRORE ", path)
    if not r.ok:
        print(r.text)
        sys.exit(1)

r = requests.get(BASE + "/kmeans/compare")
if r.ok:
    m = r.json()
    print(f"\nMetriche clustering:")
    print(f"  ARI:    {m['ari']}")
    print(f"  NMI:    {m['nmi']}")
    print(f"  Purity: {m['purity']}")
else:
    print("ERRORE /kmeans/compare:", r.text)

print("\nVisualizza i grafici nel browser:")
for p in requests.get(BASE + "/plots/").json():
    print(f"  {BASE}/plots/{p}")
