#!/usr/bin/env python3
# alma-cli.py - Interfaz modular para gestión de ALMA_RESIST

import argparse
from pathlib import Path
from datetime import datetime
import yaml
import shutil
import sys

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / 'docs'
LOGS_DIR = BASE_DIR / 'logs' / 'auditorias'

class AlmaCLI:
    def __init__(self, args):
        self.args = args
        self.verbose = args.verbose
        self.processed_files = 0

    def setup_dirs(self):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    def load_rules(self, rules_file):
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                return next(yaml.safe_load_all(f))
        except (yaml.YAMLError, FileNotFoundError) as e:
            self.error_exit(f"Error cargando reglas: {str(e)}")

    def process_md_files(self, processor):
        for md_file in DOCS_DIR.rglob('*.md'):
            try:
                if self.verbose:
                    print(f"🔍 Procesando: {md_file}")
                processor(md_file)
                self.processed_files += 1
            except Exception as e:
                print(f"❌ Error en {md_file}: {str(e)}")
                continue

    def audit_sprint(self):
        rules = self.load_rules(self.args.rules)
        report = {
            'total': 0,
            'domain_issues': [],
            'linked_to_issues': [],
            'suggestions': []
        }

        def auditor(md_file):
            content = md_file.read_text(encoding='utf-8')
            metadata = self.extract_yaml(content)

            if 'domain' in metadata and 'tags' in metadata:
                if metadata['domain'] not in metadata['tags']:
                    report['domain_issues'].append(str(md_file))

            if metadata.get('type') == 'core':
                if not metadata.get('linked_to'):
                    report['linked_to_issues'].append(str(md_file))

        self.process_md_files(auditor)
        self.generate_report(report)

    def batch_update(self):
        field = self.args.field
        value = self.args.value.split(',')
        backup_dir = LOGS_DIR / 'backups' / datetime.now().isoformat()

        def updater(md_file):
            content = md_file.read_text(encoding='utf-8')
            metadata = self.extract_yaml(content)

            if self.args.type and metadata.get('type') != self.args.type:
                return

            if self.args.missing_only and field in metadata:
                return

            backup_path = backup_dir / md_file.relative_to(DOCS_DIR)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(md_file, backup_path)

            metadata[field] = value
            new_content = self.rebuild_content(content, metadata)

            if not self.args.dry_run:
                md_file.write_text(new_content, encoding='utf-8')
                if self.verbose:
                    print(f"✏️ Actualizado: {md_file}")

        self.process_md_files(updater)
        print(f"\n✅ Archivos actualizados: {self.processed_files}")

    def extract_yaml(self, content):
        try:
            yaml_block = content.split('---')[1]
            return yaml.safe_load(yaml_block) or {}
        except IndexError:
            return {}
        except yaml.YAMLError as e:
            self.error_exit(f"Error YAML: {str(e)}")

    def rebuild_content(self, original, metadata):
        new_yaml = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
        return f"---\n{new_yaml}---\n" + original.split('---', 2)[-1]

    def generate_report(self, report_data):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        report_file = LOGS_DIR / f"auditoria_{timestamp}_{self.args.sprint}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Auditoría: {self.args.sprint}\n\n")
            f.write(f"**Documentos procesados:** {self.processed_files}\n\n")

            if report_data['domain_issues']:
                f.write("## Problemas de dominio en tags\n")
                f.write('\n'.join(f"- {f}" for f in report_data['domain_issues']))

            if report_data['linked_to_issues']:
                f.write("\n\n## Core sin linked_to\n")
                f.write('\n'.join(f"- {f}" for f in report_data['linked_to_issues']))

        print(f"📄 Reporte generado: {report_file}")

    def error_exit(self, message):
        print(f"🛑 ERROR: {message}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog='alma-cli', description='Herramienta de gestión para ALMA_RESIST')
    subparsers = parser.add_subparsers(dest='command', required=True)

    audit_parser = subparsers.add_parser('audit', help='Auditoría de documentos')
    audit_parser.add_argument('sprint', help='Nombre identificador del sprint')
    audit_parser.add_argument('--rules', required=True, help='Archivo de reglas YAML')

    update_parser = subparsers.add_parser('batch-update', help='Actualización masiva')
    update_parser.add_argument('--field', required=True, help='Campo a actualizar')
    update_parser.add_argument('--value', required=True, help='Valor a establecer')
    update_parser.add_argument('--type', help='Filtrar por tipo de documento')
    update_parser.add_argument('--missing-only', action='store_true', help='Solo agregar campos faltantes')
    update_parser.add_argument('--dry-run', action='store_true', help='Simular sin realizar cambios')

    parser.add_argument('--verbose', '-v', action='store_true', help='Mostrar detalles de ejecución')

    args = parser.parse_args()
    cli = AlmaCLI(args)
    cli.setup_dirs()

    try:
        if args.command == 'audit':
            cli.audit_sprint()
        elif args.command == 'batch-update':
            cli.batch_update()
    except KeyboardInterrupt:
        cli.error_exit("Operación cancelada por el usuario")

if __name__ == "__main__":
    main()
