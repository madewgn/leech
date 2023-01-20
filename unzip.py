import rarfile
def rar(file):
    rar = rarfile.RarFile(file)
    files = [f.filename for f in rar.infolist() if not f.isdir()]
    rar.close()
    return files


