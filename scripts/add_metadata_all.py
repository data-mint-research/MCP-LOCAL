#!/usr/bin/env python3
# 📄 Script: add_metadata_all.py
# 🔧 Zweck: Fügt Metadaten-Blöcke zu allen relevanten Dateien hinzu
# 🗂 Pfad: scripts/add_metadata_all.py
# 👤 Autor: MINT-RESEARCH
# 📅 Erstellt: 2025-04-13
# 🧱 Benötigte Pakete: os, sys, re, json, datetime, argparse
# 🧪 Testbar: ❌

import os
import sys
import re
import json
import argparse
from datetime import datetime

# Projektverzeichnis (relativ zum Skript)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATES_DIR = os.path.join(PROJECT_DIR, 'templates')

# Dateitypen und ihre Template-Dateien
FILE_TYPES = {
    '.py': 'script_metadata.template',
    '.yaml': 'yaml_metadata.template',
    '.md': 'markdown_metadata.template',
    '.json': 'json_metadata.template'
}

# Verzeichnisse, die ignoriert werden sollen
IGNORE_DIRS = ['.git', '__pycache__', 'venv', 'env', '.venv', '.env', 'templates']

# Globale Variablen
verbose = False
dry_run = False
force = False
processed_files = []
failed_files = []

def log(message, level=0):
    """Gibt eine Nachricht aus, wenn verbose aktiviert ist oder level 0 ist."""
    if verbose or level == 0:
        print(message)

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
        log(f"Fehler beim Extrahieren der Pakete aus {file_path}: {e}", 1)
        return 'Unbekannt'

def get_version():
    """Gibt eine Standardversion zurück."""
    return '1.0.0'

def has_python_yaml_metadata(file_path):
    """Prüft, ob eine Python- oder YAML-Datei bereits einen Metadaten-Block hat."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(10)])
        
        has_meta = '# 📄' in first_lines
        log(f"  Prüfe Python/YAML-Metadaten in {file_path}: {has_meta}", 2)
        return has_meta
    except Exception as e:
        log(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}", 1)
        return False

def has_markdown_metadata(file_path):
    """Prüft, ob eine Markdown-Datei bereits einen Metadaten-Block hat."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_lines = ''.join([f.readline() for _ in range(10)])
        
        has_meta = '<!-- 📄' in first_lines or '<!--\n📄' in first_lines
        log(f"  Prüfe Markdown-Metadaten in {file_path}: {has_meta}", 2)
        return has_meta
    except Exception as e:
        log(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}", 1)
        return False

