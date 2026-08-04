import os
import glob

files = glob.glob('.github/workflows/*-service.yml')

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # Replace the buggy condition
    new_content = content.replace(
        "if: github.ref == 'refs/heads/main' || github.event.pull_request.base.ref == 'main'",
        "if: github.ref == 'refs/heads/main'"
    )
    
    with open(file, 'w') as f:
        f.write(new_content)

print("Updated CD conditions.")
