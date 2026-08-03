import zipfile, io, os

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in os.listdir('.'):
        if f.endswith('.py') and f != 'build_zip.py':
            zf.write(f, f)
            print(f"  + {f}")
    for root, dirs, files in os.walk('package_fresh'):
        dirs[:] = [d for d in dirs if '__pycache__' not in d and not d.endswith('.dist-info')]
        for file in files:
            if '__pycache__' not in root:
                full = os.path.join(root, file)
                arcname = os.path.relpath(full, 'package_fresh')
                zf.write(full, arcname)

buf.seek(0)
data = buf.read()
with open('deploy.zip', 'wb') as f:
    f.write(data)

z = zipfile.ZipFile('deploy.zip')
fa = [n for n in z.namelist() if n.startswith('fastapi/')]
print(f"fastapi files in ZIP: {len(fa)}")
print(f"ZIP size: {len(data)//1024} KB")