def has_json_metadata(file_path):
    """Prüft, ob eine JSON-Datei bereits einen _meta-Block hat."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:  # Leere Datei
            log(f"  Leere JSON-Datei: {file_path}", 2)
            return False
        
        try:
            data = json.loads(content)
            has_meta = '_meta' in data
            log(f"  Prüfe JSON-Metadaten in {file_path}: {has_meta}", 2)
            return has_meta
        except json.JSONDecodeError:
            log(f"Warnung: {file_path} ist keine gültige JSON-Datei.", 1)
            return False
    except Exception as e:
        log(f"Fehler beim Prüfen der Metadaten in {file_path}: {e}", 1)
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
    log(f"  Füge Python/YAML-Metadaten zu {file_path} hinzu", 1)
    
    if dry_run:
        log(f"  [DRY RUN] Würde Metadaten zu {file_path} hinzufügen", 0)
        return True
    
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
        
        log(f"✅ Metadaten zu {file_path} hinzugefügt", 0)
        return True
    except Exception as e:
        log(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}", 0)
        return False

def add_markdown_metadata(file_path, template_path):
    """Fügt Metadaten zu einer Markdown-Datei hinzu."""
    log(f"  Füge Markdown-Metadaten zu {file_path} hinzu", 1)
    
    if dry_run:
        log(f"  [DRY RUN] Würde Metadaten zu {file_path} hinzufügen", 0)
        return True
    
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
        
        log(f"✅ Metadaten zu {file_path} hinzugefügt", 0)
        return True
    except Exception as e:
        log(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}", 0)
        return False

def add_json_metadata(file_path, template_path):
    """Fügt Metadaten zu einer JSON-Datei hinzu."""
    log(f"  Füge JSON-Metadaten zu {file_path} hinzu", 1)
    
    if dry_run:
        log(f"  [DRY RUN] Würde Metadaten zu {file_path} hinzufügen", 0)
        return True
    
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
            log(f"✅ Metadaten zu leerer JSON-Datei {file_path} hinzugefügt", 0)
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
            
            log(f"✅ Metadaten zu {file_path} hinzugefügt", 0)
            return True
        except json.JSONDecodeError:
            log(f"⚠️ {file_path} ist keine gültige JSON-Datei, überspringe...", 0)
            return False
    except Exception as e:
        log(f"❌ Fehler beim Hinzufügen von Metadaten zu {file_path}: {e}", 0)
        return False

def add_metadata(file_path):
    """Fügt Metadaten zu einer Datei hinzu, wenn sie noch keine hat."""
    log(f"\nVerarbeite Datei: {file_path}", 1)
    
    # Dateityp bestimmen
    ext = os.path.splitext(file_path)[1]
    if ext not in FILE_TYPES:
        log(f"  Dateityp {ext} wird nicht unterstützt, überspringe...", 2)
        return False
    
    # Prüfen, ob die Datei bereits Metadaten hat
    if has_metadata(file_path) and not force:
        log(f"ℹ️ {file_path} hat bereits Metadaten, überspringe...", 0)
        return False
    
    # Template-Pfad bestimmen
    template_file = FILE_TYPES[ext]
    template_path = os.path.join(TEMPLATES_DIR, template_file)
    
    log(f"  Verwende Template: {template_path}", 2)
    
    # Metadaten hinzufügen
    success = False
    if ext in ['.py', '.yaml']:
        success = add_python_yaml_metadata(file_path, template_path)
    elif ext == '.md':
        success = add_markdown_metadata(file_path, template_path)
    elif ext == '.json':
        success = add_json_metadata(file_path, template_path)
    
    if success:
        processed_files.append(file_path)
    else:
        failed_files.append(file_path)
    
    return success

def process_directory(directory):
    """Verarbeitet alle Dateien in einem Verzeichnis rekursiv."""
    log(f"Verarbeite Verzeichnis: {directory}", 1)
    success_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Ignorierte Verzeichnisse überspringen
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        log(f"Verzeichnis: {root}", 2)
        log(f"  Dateien: {len(files)}", 2)
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            
            if ext in FILE_TYPES:
                total_count += 1
                if add_metadata(file_path):
                    success_count += 1
    
    return success_count, total_count

def process_single_file(file_path):
    """Verarbeitet eine einzelne Datei."""
    if not os.path.exists(file_path):
        log(f"❌ Datei {file_path} existiert nicht!", 0)
        return 0, 0
    
    ext = os.path.splitext(file_path)[1]
    if ext not in FILE_TYPES:
        log(f"❌ Dateityp {ext} wird nicht unterstützt!", 0)
        return 0, 0
    
    if add_metadata(file_path):
        return 1, 1
    else:
        return 0, 1

def parse_arguments():
    """Parst die Kommandozeilenargumente."""
    parser = argparse.ArgumentParser(description='Fügt Metadaten-Blöcke zu Dateien hinzu.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Ausführliche Ausgabe')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Keine Änderungen vornehmen, nur simulieren')
    parser.add_argument('-f', '--force', action='store_true', help='Vorhandene Metadaten überschreiben')
    parser.add_argument('-s', '--single', help='Nur eine einzelne Datei verarbeiten')
    
    return parser.parse_args()

def main():
    """Hauptfunktion."""
    global verbose, dry_run, force
    
    args = parse_arguments()
    verbose = args.verbose
    dry_run = args.dry_run
    force = args.force
    
    log("🔍 Starte Metadaten-Scan...")
    
    if dry_run:
        log("⚠️ DRY RUN MODUS: Es werden keine Änderungen vorgenommen!")
    
    if force:
        log("⚠️ FORCE MODUS: Vorhandene Metadaten werden überschrieben!")
    
    # Prüfen, ob das Templates-Verzeichnis existiert
    if not os.path.exists(TEMPLATES_DIR):
        log(f"❌ Templates-Verzeichnis {TEMPLATES_DIR} nicht gefunden!")
        return 1
    
    # Prüfen, ob alle Template-Dateien existieren
    for ext, template_file in FILE_TYPES.items():
        template_path = os.path.join(TEMPLATES_DIR, template_file)
        if not os.path.exists(template_path):
            log(f"❌ Template-Datei {template_path} für {ext} nicht gefunden!")
            return 1
        else:
            log(f"✅ Template-Datei {template_path} für {ext} gefunden.", 1)
    
    # Verarbeitung starten
    if args.single:
        log(f"Verarbeite einzelne Datei: {args.single}")
        success_count, total_count = process_single_file(args.single)
    else:
        log(f"Verarbeite Verzeichnis: {PROJECT_DIR}")
        success_count, total_count = process_directory(PROJECT_DIR)
    
    # Ergebnis ausgeben
    log(f"\n✅ Fertig! {success_count} von {total_count} Dateien wurden mit Metadaten versehen.")
    
    if verbose and processed_files:
        log("\nErfolgreich verarbeitete Dateien:")
        for file in processed_files:
            log(f"  ✅ {file}")
    
    if failed_files:
        log("\nFehlgeschlagene Dateien:")
        for file in failed_files:
            log(f"  ❌ {file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())