import shutil
import os
from datetime import datetime
import filecmp

# Carpeta del proyecto a respaldar
proyecto = "C:\\Users\\Matías Requis\\Documents\\main"
backup_dir = "backups"
max_backups = 5  # Máximo de backups a mantener

# Crear carpeta de backups si no existe
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Crear nombre del backup con fecha y hora
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_path = os.path.join(backup_dir, f"{proyecto}_backup_{timestamp}")

# Función para comparar si hay cambios
def hay_cambios(src, dest):
    if not os.path.exists(dest):
        return True
    comparison = filecmp.dircmp(src, dest)
    if comparison.left_only or comparison.right_only or comparison.diff_files:
        return True
    for subdir in comparison.common_dirs:
        if hay_cambios(os.path.join(src, subdir), os.path.join(dest, subdir)):
            return True
    return False

# Verificar si hay cambios desde el último backup
backups_existentes = sorted([f for f in os.listdir(backup_dir) if f.startswith(proyecto+"_backup")])
ultimo_backup = os.path.join(backup_dir, backups_existentes[-1]) if backups_existentes else None

if ultimo_backup and not hay_cambios(proyecto, ultimo_backup):
    print("No hay cambios desde el último backup. ❌")
else:
    shutil.copytree(proyecto, backup_path)
    print(f"Backup realizado ✅\nGuardado en: {backup_path}")

    # Mantener solo los últimos max_backups
    backups_existentes = sorted([f for f in os.listdir(backup_dir) if f.startswith(proyecto+"_backup")])
    while len(backups_existentes) > max_backups:
        viejo_backup = os.path.join(backup_dir, backups_existentes[0])
        shutil.rmtree(viejo_backup)
        backups_existentes.pop(0)
        print(f"Backup antiguo eliminado: {viejo_backup}")