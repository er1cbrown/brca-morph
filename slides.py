"""Build the 5-slide deck. Do not use the old python-pptx generator."""
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
script = root / "presentation.js"
raise SystemExit(subprocess.call(["node", str(script)], cwd=root))
