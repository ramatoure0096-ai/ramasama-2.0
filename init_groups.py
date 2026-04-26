import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Vérifie que ton dossier s'appelle bien 'config'
django.setup()

from django.contrib.auth.models import Group, Permission

def create_project_groups():
    groups = ['Vendeur', 'Responsable Commercial', 'Directeur']
    
    for group_name in groups:
        new_group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✅ Groupe '{group_name}' créé avec succès. ✪ ω ✪")
        else:
            print(f"ℹ️ Le groupe '{group_name}' existe déjà. ＞︿＜")

if __name__ == '__main__':
    create_project_groups()