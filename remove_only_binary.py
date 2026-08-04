import glob

files = glob.glob('.github/workflows/*-service.yml')

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    content = content.replace(" --only-binary :all:", "")
    
    with open(file, 'w') as f:
        f.write(content)

print("Removed --only-binary flag from all workflows.")
