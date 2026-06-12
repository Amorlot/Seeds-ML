from flask import Blueprint

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    return """<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Seeds ML Dashboard</title>
  <style>
    body { font-family: sans-serif; background: #0d1b4b; color: white; margin: 0; padding: 20px; }
    h1 { color: #f5921e; }
    button { background: #f5921e; color: white; border: none; padding: 12px 30px;
             font-size: 16px; cursor: pointer; border-radius: 4px; margin-bottom: 30px; }
    button:hover { background: #d4780e; }
    #status { margin-bottom: 20px; color: #d0d8f0; font-size: 14px; }
    .plots { display: flex; flex-wrap: wrap; gap: 20px; }
    .plots img { max-width: 48%; border: 2px solid #1a7a7a; border-radius: 4px; }
    .step { padding: 4px 0; }
    .ok   { color: #4caf50; }
    .err  { color: #f44336; }
  </style>
</head>
<body>
  <h1>Seeds ML — Dashboard</h1>
  <button onclick="runPipeline()">Esegui Pipeline</button>
  <div id="status"></div>
  <div class="plots" id="plots"></div>

  <script>
    async function post(path, body) {
      const r = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body || {})
      });
      return r;
    }

    async function runPipeline() {
      const status = document.getElementById("status");
      const plotsDiv = document.getElementById("plots");
      status.innerHTML = "";
      plotsDiv.innerHTML = "";

      const steps = [
        ["/loader/load",            { dataset_id: 236, target_col: "Class" }],
        ["/cleaner/configure",      {}],
        ["/cleaner/fit_transform",  {}],
        ["/encoder/configure",      {}],
        ["/encoder/fit_transform",  {}],
        ["/kmeans/search",          {}],
        ["/kmeans/plot/elbow",      {}],
        ["/kmeans/fit",             {}],
        ["/kmeans/plot/pca2d",      {}],
        ["/kmeans/plot/profiles",   {}],
        ["/kmeans/plot/pairplot",   {}],
      ];

      for (const [path, body] of steps) {
        const r = await post(path, body);
        const ok = r.ok;
        const div = document.createElement("div");
        div.className = "step " + (ok ? "ok" : "err");
        div.textContent = (ok ? "✓ " : "✗ ") + path;
        status.appendChild(div);
        if (!ok) return;
      }

      const plots = await (await fetch("/plots/")).json();
      for (const p of plots) {
        const img = document.createElement("img");
        img.src = "/plots/" + p + "?t=" + Date.now();
        plotsDiv.appendChild(img);
      }
    }
  </script>
</body>
</html>"""
