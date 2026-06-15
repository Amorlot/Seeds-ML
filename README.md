# Seeds ML — Unsupervised Clustering Pipeline

Progetto di Machine Learning non supervisionato sul dataset UCI Seeds.  
Identifica automaticamente le 3 varietà di grano (Kama, Rosa, Canadian) tramite K-Means clustering, senza usare le etichette durante il training.

**Autori:** Andrea Morlotti, Cerea Gianluca — 2025/26

---

## Struttura del progetto

```
Seeds-ML/
├── data/
│   └── seeds_dataset.txt       # Dataset UCI Seeds (210 campioni, 7 feature)
├── lib/
│   ├── loader.py               # GenericLoader  — carica CSV o dataset UCI
│   ├── eda.py                  # GenericEda     — statistiche e correlazioni
│   ├── cleaner.py              # GenericCleaner — imputa valori mancanti
│   ├── encoder.py              # GenericEncoder — scaling e encoding
│   ├── kmeans.py               # KMeansModel    — clustering, metriche, profili
│   ├── plots.py                # KMeansPlotter  — grafici PNG
│   └── api/                    # Blueprint Flask per ogni componente
│       ├── state.py            # Stato condiviso della pipeline API
│       ├── loader.py
│       ├── eda.py
│       ├── cleaner.py
│       ├── encoder.py
│       ├── kmeans.py
│       └── plots.py
├── main.py                     # Pipeline batch completa (stampa tutto a console)
├── app.py                      # Server Flask con REST API
├── run_pipeline.py             # Esegue la pipeline via chiamate HTTP
├── config.yaml                 # Unico punto di configurazione
├── Dockerfile
└── requirements.txt
```

---

## Avvio rapido

### Pipeline batch (via Docker)

```bash
docker build -t seeds-ml .
docker run -v $(pwd)/output:/app/output seeds-ml
```

Esegue l'intera pipeline e salva i grafici in `output/`.

### REST API (via Docker)

```bash
# Avvia il server Flask
docker run -p 5001:5001 -v $(pwd)/output:/app/output seeds-ml python app.py

# In un altro terminale, esegui la pipeline via HTTP
python run_pipeline.py
```

---

## Configurazione

Tutto il comportamento è controllato da `config.yaml`:

```yaml
loader:
  csv_path: data/seeds_dataset.txt
  target_col: Class

cleaner:
  num_strategy: median       # median | mean | most_frequent

encoder:
  num_strategy: standard     # standard | minmax | none

kmeans:
  k_min: 2
  k_max: 10
  best_k: 3                  # null = auto (silhouette), int = forzato
  random_state: 42
  n_init: 10

output:
  plots_dir: output/
```

Per cambiare dataset basta modificare `csv_path`, `target_col` e `col_names` — la libreria `lib/` è generica e funziona su qualsiasi dataset tabellare.

---

## Pipeline

```
Loader → EDA → Cleaner → Encoder → KMeans search k → KMeans fit → Metriche → Plot
```

Il target (`Class`) viene caricato ma **non usato durante il training**.  
Serve solo per la valutazione esterna post-fit (ARI, NMI, Purity).

---

## REST API

Il server Flask espone i seguenti endpoint:

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/loader/load` | Carica il dataset |
| GET  | `/loader/info` | Info sul dataset caricato |
| GET  | `/eda/summary` | Statistiche descrittive |
| GET  | `/eda/correlation` | Matrice di correlazione |
| POST | `/cleaner/configure` | Configura la pulizia |
| POST | `/cleaner/fit_transform` | Imputa valori mancanti |
| POST | `/encoder/configure` | Configura lo scaling |
| POST | `/encoder/fit_transform` | Scala le feature |
| POST | `/kmeans/search` | Elbow + Silhouette per k in [k_min, k_max] |
| POST | `/kmeans/fit` | Fit con il k scelto |
| GET  | `/kmeans/compare` | ARI, NMI, Purity vs etichette reali |
| GET  | `/kmeans/profiles` | Profili medi dei cluster |
| POST | `/kmeans/plot/elbow` | Genera grafico elbow + silhouette |
| POST | `/kmeans/plot/pca2d` | Genera scatter PCA 2D |
| POST | `/kmeans/plot/profiles` | Genera heatmap profili cluster |
| POST | `/kmeans/plot/pairplot` | Genera pairplot feature |
| GET  | `/plots/` | Lista dei PNG generati |
| GET  | `/plots/<file>` | Scarica un PNG |

---

## Risultati (k=3, StandardScaler)

| Metrica | Valore |
|---------|--------|
| Silhouette | 0.4007 |
| ARI | 0.7733 |
| NMI | 0.7279 |
| Purity | 0.919 |
| Inertia | 430.66 |

k=3 è stato scelto perché l'elbow method indica un cambio di pendenza dell'inertia a k=3, che corrisponde alle 3 varietà biologiche reali. La silhouette è massima a k=2 (0.4658) ma fonderebbe due varietà distinte in un unico cluster.

---

## Grafici generati

| File | Contenuto |
|------|-----------|
| `elbow_silhouette.png` | Inertia vs k (elbow) e Silhouette vs k |
| `pca2d.png` | Scatter PCA 2D: cluster assegnati (sx) vs varietà reali (dx) |
| `cluster_profiles.png` | Heatmap delle medie delle feature per cluster |
| `pairplot.png` | Scatter plot per ogni coppia di feature, colorato per cluster |

---

## Libreria `lib/`

I componenti in `lib/` sono generici e riutilizzabili su qualsiasi dataset tabellare, non solo Seeds. Ogni classe segue il pattern `configure → fit → transform` di scikit-learn.

Per usare la libreria su un nuovo dataset è sufficiente aggiornare `config.yaml`.

---

## Dipendenze

```
pandas==2.2.0
numpy==1.26.4
matplotlib==3.8.2
seaborn==0.13.2
scikit-learn==1.4.0
ucimlrepo==0.0.3
pyyaml==6.0.1
flask==3.0.0
requests==2.31.0
```
