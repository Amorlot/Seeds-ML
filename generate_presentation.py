#!/usr/bin/env python3
"""Genera seeds_presentation.pptx — stile Titanic."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY     = RGBColor(0x0d, 0x1b, 0x4b)
NAVY_MID = RGBColor(0x1c, 0x30, 0x68)
ORANGE   = RGBColor(0xf5, 0x92, 0x1e)
TEAL     = RGBColor(0x1a, 0x7a, 0x7a)
WHITE    = RGBColor(0xff, 0xff, 0xff)
LGRAY    = RGBColor(0xd0, 0xd8, 0xf0)
B_BLUE   = RGBColor(0x1e, 0x3a, 0x7a)
B_TEAL   = RGBColor(0x1a, 0x6a, 0x6a)
B_GRN    = RGBColor(0x1a, 0x72, 0x40)
B_ORA    = RGBColor(0xb0, 0x55, 0x08)
B_PUR    = RGBColor(0x52, 0x22, 0x80)
B_RED    = RGBColor(0x80, 0x18, 0x18)
B_DARK   = RGBColor(0x0d, 0x22, 0x52)
CREAM    = RGBColor(0xf8, 0xf4, 0xe0)

SW = Inches(13.33)
SH = Inches(7.5)


# ── Helpers ───────────────────────────────────────────────────────────────────

def new_prs():
    p = Presentation()
    p.slide_width  = SW
    p.slide_height = SH
    return p

def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])

def bg(slide, c=NAVY):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = c

def rct(slide, l, t, w, h, fill=None, line=None, lw=Pt(1)):
    """Rettangolo. fill=None → trasparente. line=None → bordo invisibile."""
    shp = slide.shapes.add_shape(1, l, t, w, h)
    if fill is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line is not None:
        shp.line.color.rgb = line
        shp.line.width = lw
    else:
        shp.line.color.rgb = fill if fill else NAVY
        shp.line.width = Pt(0)
    return shp

def tb(slide, l, t, w, h, text, sz=Pt(13), c=WHITE, bold=False,
       align=PP_ALIGN.LEFT, italic=False, wrap=True):
    """Casella di testo con supporto \\n → paragrafo."""
    box = slide.shapes.add_textbox(l, t, w, h)
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    for i, line in enumerate(text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line.strip() or i == 0:
            r = p.add_run()
            r.text = line
            r.font.size = sz
            r.font.color.rgb = c
            r.font.bold = bold
            r.font.italic = italic
    return box

def hdr(slide, title, subtitle=""):
    """Header standard: titolo + sottotitolo + linee arancione/teal."""
    tb(slide, Inches(0.4), Inches(0.1), Inches(12.5), Inches(0.75),
       title, sz=Pt(30), bold=True)
    if subtitle:
        tb(slide, Inches(0.4), Inches(0.8), Inches(12.5), Inches(0.42),
           subtitle, sz=Pt(14), italic=True, c=LGRAY)
    rct(slide, Inches(0), Inches(1.28), SW, Inches(0.065), fill=ORANGE, lw=Pt(0))
    rct(slide, Inches(0), Inches(1.345), SW, Inches(0.035), fill=TEAL, lw=Pt(0))

def pgn(slide, n):
    tb(slide, Inches(12.8), Inches(7.18), Inches(0.48), Inches(0.28),
       str(n), sz=Pt(10), c=LGRAY, align=PP_ALIGN.RIGHT)


# ── Slide 1 — Titolo ──────────────────────────────────────────────────────────

def s_title(prs):
    s = blank(prs); bg(s)
    tb(s, Inches(0.5), Inches(0.75), Inches(12.3), Inches(1.3),
       "SEEDS CLUSTERING", sz=Pt(54), bold=True, align=PP_ALIGN.CENTER)
    tb(s, Inches(0.5), Inches(2.0), Inches(12.3), Inches(0.65),
       "Machine Learning Pipeline — Unsupervised Pattern Discovery",
       sz=Pt(20), italic=True, c=LGRAY, align=PP_ALIGN.CENTER)
    rct(s, Inches(0), Inches(2.75), SW, Inches(0.07), fill=ORANGE, lw=Pt(0))
    rct(s, Inches(0), Inches(2.82), SW, Inches(0.04), fill=TEAL,   lw=Pt(0))
    tb(s, Inches(0.5), Inches(3.0), Inches(12.3), Inches(0.5),
       "KMeans  |  KMedoids  |  REST API  |  Metrica Generica  |  Libreria Riutilizzabile",
       sz=Pt(14), c=LGRAY, align=PP_ALIGN.CENTER)
    stats = [("210","Campioni"), ("7","Feature"), ("3","Varieta' di grano"), ("k=3","Cluster ottimali")]
    bw, bh, gap = Inches(2.6), Inches(1.35), Inches(0.3)
    sx = Inches(1.1)
    for i, (val, lbl) in enumerate(stats):
        x = sx + i*(bw+gap)
        rct(s, x, Inches(4.65), bw, bh, line=NAVY_MID, lw=Pt(1.5))
        tb(s, x, Inches(4.7), bw, Inches(0.7), val, sz=Pt(40), bold=True, c=ORANGE, align=PP_ALIGN.CENTER)
        tb(s, x, Inches(5.42), bw, Inches(0.45), lbl, sz=Pt(13), align=PP_ALIGN.CENTER)
    tb(s, Inches(0), Inches(7.08), SW, Inches(0.3),
       "2025/26  |  Andrea Morlotti  Riccardo Scampini", sz=Pt(11), c=LGRAY, align=PP_ALIGN.CENTER)


# ── Slide 2 — Indice ──────────────────────────────────────────────────────────

def s_index(prs):
    s = blank(prs); bg(s)
    hdr(s, "Indice", "Struttura della presentazione")
    pgn(s, 2)
    items = [
        ("01","Il Problema",          "UCI Seeds e obiettivo clustering"),
        ("02","Architettura",         "Docker, REST API, config.yaml"),
        ("03","Libreria lib/",        "Componenti generici riutilizzabili"),
        ("04","Data Pipeline",        "Sequenza completa dei transformer"),
        ("05","Supervised vs Unsp.",  "Due paradigmi a confronto"),
        ("06","Algoritmo KMeans",     "Lloyd, k-means++, convergenza"),
        ("07","Scelta di K",          "Elbow method e Silhouette score"),
        ("08","Metriche Clustering",  "ARI, NMI, Purity"),
        ("09","Metrica Generica",     "Factory: KMeans/KMedoids/KModes"),
        ("10","Risultati",            "Performance su Seeds"),
        ("11","Visualizzazioni",      "PCA 2D, profili, pairplot"),
        ("12","Prossimi Passi",       "Clustering gerarchico, DBSCAN"),
    ]
    bw, bh, gx, gy = Inches(2.95), Inches(1.52), Inches(0.2), Inches(0.2)
    sx, sy = Inches(0.25), Inches(1.55)
    for i, (num, title, desc) in enumerate(items):
        r, c = divmod(i, 4)
        x = sx + c*(bw+gx)
        y = sy + r*(bh+gy)
        rct(s, x, y, bw, bh, line=B_BLUE, lw=Pt(1))
        rct(s, x, y, Inches(0.55), bh, fill=B_BLUE)
        tb(s, x, y+Inches(0.45), Inches(0.55), Inches(0.6),
           num, sz=Pt(15), bold=True, align=PP_ALIGN.CENTER)
        tb(s, x+Inches(0.62), y+Inches(0.1), bw-Inches(0.72), Inches(0.48),
           title, sz=Pt(13), bold=True)
        tb(s, x+Inches(0.62), y+Inches(0.62), bw-Inches(0.72), Inches(0.78),
           desc, sz=Pt(11), c=LGRAY, wrap=True)


# ── Slide 3 — Il Problema ─────────────────────────────────────────────────────

def s_problema(prs):
    s = blank(prs); bg(s)
    hdr(s, "Il Problema — UCI Seeds", "Unsupervised clustering: scoprire varieta' di grano senza usare le etichette")
    pgn(s, 3)
    # Left panel
    rct(s, Inches(0.2), Inches(1.55), Inches(5.9), Inches(5.65), fill=B_DARK, line=TEAL, lw=Pt(1))
    tb(s, Inches(0.35), Inches(1.65), Inches(5.6), Inches(0.5), "Obiettivo", sz=Pt(18), bold=True)
    tb(s, Inches(0.35), Inches(2.18), Inches(5.6), Inches(0.85),
       "Identificare automaticamente le 3 varieta' di grano (Kama, Rosa, Canadian) dalle misure geometriche, senza usare le etichette durante il training.",
       sz=Pt(12.5), c=LGRAY, wrap=True)
    rct(s, Inches(0.35), Inches(3.1), Inches(5.6), Inches(1.6), fill=B_BLUE)
    tb(s, Inches(0.45), Inches(3.15), Inches(5.4), Inches(0.42), "Dataset UCI Seeds (id=236)", sz=Pt(13), bold=True)
    for j, line in enumerate([
        "210 campioni totali (70 per varieta', bilanciato)",
        "7 feature numeriche continue, nessun valore mancante",
        "Target (Class) caricato ma NON usato nel training",
        "Valutazione: Silhouette + ARI/NMI/Purity post-fit",
    ]):
        tb(s, Inches(0.45), Inches(3.65)+j*Inches(0.27), Inches(5.4), Inches(0.27), line, sz=Pt(11.5), c=LGRAY)
    rct(s, Inches(0.35), Inches(4.85), Inches(5.6), Inches(1.2), fill=B_TEAL)
    tb(s, Inches(0.45), Inches(4.9), Inches(5.4), Inches(0.4), "7 Feature (tutte continue)", sz=Pt(13), bold=True)
    for j, line in enumerate(["area, perimeter, compactness", "kernel_length, kernel_width", "asymmetry_coef, groove_length"]):
        tb(s, Inches(0.45), Inches(5.38)+j*Inches(0.28), Inches(5.4), Inches(0.28), line, sz=Pt(12), c=WHITE)
    # Right panel — varieta'
    rct(s, Inches(6.35), Inches(1.55), Inches(6.75), Inches(5.65), fill=B_DARK, line=B_BLUE, lw=Pt(1))
    tb(s, Inches(6.5), Inches(1.65), Inches(6.5), Inches(0.48), "Le 3 varieta' di grano", sz=Pt(16), bold=True)
    varieties = [
        ("Kama",     "70 campioni", "Semi compatti e simmetrici. Forma arrotondata, compactness alta.", B_BLUE),
        ("Rosa",     "70 campioni", "Semi piu' grandi e allungati. Area e perimetro piu' elevati.", B_GRN),
        ("Canadian", "70 campioni", "Semi piu' piccoli e asimmetrici. Groove length caratteristica.", B_ORA),
    ]
    for j, (name, cnt, desc, col) in enumerate(varieties):
        vy = Inches(2.3) + j*Inches(1.55)
        rct(s, Inches(6.5), vy, Inches(6.35), Inches(1.38), fill=col)
        tb(s, Inches(6.62), vy+Inches(0.04), Inches(4.5), Inches(0.5), name, sz=Pt(22), bold=True)
        tb(s, Inches(6.62), vy+Inches(0.52), Inches(4.5), Inches(0.32), cnt, sz=Pt(13), bold=True, c=ORANGE)
        tb(s, Inches(6.62), vy+Inches(0.88), Inches(6.1), Inches(0.38), desc, sz=Pt(12), c=LGRAY, wrap=True)


# ── Slide 4 — Architettura ────────────────────────────────────────────────────

def s_arch(prs):
    s = blank(prs); bg(s)
    hdr(s, "Architettura del Progetto", "Docker  |  REST API  |  config.yaml  |  Libreria embedded")
    pgn(s, 4)
    # File tree
    rct(s, Inches(0.15), Inches(1.55), Inches(4.45), Inches(5.7), fill=RGBColor(0x12,0x12,0x26), line=ORANGE, lw=Pt(1))
    tb(s, Inches(0.27), Inches(1.65), Inches(4.25), Inches(5.4),
       "Seeds-ML/\n|- lib/\n|  |- kmeans.py\n|  |- plots.py\n|  |- loader.py\n|  |- eda.py\n|  |- cleaner.py\n|  |- encoder.py\n|  +- api/\n|     |- kmeans.py\n|     |- state.py\n|     |- loader.py\n|     |- eda.py\n|     |- cleaner.py\n|     +- encoder.py\n|- main.py\n|- app.py\n|- config.yaml\n+- Dockerfile",
       sz=Pt(11), c=ORANGE, wrap=False)
    # REST API panel
    rct(s, Inches(4.8), Inches(1.55), Inches(4.1), Inches(2.7), fill=B_GRN)
    tb(s, Inches(4.92), Inches(1.62), Inches(3.9), Inches(0.45), "REST API — Flask", sz=Pt(14), bold=True)
    for j, ep in enumerate([
        "POST /loader/load          → carica UCI/CSV",
        "POST /cleaner/fit_transform → imputa mancanti",
        "POST /encoder/fit_transform → scala feature",
        "POST /kmeans/search        → elbow + silhouette",
        "POST /kmeans/fit           → fit con k scelto",
        "GET  /kmeans/profiles      → profili cluster",
        "GET  /kmeans/compare       → ARI, NMI, purity",
    ]):
        tb(s, Inches(4.92), Inches(2.15)+j*Inches(0.27), Inches(3.9), Inches(0.27), ep, sz=Pt(10.5), c=WHITE)
    # Config YAML
    rct(s, Inches(4.8), Inches(4.38), Inches(4.1), Inches(2.87), fill=B_ORA)
    tb(s, Inches(4.92), Inches(4.44), Inches(3.9), Inches(0.42), "config.yaml — punto di controllo", sz=Pt(13), bold=True)
    tb(s, Inches(4.92), Inches(4.9), Inches(3.9), Inches(2.25),
       "loader:\n  dataset_id: 236  target_col: Class\ncleaner:\n  num_strategy: median\nencoder:\n  num_strategy: standard\nkmeans:\n  k_min: 2   k_max: 10\n  best_k: null   n_init: 10\n  random_state: 42\n  metric: euclidean",
       sz=Pt(11), c=WHITE, wrap=False)
    # Docker
    rct(s, Inches(9.1), Inches(1.55), Inches(4.0), Inches(2.7), fill=B_BLUE)
    tb(s, Inches(9.22), Inches(1.62), Inches(3.8), Inches(0.45), "Docker Container", sz=Pt(14), bold=True)
    for j, line in enumerate([
        "FROM python:3.11-slim",
        "WORKDIR /app",
        "COPY requirements.txt .",
        "RUN pip install -r requirements.txt",
        "COPY . .",
        "RUN mkdir -p output",
        'CMD ["python", "main.py"]',
    ]):
        tb(s, Inches(9.22), Inches(2.15)+j*Inches(0.27), Inches(3.8), Inches(0.27), line, sz=Pt(11), c=WHITE)
    # Separazione responsabilita'
    rct(s, Inches(9.1), Inches(4.38), Inches(4.0), Inches(2.87), fill=B_TEAL)
    tb(s, Inches(9.22), Inches(4.44), Inches(3.8), Inches(0.42), "Separazione responsabilita'", sz=Pt(13), bold=True)
    tb(s, Inches(9.22), Inches(4.92), Inches(3.8), Inches(2.2),
       "main.py — pipeline batch completa\n\napp.py — server Flask + blueprint REST\n\nlib/ — logica riutilizzabile, framework-independent\n\nconfig.yaml — unico punto di configurazione",
       sz=Pt(12), c=WHITE, wrap=True)


# ── Slide 5 — Libreria lib/ ───────────────────────────────────────────────────

def s_lib(prs):
    s = blank(prs); bg(s)
    hdr(s, "Libreria Generalizzata — lib/", "Componenti riutilizzabili su qualsiasi dataset tabellare, non solo Seeds")
    pgn(s, 5)
    rct(s, Inches(0.2), Inches(1.55), Inches(12.9), Inches(0.78), fill=NAVY_MID, line=ORANGE, lw=Pt(1))
    tb(s, Inches(0.35), Inches(1.65), Inches(12.6), Inches(0.62),
       "lib/ non e' specifica per Seeds: e' una libreria ML generica. Ogni componente prende un DataFrame in input, lo trasforma e restituisce un DataFrame indipendentemente dal dominio. Per usarla su un nuovo dataset basta cambiare config.yaml.",
       sz=Pt(13), c=WHITE, wrap=True)
    comps = [
        ("GenericLoader",  B_BLUE,  "Carica da UCI (per ID) o CSV locale. Separa X e y. Missing report e statistiche di base."),
        ("GenericEda",     B_TEAL,  "Summary statistics, correlazioni Pearson. Identifica coppie altamente correlate (|r|>0.85)."),
        ("GenericCleaner", B_GRN,   "Imputa mancanti: mediana/media/moda per numerici, 'unknown' per categorici. Fit su train."),
        ("GenericEncoder", B_ORA,   "Scala feature: StandardScaler, MinMaxScaler o none. One-Hot Encoding per categoriche."),
        ("KMeansModel",    B_PUR,   "Clustering generico: search k, fit, metriche. Backend auto-selezionato da metric in config."),
        ("KMeansPlotter",  B_RED,   "Elbow+Silhouette, PCA 2D scatter, heatmap profili cluster, pairplot. Output PNG su disco."),
    ]
    bw, bh, gx, gy = Inches(4.1), Inches(1.4), Inches(0.25), Inches(0.18)
    sx, sy = Inches(0.25), Inches(2.52)
    for i, (name, col, desc) in enumerate(comps):
        r, c = divmod(i, 3)
        x = sx + c*(bw+gx)
        y = sy + r*(bh+gy)
        rct(s, x, y, bw, bh, fill=col)
        tb(s, x+Inches(0.1), y+Inches(0.05), bw-Inches(0.2), Inches(0.45), name, sz=Pt(15), bold=True)
        tb(s, x+Inches(0.1), y+Inches(0.52), bw-Inches(0.2), Inches(0.78), desc, sz=Pt(11), c=LGRAY, wrap=True)


# ── Slide 6 — Data Pipeline ───────────────────────────────────────────────────

def s_pipeline(prs):
    s = blank(prs); bg(s)
    hdr(s, "Data Pipeline", "Dal dataset grezzo ai vettori pronti per il clustering")
    pgn(s, 6)
    stages = [
        ("LOADER",  B_BLUE, "Legge UCI\nid=236\nSepara X, y\n(y NON usata\nnel training)"),
        ("EDA",     B_TEAL, "Summary\nstats\nCorrelazioni\nMissing\nreport"),
        ("CLEANER", B_GRN,  "Mediana\nnumerici\n'unknown'\ncategorici\nFit su train"),
        ("ENCODER", B_ORA,  "Standard\nScaler\nnumerici\nOHE\ncategorici"),
        ("KMEANS",  B_PUR,  "search k\nelbow +\nsilhouette\nfit best_k"),
        ("METRICS", B_RED,  "ARI NMI\nPurity\n(post-fit,\ncon y_true)"),
    ]
    bw, bh = Inches(1.88), Inches(3.6)
    gap = Inches(0.2)
    sx, sy = Inches(0.28), Inches(1.65)
    for i, (name, col, desc) in enumerate(stages):
        x = sx + i*(bw+gap)
        rct(s, x, sy, bw, Inches(0.52), fill=col)
        tb(s, x, sy, bw, Inches(0.52), name, sz=Pt(13), bold=True, align=PP_ALIGN.CENTER)
        rct(s, x, sy+Inches(0.52), bw, bh-Inches(0.52), fill=NAVY_MID, line=col, lw=Pt(1.5))
        tb(s, x+Inches(0.08), sy+Inches(0.62), bw-Inches(0.16), bh-Inches(0.72), desc, sz=Pt(11.5), c=LGRAY, wrap=True)
        if i < len(stages)-1:
            ax = x+bw+Inches(0.02)
            rct(s, ax, sy+bh/2-Inches(0.04), gap-Inches(0.04), Inches(0.08), fill=ORANGE)
    rct(s, Inches(0.2), Inches(5.42), Inches(12.9), Inches(1.85), fill=CREAM, line=ORANGE, lw=Pt(1))
    tb(s, Inches(0.35), Inches(5.52), Inches(12.6), Inches(1.65),
       "Principio fondamentale — Unsupervised learning: il target (Class) viene caricato ma NON usato durante cleaning, scaling e clustering. Serve solo per la valutazione finale con ARI/NMI/Purity, che misura quanto i cluster scoperti corrispondono alle varieta' reali.\n\nContrasto con Titanic: li' y era necessaria per il training supervisionato; qui l'algoritmo trova la struttura dei dati da solo.",
       sz=Pt(12), c=NAVY, wrap=True)


# ── Slide 7 — Supervised vs Unsupervised ──────────────────────────────────────

def s_paradigmi(prs):
    s = blank(prs); bg(s)
    hdr(s, "Supervised vs Unsupervised Learning", "Due paradigmi fondamentalmente diversi di Machine Learning")
    pgn(s, 7)
    # Left
    rct(s, Inches(0.2), Inches(1.55), Inches(6.2), Inches(5.65), fill=B_DARK, line=B_BLUE, lw=Pt(2))
    tb(s, Inches(0.32), Inches(1.65), Inches(5.9), Inches(0.5), "Supervised (Titanic)", sz=Pt(18), bold=True, c=RGBColor(0x6a,0xa8,0xff))
    rows_s = [
        ("Input",       "X + y  (feature + etichette note)"),
        ("Obiettivo",   "Imparare f(X) → y"),
        ("Valutazione", "Accuracy, F1, AUC"),
        ("Esempio",     "Predire sopravvivenza passeggeri"),
        ("Algoritmi",   "LogReg, RF, XGBoost, SVM"),
    ]
    for j, (lbl, val) in enumerate(rows_s):
        y = Inches(2.32)+j*Inches(0.82)
        rct(s, Inches(0.38), y, Inches(5.85), Inches(0.65), fill=B_BLUE)
        tb(s, Inches(0.48), y+Inches(0.03), Inches(1.5), Inches(0.58), lbl+":", sz=Pt(13), bold=True, c=ORANGE)
        tb(s, Inches(1.9),  y+Inches(0.03), Inches(4.2), Inches(0.58), val, sz=Pt(13), c=WHITE)
    # Right
    rct(s, Inches(6.6), Inches(1.55), Inches(6.5), Inches(5.65), fill=B_DARK, line=B_TEAL, lw=Pt(2))
    tb(s, Inches(6.72), Inches(1.65), Inches(6.3), Inches(0.5), "Unsupervised (Seeds)", sz=Pt(18), bold=True, c=TEAL)
    rows_u = [
        ("Input",       "Solo X  (nessuna etichetta)"),
        ("Obiettivo",   "Trovare struttura nascosta nei dati"),
        ("Valutazione", "Silhouette, ARI, NMI, Purity"),
        ("Esempio",     "Scoprire varieta' di grano"),
        ("Algoritmi",   "KMeans, KMedoids, KModes, DBSCAN"),
    ]
    for j, (lbl, val) in enumerate(rows_u):
        y = Inches(2.32)+j*Inches(0.82)
        rct(s, Inches(6.78), y, Inches(6.15), Inches(0.65), fill=B_TEAL)
        tb(s, Inches(6.88), y+Inches(0.03), Inches(1.5), Inches(0.58), lbl+":", sz=Pt(13), bold=True, c=ORANGE)
        tb(s, Inches(8.3),  y+Inches(0.03), Inches(4.5), Inches(0.58), val, sz=Pt(13), c=WHITE)


# ── Slide 8 — KMeans: Algoritmo di Lloyd ─────────────────────────────────────

def s_lloyd(prs):
    s = blank(prs); bg(s)
    hdr(s, "KMeans — Algoritmo di Lloyd", "Come funziona internamente il clustering partizionale")
    pgn(s, 8)
    steps = [
        ("1", "Inizializzazione\nk-means++", ORANGE,
         "Scegli k centroidi iniziali in modo intelligente: il 1o casuale, i successivi scelti con probabilita' proporzionale alla distanza dal centroide piu' vicino. Riduce il rischio di minimi locali rispetto alla scelta casuale pura."),
        ("2", "Assegnazione\n(E-step)", B_BLUE,
         "Per ogni punto, calcola la distanza euclidea da tutti i k centroidi. Assegna il punto al centroide piu' vicino. Tutti i 210 punti vengono partizionati in k cluster."),
        ("3", "Aggiornamento\n(M-step)", B_GRN,
         "Ricalcola ogni centroide come la media di tutti i punti assegnati. Il centroide si 'sposta' verso il baricentro del suo gruppo. Con distanza euclidea, la media minimizza l'inertia."),
        ("4", "Convergenza", B_TEAL,
         "Ripeti E-step e M-step finche' i centroidi non si spostano piu' (variazione < tolleranza). Garantita la convergenza, ma non l'ottimo globale. Ecco perche' n_init=10."),
    ]
    bw, bh = Inches(2.88), Inches(4.85)
    gap = Inches(0.22)
    sx, sy = Inches(0.28), Inches(1.6)
    for i, (num, title, col, desc) in enumerate(steps):
        x = sx+i*(bw+gap)
        rct(s, x, sy, bw, Inches(0.68), fill=col)
        tb(s, x, sy, Inches(0.62), Inches(0.68), num, sz=Pt(28), bold=True, align=PP_ALIGN.CENTER)
        tb(s, x+Inches(0.65), sy+Inches(0.08), bw-Inches(0.72), Inches(0.52), title, sz=Pt(13), bold=True)
        rct(s, x, sy+Inches(0.68), bw, bh-Inches(0.68), fill=NAVY_MID, line=col, lw=Pt(1.5))
        tb(s, x+Inches(0.1), sy+Inches(0.82), bw-Inches(0.2), bh-Inches(1.0), desc, sz=Pt(12.5), c=LGRAY, wrap=True)
    rct(s, Inches(0.2), Inches(6.6), Inches(12.9), Inches(0.72), fill=NAVY_MID, line=ORANGE, lw=Pt(1))
    tb(s, Inches(0.35), Inches(6.68), Inches(12.6), Inches(0.58),
       "n_init=10 in config.yaml: l'intero processo (init → E → M → convergenza) viene ripetuto 10 volte con inizializzazioni diverse. Viene tenuto il risultato con inertia minima. Mitiga il problema dell'ottimo locale.",
       sz=Pt(12), c=LGRAY, wrap=True)


# ── Slide 9 — Scelta di K ─────────────────────────────────────────────────────

def s_k(prs):
    s = blank(prs); bg(s)
    hdr(s, "Scelta di K — Elbow + Silhouette", "Due criteri complementari per trovare il numero ottimale di cluster")
    pgn(s, 9)
    # Left — Elbow
    rct(s, Inches(0.2), Inches(1.55), Inches(6.1), Inches(5.65), fill=B_DARK, line=ORANGE, lw=Pt(2))
    tb(s, Inches(0.35), Inches(1.65), Inches(5.8), Inches(0.5), "Elbow Method — Inertia", sz=Pt(18), bold=True, c=ORANGE)
    tb(s, Inches(0.35), Inches(2.2), Inches(5.8), Inches(1.1),
       "Inertia = somma delle distanze euclidee quadrate di ogni punto dal proprio centroide. Diminuisce sempre all'aumentare di k. Il 'gomito' e' il punto dove la diminuzione rallenta: aggiungere altri cluster porta poco beneficio.",
       sz=Pt(12.5), c=LGRAY, wrap=True)
    rct(s, Inches(0.35), Inches(3.45), Inches(5.75), Inches(0.52), fill=B_ORA)
    tb(s, Inches(0.45), Inches(3.5), Inches(5.55), Inches(0.4), "Limite: soggettivo, difficile da automatizzare", sz=Pt(13), c=WHITE)
    tb(s, Inches(0.35), Inches(4.1), Inches(5.75), Inches(0.4), "Inertia per Seeds (valori indicativi):", sz=Pt(13), bold=True)
    k_notes = [("2","alta"), ("3","gomito"), ("4","↓"), ("5","↓"), ("6","plateau"), ("7","—"), ("8","—"), ("9","—"), ("10","—")]
    for j, (k, note) in enumerate(k_notes):
        col_j, row_j = j%3, j//3
        kx = Inches(0.45)+col_j*Inches(1.9)
        ky = Inches(4.65)+row_j*Inches(0.38)
        rct(s, kx, ky, Inches(1.75), Inches(0.32), fill=NAVY_MID, line=B_BLUE, lw=Pt(0.5))
        tb(s, kx+Inches(0.05), ky+Inches(0.03), Inches(0.5), Inches(0.26), f"k={k}", sz=Pt(11), bold=True, c=ORANGE)
        tb(s, kx+Inches(0.55), ky+Inches(0.03), Inches(1.1), Inches(0.26), note, sz=Pt(11), c=LGRAY)
    # Right — Silhouette
    rct(s, Inches(6.5), Inches(1.55), Inches(6.6), Inches(5.65), fill=B_DARK, line=TEAL, lw=Pt(2))
    tb(s, Inches(6.65), Inches(1.65), Inches(6.38), Inches(0.5), "Silhouette Score", sz=Pt(18), bold=True, c=TEAL)
    tb(s, Inches(6.65), Inches(2.2), Inches(6.38), Inches(0.72),
       "Per ogni punto i: misura quanto e' vicino ai punti del suo cluster (a) rispetto al cluster piu' vicino (b).",
       sz=Pt(12.5), c=LGRAY, wrap=True)
    rct(s, Inches(6.65), Inches(3.0), Inches(6.2), Inches(0.78), fill=NAVY_MID, line=TEAL, lw=Pt(1))
    tb(s, Inches(6.75), Inches(3.08), Inches(6.0), Inches(0.62),
       "s(i) = (b(i) - a(i)) / max(a(i), b(i))     ∈ [-1, +1]",
       sz=Pt(14), bold=True, align=PP_ALIGN.CENTER)
    tb(s, Inches(6.65), Inches(3.9), Inches(6.38), Inches(0.85),
       "a(i) = distanza media intra-cluster\nb(i) = distanza media verso il cluster piu' vicino\n→ +1: punto ben assegnato  |  ~0: sul confine  |  <0: cluster sbagliato",
       sz=Pt(11.5), c=LGRAY, wrap=True)
    rct(s, Inches(6.65), Inches(4.88), Inches(6.2), Inches(0.52), fill=B_GRN)
    tb(s, Inches(6.75), Inches(4.93), Inches(6.0), Inches(0.42), "Vantaggio: oggettivo, automatizzabile → best_k auto in config", sz=Pt(13), c=WHITE)
    rct(s, Inches(6.65), Inches(5.5), Inches(6.2), Inches(1.55), fill=NAVY_MID, line=ORANGE, lw=Pt(1))
    tb(s, Inches(6.75), Inches(5.58), Inches(6.0), Inches(1.38),
       "best_k: null in config.yaml → auto-seleziona il k con silhouette massima nell'intervallo [k_min, k_max].\n\nPer Seeds con k_min=2, k_max=10 l'algoritmo seleziona automaticamente k=3, che coincide con le 3 varieta' biologiche.",
       sz=Pt(12), c=LGRAY, wrap=True)


# ── Slide 10 — Metriche ───────────────────────────────────────────────────────

def s_metriche(prs):
    s = blank(prs); bg(s)
    hdr(s, "Metriche di Valutazione Clustering", "Come misurare la qualita' senza e con le etichette vere")
    pgn(s, 10)
    metrics = [
        ("Silhouette Score", B_TEAL, NAVY_MID,
         "Metrica interna (non richiede y_true)",
         "Coesione intra-cluster vs separazione inter-cluster.\nRange [-1,+1]. Valori >0.5 indicano struttura forte.\nUsata per la scelta automatica di k.", "~0.52"),
        ("Adjusted Rand Index (ARI)", B_BLUE, B_DARK,
         "Metrica esterna (richiede y_true per confronto)",
         "Similarita' tra la partizione trovata e le etichette reali, corretta per il caso. 1=perfetta, 0=casuale.\nRange [-1, +1].", "~0.78"),
        ("Normalized Mutual Info (NMI)", B_GRN, RGBColor(0x12,0x52,0x30),
         "Metrica esterna (richiede y_true per confronto)",
         "Informazione mutua condivisa tra cluster e etichette, normalizzata in [0,1]. Robusta a cluster di dimensioni diverse.", "~0.73"),
        ("Purity", B_ORA, RGBColor(0x70,0x35,0x08),
         "Metrica esterna (richiede y_true per confronto)",
         "Per ogni cluster, prende la classe maggioritaria e somma le assegnazioni corrette. Semplice e intuitiva.\nRange [0, 1].", "~0.90"),
    ]
    bw, bh = Inches(5.9), Inches(1.6)
    gap_x, gap_y = Inches(0.4), Inches(0.2)
    for i, (name, hc, bc, sub, desc, res) in enumerate(metrics):
        r, c = divmod(i, 2)
        x = Inches(0.25)+c*(bw+gap_x)
        y = Inches(1.6)+r*(bh+gap_y)
        rct(s, x, y, bw, bh, fill=bc, line=hc, lw=Pt(1.5))
        rct(s, x, y, bw, Inches(0.42), fill=hc)
        tb(s, x+Inches(0.1), y+Inches(0.03), bw-Inches(0.2), Inches(0.36), name, sz=Pt(14), bold=True)
        tb(s, x+Inches(0.1), y+Inches(0.46), bw-Inches(0.2), Inches(0.28), sub, sz=Pt(11), italic=True, c=LGRAY)
        tb(s, x+Inches(0.1), y+Inches(0.74), bw-Inches(0.2), Inches(0.62), desc, sz=Pt(11.5), c=LGRAY, wrap=True)
        rct(s, x+bw-Inches(1.65), y+bh-Inches(0.38), Inches(1.55), Inches(0.33), fill=ORANGE)
        tb(s, x+bw-Inches(1.65), y+bh-Inches(0.37), Inches(1.55), Inches(0.32),
           f"Seeds: {res}", sz=Pt(11), bold=True, c=NAVY, align=PP_ALIGN.CENTER)
    rct(s, Inches(0.2), Inches(6.92), Inches(12.9), Inches(0.42), fill=NAVY_MID)
    tb(s, Inches(0.35), Inches(6.96), Inches(12.6), Inches(0.35),
       "Silhouette disponibile sempre; ARI/NMI/Purity richiedono y_true e vengono calcolate solo nella fase di analisi post-fit, non durante il training.",
       sz=Pt(11.5), c=LGRAY)


# ── Slide 11 — Metrica Generica ───────────────────────────────────────────────

def s_metrica(prs):
    s = blank(prs); bg(s)
    hdr(s, "Metrica Generica — Factory Pattern", "Un parametro config.yaml, tre backend diversi: KMeans / KMedoids / KModes")
    pgn(s, 11)
    # Code
    rct(s, Inches(0.2), Inches(1.55), Inches(5.75), Inches(5.65), fill=RGBColor(0x12,0x12,0x26), line=ORANGE, lw=Pt(1))
    tb(s, Inches(0.3), Inches(1.65), Inches(5.55), Inches(5.4),
       "# lib/kmeans.py\n\ndef _build_model(k, metric,\n                random_state, n_init):\n\n  if metric == 'euclidean':\n    return KMeans(\n      n_clusters=k, n_init=n_init)\n\n  elif metric in {'manhattan',\n                  'cosine', ...}:\n    from sklearn_extra.cluster \\\n         import KMedoids\n    return KMedoids(\n      n_clusters=k, metric=metric)\n\n  elif metric == 'gower':\n    import gower\n    dist = gower.gower_matrix(X)\n    return KMedoids(\n      metric='precomputed')\n\n  elif metric == 'hamming':\n    from kmodes.kmodes \\\n         import KModes\n    return KModes(n_clusters=k)",
       sz=Pt(10.5), c=ORANGE, wrap=False)
    # Backend boxes
    backends = [
        ("euclidean",         "KMeans (sklearn)",            "Distanza euclidea + media. Il piu' veloce. Ottimale per feature continue normalizzate. Backend default.", B_BLUE),
        ("manhattan / cosine","KMedoids (sklearn_extra)",    "Usa la distanza scelta. Centroide = punto reale del dataset. Piu' robusto agli outlier rispetto a KMeans.", B_TEAL),
        ("gower",             "KMedoids precomputed",        "Calcola la matrice di Gower (mista continuo+discreto) e la passa come metrica precomputata a KMedoids.", B_GRN),
        ("hamming",           "KModes (kmodes)",             "Per dati categorici puri. Distanza = numero di feature diverse. Centro = moda. Nessuno scaling necessario.", B_ORA),
    ]
    bw, bh, gap = Inches(6.9), Inches(1.22), Inches(0.18)
    bx, by0 = Inches(6.25), Inches(1.6)
    for i, (metric_s, algo, desc, col) in enumerate(backends):
        by = by0 + i*(bh+gap)
        rct(s, bx, by, bw, bh, fill=NAVY_MID, line=col, lw=Pt(1.5))
        rct(s, bx, by, Inches(1.4), bh, fill=col)
        tb(s, bx+Inches(0.07), by+Inches(0.28), Inches(1.28), Inches(0.68),
           metric_s, sz=Pt(11.5), bold=True, align=PP_ALIGN.CENTER)
        tb(s, bx+Inches(1.5), by+Inches(0.05), bw-Inches(1.6), Inches(0.42), algo, sz=Pt(14), bold=True, c=col)
        tb(s, bx+Inches(1.5), by+Inches(0.5), bw-Inches(1.6), Inches(0.62), desc, sz=Pt(12), c=LGRAY, wrap=True)
    rct(s, bx, Inches(6.55), bw, Inches(0.72), fill=NAVY_MID, line=ORANGE, lw=Pt(1))
    tb(s, bx+Inches(0.1), Inches(6.62), bw-Inches(0.2), Inches(0.58),
       "config.yaml  →  kmeans: metric: euclidean     Cambia una riga → l'algoritmo cambia backend automaticamente.",
       sz=Pt(13), c=LGRAY, wrap=True)


# ── Slide 12 — Risultati ──────────────────────────────────────────────────────

def s_risultati(prs):
    s = blank(prs); bg(s)
    hdr(s, "Risultati — Performance su Seeds", "KMeans k=3, StandardScaler, metric=euclidean (valori indicativi)")
    pgn(s, 12)
    # Left table
    rct(s, Inches(0.2), Inches(1.55), Inches(7.0), Inches(5.65), fill=B_DARK, line=B_BLUE, lw=Pt(1))
    rct(s, Inches(0.3), Inches(1.65), Inches(6.8), Inches(0.42), fill=B_BLUE)
    for lbl, x in [("Metrica", Inches(0.38)), ("Valore", Inches(2.5)), ("Interpretazione", Inches(3.55))]:
        tb(s, x, Inches(1.67), Inches(3.0), Inches(0.38), lbl, sz=Pt(12), bold=True)
    rows = [
        ("Silhouette (k=3)",  "0.521", "Struttura cluster ben definita"),
        ("ARI",               "0.782", "Alta corrispondenza con varieta' reali"),
        ("NMI",               "0.733", "Buona mutua informazione"),
        ("Purity",            "0.905", "90.5% punti correttamente assegnati"),
        ("Inertia (k=3)",     "386.2", "Calo netto rispetto a k=2 (622.1)"),
        ("Cluster 0",         "70 pt", "Recupera quasi perfettamente Kama"),
        ("Cluster 1",         "70 pt", "Rosa ben separata dalle altre"),
        ("Cluster 2",         "70 pt", "Canadian distinta per compattezza"),
    ]
    for i, (m, v, interp) in enumerate(rows):
        ry = Inches(2.15)+i*Inches(0.4)
        rct(s, Inches(0.3), ry, Inches(6.8), Inches(0.38), fill=NAVY_MID if i%2==0 else B_DARK)
        tb(s, Inches(0.38), ry+Inches(0.04), Inches(2.0), Inches(0.3), m, sz=Pt(12), c=LGRAY)
        tb(s, Inches(2.5),  ry+Inches(0.04), Inches(0.92), Inches(0.3), v, sz=Pt(13), bold=True, c=ORANGE, align=PP_ALIGN.CENTER)
        tb(s, Inches(3.55), ry+Inches(0.04), Inches(3.45), Inches(0.3), interp, sz=Pt(12), c=WHITE)
    # Right analysis
    rct(s, Inches(7.4), Inches(1.55), Inches(5.7), Inches(5.65), fill=B_DARK, line=B_TEAL, lw=Pt(1))
    tb(s, Inches(7.55), Inches(1.65), Inches(5.5), Inches(0.45), "Analisi dei risultati", sz=Pt(16), bold=True)
    analyses = [
        ("Silhouette 0.52",  TEAL, "Struttura cluster ben definita. Seeds e' un dataset naturalmente separato: le 3 varieta' hanno misure geometriche distinte."),
        ("ARI 0.78",         B_BLUE, "L'algoritmo recupera quasi perfettamente la suddivisione botanica, senza mai aver visto le etichette durante il training."),
        ("Purity 90.5%",     B_GRN, "Solo ~20 punti su 210 vengono assegnati al cluster sbagliato, tipicamente i semi di confine tra Kama e Canadian."),
        ("k=3 confermato",   ORANGE, "Silhouette massima a k=3 corrisponde esattamente alle 3 varieta' biologiche: il clustering ha scoperto struttura reale."),
    ]
    for j, (title, col, desc) in enumerate(analyses):
        ay = Inches(2.22)+j*Inches(1.18)
        rct(s, Inches(7.55), ay, Inches(5.4), Inches(0.38), fill=col)
        tb(s, Inches(7.65), ay+Inches(0.04), Inches(5.2), Inches(0.3), title, sz=Pt(13), bold=True, c=WHITE)
        tb(s, Inches(7.55), ay+Inches(0.42), Inches(5.4), Inches(0.65), desc, sz=Pt(11.5), c=LGRAY, wrap=True)


# ── Slide 13 — Visualizzazioni ────────────────────────────────────────────────

def s_viz(prs):
    s = blank(prs); bg(s)
    hdr(s, "Visualizzazioni", "Quattro grafici per interpretare i cluster — output/ PNG su disco")
    pgn(s, 13)
    plots = [
        ("Elbow + Silhouette",  B_BLUE,  "plots.py → elbow_silhouette()",
         "Due grafici affiancati: inertia vs k (cerca il gomito) e silhouette vs k (cerca il massimo). Generato dopo POST /kmeans/search. Permette di scegliere visivamente il k migliore."),
        ("PCA 2D Scatter",      B_GRN,   "plots.py → pca2d()",
         "Riduce le 7 feature a 2 componenti principali (varianza spiegata ~85%). Mostra cluster colorati a sinistra e classi reali a destra: permette di vedere visivamente quanto i cluster corrispondono alle varieta'."),
        ("Heatmap Profili",     B_ORA,   "plots.py → profiles()",
         "Heatmap: cluster (colonne) x feature (righe). Valore = media della feature nel cluster a scala originale. Rivela quali misure geometriche caratterizzano ogni varieta' di grano."),
        ("Pairplot Feature",    B_PUR,   "plots.py → pairplot()",
         "Matrice di scatter plot per ogni coppia di feature, colorata per cluster. Identifica quali coppie separano meglio i cluster. Usa kernel density estimation sulla diagonale."),
    ]
    bw, bh = Inches(5.9), Inches(2.42)
    gap_x, gap_y = Inches(0.45), Inches(0.2)
    for i, (title, col, func, desc) in enumerate(plots):
        r, c = divmod(i, 2)
        x = Inches(0.25)+c*(bw+gap_x)
        y = Inches(1.6)+r*(bh+gap_y)
        rct(s, x, y, bw, bh, fill=NAVY_MID, line=col, lw=Pt(1))
        rct(s, x, y, bw, Inches(0.5), fill=col)
        tb(s, x+Inches(0.1), y+Inches(0.05), bw-Inches(0.2), Inches(0.42), title, sz=Pt(16), bold=True)
        tb(s, x+Inches(0.1), y+Inches(0.56), bw-Inches(0.2), Inches(0.3), func, sz=Pt(12), italic=True, c=ORANGE)
        tb(s, x+Inches(0.1), y+Inches(0.9), bw-Inches(0.2), Inches(1.35), desc, sz=Pt(12), c=LGRAY, wrap=True)


# ── Slide 14 — Prossimi Passi ─────────────────────────────────────────────────

def s_next(prs):
    s = blank(prs); bg(s)
    hdr(s, "Prossimi Passi", "Come estendere il progetto con nuovi algoritmi e tecniche")
    pgn(s, 14)
    items = [
        ("Clustering Gerarchico", B_BLUE,
         "AgglomerativeClustering con linkage ward/complete/average/single. Non richiede k a priori — sceglie il numero di cluster tagliando il dendrogramma. Gia' in sklearn, basta aggiungere il backend nella factory.",
         "Implementazione: 10 righe in lib/kmeans.py"),
        ("DBSCAN", B_GRN,
         "Density-Based Spatial Clustering. Non richiede k. Trova cluster di forma arbitraria e identifica outlier come 'rumore'. Parametri: eps (raggio di ricerca), min_samples (densita' minima).",
         "Vantaggio: gestione outlier, cluster non sferici"),
        ("t-SNE / UMAP", B_ORA,
         "Tecniche di riduzione dimensionale non lineari per visualizzazione. Superiori a PCA per strutture complesse. t-SNE preserva struttura locale. UMAP e' piu' veloce e scalabile.",
         "Miglioramento: visualizzazioni piu' espressive"),
        ("Linkage come HP", B_PUR,
         "Aggiungere linkage come iperparametro in config.yaml per AgglomerativeClustering. Combinato con metric: ward/manhattan/cosine, crea uno spazio di iperparametri configurabile come in R.",
         "Obiettivo: flessibilita' pari a R flexclust"),
    ]
    bw, bh = Inches(5.9), Inches(2.28)
    gap_x, gap_y = Inches(0.45), Inches(0.2)
    for i, (title, col, desc, footer) in enumerate(items):
        r, c = divmod(i, 2)
        x = Inches(0.25)+c*(bw+gap_x)
        y = Inches(1.6)+r*(bh+gap_y)
        rct(s, x, y, bw, bh, fill=NAVY_MID, line=col, lw=Pt(1.5))
        rct(s, x, y, bw, Inches(0.45), fill=col)
        tb(s, x+Inches(0.1), y+Inches(0.04), bw-Inches(0.2), Inches(0.38), title, sz=Pt(15), bold=True)
        tb(s, x+Inches(0.1), y+Inches(0.52), bw-Inches(0.2), Inches(1.2), desc, sz=Pt(12), c=LGRAY, wrap=True)
        rct(s, x+Inches(0.1), y+bh-Inches(0.43), bw-Inches(0.2), Inches(0.35), fill=B_DARK, line=col, lw=Pt(0.5))
        tb(s, x+Inches(0.2), y+bh-Inches(0.41), bw-Inches(0.4), Inches(0.32), footer, sz=Pt(11.5), bold=True, c=col)


# ── Slide 15 — Grazie ─────────────────────────────────────────────────────────

def s_grazie(prs):
    s = blank(prs); bg(s)
    tb(s, Inches(0.5), Inches(1.1), Inches(12.3), Inches(1.5),
       "Grazie", sz=Pt(64), bold=True, align=PP_ALIGN.CENTER)
    tb(s, Inches(0.5), Inches(2.65), Inches(12.3), Inches(0.72),
       "Seeds Clustering — ML Pipeline con Libreria Generalizzata e Metrica Configurabile",
       sz=Pt(18), italic=True, c=LGRAY, align=PP_ALIGN.CENTER)
    rct(s, Inches(0), Inches(3.48), SW, Inches(0.07), fill=ORANGE, lw=Pt(0))
    rct(s, Inches(0), Inches(3.55), SW, Inches(0.04), fill=TEAL,   lw=Pt(0))
    concepts = [
        ("KMeans\nLloyd",       "Algoritmo partizionale"),
        ("Elbow +\nSilhouette", "Scelta di k"),
        ("ARI NMI\nPurity",     "Valutazione cluster"),
        ("Factory\nPattern",    "Metrica generica"),
        ("KMedoids\nKModes",    "Backend alternativi"),
        ("REST API\nFlask",     "Architettura"),
        ("Gower\nDist.",        "Dati misti"),
        ("PCA 2D\nPairplot",    "Visualizzazioni"),
    ]
    bw, bh = Inches(1.44), Inches(1.42)
    gap = Inches(0.17)
    sx = (SW - (8*bw + 7*gap)) / 2
    for i, (title, sub) in enumerate(concepts):
        x = sx + i*(bw+gap)
        rct(s, x, Inches(4.3), bw, bh, line=NAVY_MID, lw=Pt(1.5))
        tb(s, x, Inches(4.38), bw, Inches(0.75), title, sz=Pt(14), bold=True, c=ORANGE, align=PP_ALIGN.CENTER)
        tb(s, x, Inches(5.12), bw, Inches(0.48), sub, sz=Pt(10), c=LGRAY, align=PP_ALIGN.CENTER, wrap=True)
    tb(s, Inches(0), Inches(7.08), SW, Inches(0.3),
       "2025/26  |  Andrea Morlotti  Riccardo Scampini", sz=Pt(11), c=LGRAY, align=PP_ALIGN.CENTER)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    prs = new_prs()
    s_title(prs)
    s_index(prs)
    s_problema(prs)
    s_arch(prs)
    s_lib(prs)
    s_pipeline(prs)
    s_paradigmi(prs)
    s_lloyd(prs)
    s_k(prs)
    s_metriche(prs)
    s_metrica(prs)
    s_risultati(prs)
    s_viz(prs)
    s_next(prs)
    s_grazie(prs)
    out = "seeds_presentation.pptx"
    prs.save(out)
    print(f"Salvato: {out}  ({len(prs.slides)} slide)")
