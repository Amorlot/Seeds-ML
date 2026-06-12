pipeline = {
    "loader": None,
    "cleaner": None,
    "encoder": None,
    "km": None,
    "X_clean": None,        # DataFrame features pulite (scala originale)
    "X_scaled": None,       # ndarray scalato, input per K-Means
    "y": None,              # etichette reali (solo per confronto)
    "search_results": None, # dict k -> {inertia, silhouette}
}
