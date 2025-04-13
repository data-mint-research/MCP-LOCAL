#!/usr/bin/env python3
# 📄 Script: add_metadata.py
# 🔧 Zweck: Fügt Metadaten-Blöcke zu Dateien hinzu, die noch keine haben
# 🗂 Pfad: scripts/add_metadata.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: os, sys, re, json, datetime
# 🧪 Testbar: ❌

# HINWEIS (MCP): Dieses Skript ist Teil des MCP-Compliance-Frameworks und fügt
# HINWEIS (MCP): standardisierte Metadaten-Blöcke zu Dateien hinzu, die noch keine haben.
# HINWEIS (MCP): Es unterstützt verschiedene Dateitypen (Python, YAML, Markdown, JSON) und
# HINWEIS (MCP): verwendet Templates aus dem templates-Verzeichnis, um die Metadaten zu generieren.
# HINWEIS (MCP): Das Skript ist ein wichtiges Werkzeug für die Einhaltung der MCP-Dokumentationsstandards.

import os
import sys
import re
import json
from datetime import datetime
import shutil

# Projektverzeichnis (relativ zum Skript)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')

print(f"Projektverzeichnis: {PROJECT_DIR}")
print(f"Templates-Verzeichnis: {TEMPLATES_DIR}")

# Dateitypen und ihre Template-Dateien
FILE_TYPES = {
    '.py': 'script_metadata.template',
    '.yaml': 'yaml_metadata.template',
    '.md': 'markdown_metadata.template',
    '.json': 'json_metadata.template'
}

# Verzeichnisse, die ignoriert werden sollen
IGNORE_DIRS = ['.git', '__pycache__', 'venv', 'env', '.venv', '.env', 'templates']

# Debug-Modus aktivieren
DEBUG = True

def get_today_date():
    """Gibt das aktuelle Datum im Format YYYY-MM-DD zurück."""
    return datetime.now().strftime('%Y-%m-%d')

def get_filename(file_path):
    """Extrahiert den Dateinamen aus dem Dateipfad."""
    return os.path.basename(file_path)

def get_relative_path(file_path):
    """Berechnet den relativen Pfad zum Projektverzeichnis."""
    return os.path.relpath(file_path, PROJECT_DIR)

def infer_purpose(file_path):
    """Leitet den Zweck der Datei aus ihrem Pfad und Namen ab."""
    rel_path = get_relative_path(file_path)
    filename = get_filename(file_path)
    
    # Spezielle Dateien
    if filename == 'README.md':
        return 'Projektdokumentation und Anleitung'
    elif 'test_' in filename:
        return 'Testfälle für die Anwendung'
    elif filename.endswith('.rules.yaml'):
        return 'Regelwerk für die MCP-Struktur'
    elif filename.endswith('.policy.yaml'):
        return 'Richtlinien für die MCP-Komponenten'
    
    # Verzeichnisbasierte Zwecke
    if 'config' in rel_path:
        return 'Konfigurationsdatei für das MCP-System'
    elif 'scripts' in rel_path:
        return 'Hilfsskript für das MCP-System'
    elif 'mcp_units' in rel_path:
        if 'mcp_agent' in rel_path:
            return 'Agent-Komponente des MCP-Systems'
        elif 'mcp_host' in rel_path:
            return 'Host-Komponente des MCP-Systems'
        elif 'mcp_tool' in rel_path:
            return 'Tool-Komponente des MCP-Systems'
        else:
            return 'MCP-Systemkomponente'
    elif 'ui' in rel_path:
        return 'Benutzeroberfläche des MCP-Systems'
    elif 'runtime_state' in rel_path:
        return 'Laufzeitstatus des MCP-Systems'
    
    # Fallback
    return 'Komponente des MCP-Systems'

