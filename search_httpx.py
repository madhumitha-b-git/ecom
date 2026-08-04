import os
import re

search_dir = "microservices"
keywords = [r"httpx\.get\(", r"httpx\.post\("]
exclude_dirs = ["package", "package_fresh", "venv", "layer", "pkg_linux", "lambda_build"]

matches = []

for root, dirs, files in os.walk(search_dir):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            for idx, line in enumerate(lines):
                for kw in keywords:
                    if re.search(kw, line):
                        matches.append((filepath, idx + 1, line.strip()))

for filepath, line_num, content in matches:
    print(f"{filepath}:{line_num} -> {content}")
