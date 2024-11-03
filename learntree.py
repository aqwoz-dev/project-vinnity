import os


def list_files(startpath, max_depth, current_depth=0):
    if current_depth > max_depth:
        return

    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level > max_depth:
            continue
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        for f in files:
            print(f'{indent}    {f}')

        # Dizinlerde derinliği kısıtlamak
        dirs[:] = dirs[:1]  # Sadece ilk derinliği göster


# Örnek kullanım: Mevcut çalışma dizinini listele, en fazla 2 derinlikte
list_files('.', max_depth=2)