def infer_packages(file_path):
    """Versucht, benötigte Pakete aus Python-Dateien zu extrahieren."""
    if not file_path.endswith('.py'):
        return 'N/A'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Einfache Regex für Import-Anweisungen
        imports = re.findall(r'^\s*import\s+([a-zA-Z0-9_.,\s]+)', content, re.MULTILINE)
        from_imports = re.findall(r'^\s*from\s+([a-zA-Z0-9_.]+)\s+import', content, re.MULTILINE)
        
        all_imports = []
        for imp in imports:
            all_imports.extend([i.strip() for i in imp.split(',')])
        all_imports.extend(from_imports)
        
        if all_imports:
            return ', '.join(sorted(set(all_imports)))
        else:
            return 'Keine externen Pakete'
    except Exception as e:
        print(f"Fehler beim Extrahieren der Pakete aus {file_path}: {e}")
        return 'Unbekannt'

def get_version():
    """Gibt eine Standardversion zurück."""
    return '1.0.0'

def has_python_yaml_metadata(file_path):
    """Prüft, ob eine Python- oder YAML-Datei bereits einen Metadaten-Block hat."""
    if DEBUG:
        print(f"Prüfe Python/YAML-Metadaten in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(10)])
        
        has_meta = '# 📄' in first_lines
        if DEBUG:
            print(f"  Hat Metadaten: {has_meta}")
        return has_meta
    except Exception as e:
        print(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}")
        return False

def has_markdown_metadata(file_path):
    """Prüft, ob eine Markdown-Datei bereits einen Metadaten-Block hat."""
    if DEBUG:
        print(f"Prüfe Markdown-Metadaten in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(10)])
        
        has_meta = '<!-- 📄' in first_lines or '<!--\n📄' in first_lines
        if DEBUG:
            print(f"  Hat Metadaten: {has_meta}")
        return has_meta
    except Exception as e:
        print(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}")
        return False

def has_json_metadata(file_path):
    """Prüft, ob eine JSON-Datei bereits einen _meta-Block hat."""
    if DEBUG:
        print(f"Prüfe JSON-Metadaten in {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:  # Leere Datei
            if DEBUG:
                print(f"  Leere Datei, hat keine Metadaten")
            return False
        
        try:
            data = json.loads(content)
            has_meta = '_meta' in data
            if DEBUG:
                print(f"  Hat Metadaten: {has_meta}")
            return has_meta
        except json.JSONDecodeError:
            print(f"Warnung: {file_path} ist keine gültige JSON-Datei.")
            return False
    except Exception as e:
        print(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}")
        return False

def has_metadata(file_path):
    """Prüft, ob eine Datei bereits einen Metadaten-Block hat."""
    if file_path.endswith(('.py', '.yaml')):
        return has_python_yaml_metadata(file_path)
    elif file_path.endswith('.md'):
        return has_markdown_metadata(file_path)
    elif file_path.endswith('.json'):
        return has_json_metadata(file_path)
    else:
        return False

def add_python_yaml_metadata(file_path, template_path):
    """Fügt Metadaten zu einer Python- oder YAML-Datei hinzu."""
    if DEBUG:
        print(f"Füge Python/YAML-Metadaten zu {file_path} hinzu")
    try:
        # Template laden und Platzhalter ersetzen
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        metadata = template.format(
            filename=get_filename(file_path),
            purpose=infer_purpose(file_path),
            relative_path=get_relative_path(file_path),
            today=get_today_date(),
            packages=infer_packages(file_path),
            version=get_version()
        )
        
        # Originaldatei lesen
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Metadaten hinzufügen und zurückschreiben
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(metadata + '\n' + content)
        
        print(f"✅ Metadaten zu {file_path} hinzugefügt")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}")
        return False

def add_markdown_metadata(file_path, template_path):
    """Fügt Metadaten zu einer Markdown-Datei hinzu."""
    if DEBUG:
        print(f"Füge Markdown-Metadaten zu {file_path} hinzu")
    try:
        # Template laden und Platzhalter ersetzen
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        metadata = template.format(
            filename=get_filename(file_path),
            purpose=infer_purpose(file_path),
            today=get_today_date()
        )
        
        # Originaldatei lesen
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Metadaten hinzufügen und zurückschreiben
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(metadata + '\n' + content)
        
        print(f"✅ Metadaten zu {file_path} hinzugefügt")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}")
        return False

def add_json_metadata(file_path, template_path):
    """Fügt Metadaten zu einer JSON-Datei hinzu."""
    if DEBUG:
        print(f"Füge JSON-Metadaten zu {file_path} hinzu")
    try:
        # Template laden und Platzhalter ersetzen
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        metadata_text = template.format(
            filename=get_filename(file_path),
            purpose=infer_purpose(file_path),
            today=get_today_date(),
            version=get_version()
        )
        
        # Originaldatei lesen
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:  # Leere Datei
            # Einfach ein neues JSON-Objekt mit Metadaten erstellen
            new_content = metadata_text + '\n}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Metadaten zu leerer JSON-Datei {file_path} hinzugefügt")
            return True
        
        try:
            # Bestehende JSON parsen
            data = json.loads(content)
            
            # Metadaten als JSON parsen
            metadata_json = json.loads(metadata_text + '}')
            
            # Metadaten zum bestehenden JSON hinzufügen
            merged_data = {**metadata_json, **data}
            
            # Zurückschreiben mit schöner Formatierung
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Metadaten zu {file_path} hinzugefügt")
            return True
        except json.JSONDecodeError:
            print(f"⚠️ {file_path} ist keine gültige JSON-Datei, überspringe...")
            return False
    except Exception as e:
        print(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}")
        return False

def add_metadata(file_path):
    """Fügt Metadaten zu einer Datei hinzu, wenn sie noch keine hat."""
    if DEBUG:
        print(f"\nVerarbeite Datei: {file_path}")
    # Dateityp bestimmen
    ext = os.path.splitext(file_path)[1]
    if ext not in FILE_TYPES:
        if DEBUG:
            print(f"  Dateityp {ext} wird nicht unterstützt, überspringe...")
        return False
    
    # Prüfen, ob die Datei bereits Metadaten hat
    if has_metadata(file_path):
        print(f"ℹ️ {file_path} hat bereits Metadaten, überspringe...")
        return False
    
    # Template-Pfad bestimmen
    template_file = FILE_TYPES[ext]
    template_path = os.path.join(TEMPLATES_DIR, template_file)
    
    if DEBUG:
        print(f"  Verwende Template: {template_path}")
    
    # Metadaten hinzufügen
    if ext in ['.py', '.yaml']:
        return add_python_yaml_metadata(file_path, template_path)
    elif ext == '.md':
        return add_markdown_metadata(file_path, template_path)
    elif ext == '.json':
        return add_json_metadata(file_path, template_path)
    
    return False

def process_directory(directory):
    """Verarbeitet alle Dateien in einem Verzeichnis rekursiv."""
    if DEBUG:
        print(f"Verarbeite Verzeichnis: {directory}")
    success_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Ignorierte Verzeichnisse überspringen
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        if DEBUG:
            print(f"Verzeichnis: {root}")
            print(f"  Dateien: {len(files)}")
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            
            if ext in FILE_TYPES:
                total_count += 1
                if add_metadata(file_path):
                    success_count += 1
    
    return success_count, total_count

def main():
    """Hauptfunktion."""
    print("DEBUG-MODUS AKTIVIERT")
    print("🔍 Starte Metadaten-Scan...")
    
    # Prüfen, ob das Templates-Verzeichnis existiert
    if not os.path.exists(TEMPLATES_DIR):
        print(f"❌ Templates-Verzeichnis {TEMPLATES_DIR} nicht gefunden!")
        return 1
    
    # Prüfen, ob alle Template-Dateien existieren
    for ext, template_file in FILE_TYPES.items():
        template_path = os.path.join(TEMPLATES_DIR, template_file)
        if not os.path.exists(template_path):
            print(f"❌ Template-Datei {template_path} für {ext} nicht gefunden!")
            return 1
        else:
            print(f"✅ Template-Datei {template_path} für {ext} gefunden.")
    
    # Verzeichnis verarbeiten
    success_count, total_count = process_directory(PROJECT_DIR)
    
    print(f"\n✅ Fertig! {success_count} von {total_count} Dateien wurden mit Metadaten versehen.")
    return 0

if __name__ == "__main__":
    sys.exit(main())