import zipfile, io, os

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in os.listdir('.'):
        if f.endswith('.py') and f != 'build_zip.py':
            zf.write(f, f)
    for root, dirs, files in os.walk('pkg_linux'):
        dirs[:] = [d for d in dirs if '__pycache__' not in d and not d.endswith('.dist-info')]
        for file in files:
            if '__pycache__' not in root:
                full = os.path.join(root, file)
                zf.write(full, os.path.relpath(full, 'pkg_linux'))

buf.seek(0)
data = buf.read()
open('deploy.zip', 'wb').write(data)
print(f"ZIP: {len(data)//1024} KB")
