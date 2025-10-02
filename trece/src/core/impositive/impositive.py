#!/usr/bin/env python3
import typer
from typing import Optional
from pathlib import Path
import sys

# Importaciones al principio - SOLO UNA VEZ
try:
    # Intentar importaciones relativas primero
    from .command.db import db_manager
    from .command.load_entities import load_entities_from_csv, create_entity
    from .command.load_genetics import load_genetics_from_csv, create_genetic
    from .command.load_harvest import load_harvest_from_csv, create_harvest
    from .command.load_withdrawal import load_withdrawal_from_csv, create_withdrawal
    from .command.load_expense import load_expense_from_csv, create_expense
    from .command.load_prices import load_prices_from_csv, create_price
    from .command.reports import generate_balance_report, generate_stock_report
    from .command.stock import rebuild_stock
except ImportError:
    # Fallback para desarrollo
    from command.db import db_manager
    from command.load_entities import load_entities_from_csv, create_entity
    from command.load_genetics import load_genetics_from_csv, create_genetic
    from command.load_harvest import load_harvest_from_csv, create_harvest
    from command.load_withdrawal import load_withdrawal_from_csv, create_withdrawal
    from command.load_expense import load_expense_from_csv, create_expense
    from command.load_prices import load_prices_from_csv, create_price
    from command.reports import generate_balance_report, generate_stock_report
    from command.stock import rebuild_stock

app = typer.Typer(help="Sistema Trece Impositive - Gestión de Cannabis Club")

@app.command()
def init():
    """Inicializar base de datos"""
    try:
        db_manager.initialize_database()
        typer.echo("✅ Base de datos inicializada correctamente")
    except Exception as e:
        typer.echo(f"❌ Error inicializando base de datos: {e}", err=True)

# Grupo de comandos para carga de datos
load_app = typer.Typer(help="Comandos para carga de datos")
app.add_typer(load_app, name="load")

@load_app.command("entities")
def load_entities(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con entidades"),
    name: Optional[str] = typer.Option(None, help="Nombre de la entidad"),
    entity_type: Optional[str] = typer.Option(None, help="Tipo de entidad (socio/proveedor/empleado)"),
    email: Optional[str] = typer.Option(None, help="Email"),
    phone: Optional[str] = typer.Option(None, help="Teléfono")
):
    """Cargar entidades desde CSV o crear una directamente"""
    if file:
        load_entities_from_csv(file)
    elif name and entity_type:
        create_entity(name, entity_type, email, phone)
    else:
        typer.echo("❌ Debe especificar archivo CSV o parámetros para creación directa")

@load_app.command("genetics")
def load_genetics(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con genéticas"),
    name: Optional[str] = typer.Option(None, help="Nombre de la genética"),
    description: Optional[str] = typer.Option(None, help="Descripción")
):
    """Cargar genéticas desde CSV o crear una directamente"""
    if file:
        load_genetics_from_csv(file)
    elif name:
        create_genetic(name, description)
    else:
        typer.echo("❌ Debe especificar archivo CSV o nombre para creación directa")

@load_app.command("harvest")
def load_harvest(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con cosechas"),
    genetic: Optional[str] = typer.Option(None, help="Nombre de la genética"),
    grams: Optional[float] = typer.Option(None, help="Gramos cosechados"),
    date: Optional[str] = typer.Option(None, help="Fecha de cosecha (YYYY-MM-DD)"),
    module: Optional[str] = typer.Option(None, help="Nombre del módulo")
):
    """Cargar cosechas desde CSV o crear una directamente"""
    if file:
        load_harvest_from_csv(file)
    elif genetic and grams and date and module:
        create_harvest(genetic, grams, date, module)
    else:
        typer.echo("❌ Debe especificar archivo CSV o parámetros completos para creación directa")

@load_app.command("withdrawal")
def load_withdrawal(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con retiros"),
    entity: Optional[str] = typer.Option(None, help="Nombre del socio"),
    genetic: Optional[str] = typer.Option(None, help="Nombre de la genética"),
    grams: Optional[float] = typer.Option(None, help="Gramos retirados"),
    date: Optional[str] = typer.Option(None, help="Fecha de retiro (YYYY-MM-DD)"),
    price_type: Optional[str] = typer.Option(
        None, 
        help="Tipo de precio: retail (socio) o wholesale (mayorista)"
    )
):
    """Cargar retiros desde CSV o crear uno directamente"""
    if file:
        load_withdrawal_from_csv(file)
    elif entity and genetic and grams and date:
        create_withdrawal(
            entity_name=entity,
            genetic_name=genetic, 
            grams=grams,
            withdrawal_date=date,
            price_type=price_type
        )
    else:
        typer.echo("❌ Debe especificar archivo CSV o parámetros completos para creación directa")

@load_app.command("expense")
def load_expense(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con gastos"),
    entity: Optional[str] = typer.Option(None, help="Nombre del proveedor"),
    amount: Optional[float] = typer.Option(None, help="Monto del gasto"),
    concept: Optional[str] = typer.Option(None, help="Concepto del gasto"),
    date: Optional[str] = typer.Option(None, help="Fecha del gasto (YYYY-MM-DD)")
):
    """Cargar gastos desde CSV o crear uno directamente"""
    if file:
        load_expense_from_csv(file)
    elif entity and amount and concept and date:
        create_expense(entity, amount, concept, date)
    else:
        typer.echo("❌ Debe especificar archivo CSV o parámetros completos para creación directa")

# Grupo de comandos para reportes
report_app = typer.Typer(help="Comandos para reportes")
app.add_typer(report_app, name="report")

@report_app.command("balance")
def report_balance(
    month: str = typer.Argument(..., help="Mes en formato YYYY-MM"),
    detailed: bool = typer.Option(False, help="Mostrar detalles detallados")
):
    """Generar reporte de balance mensual"""
    generate_balance_report(month, detailed)

@report_app.command("stock")
def report_stock(
    genetic: Optional[str] = typer.Option(None, help="Filtrar por genética (nombre o ID)")
):
    """Generar reporte de stock actual"""
    generate_stock_report(genetic)

# Comandos de mantenimiento
@app.command("rebuild-stock")
def maintenance_rebuild_stock():
    """Reconstruir movimientos de stock desde cero"""
    rebuild_stock()
    typer.echo("✅ Movimientos de stock reconstruidos")

@app.command("version")
def show_version():
    """Mostrar versión del sistema"""
    typer.echo("Trece Impositive v0.1.0")

@load_app.command("prices")
def load_prices(
    file: Optional[Path] = typer.Argument(None, help="Archivo CSV con precios"),
    genetic: Optional[str] = typer.Option(None, help="Nombre de la genética"),
    price: Optional[float] = typer.Option(None, help="Precio por gramo"),
    price_type: Optional[str] = typer.Option("retail", help="Tipo de precio: retail o wholesale"),
    date: Optional[str] = typer.Option(None, help="Fecha de vigencia (YYYY-MM-DD)")
):
    """Cargar precios desde CSV o crear uno directamente"""
    if file:
        from .command.load_prices import load_prices_from_csv
        load_prices_from_csv(file)
    elif genetic and price:
        from .command.load_prices import create_price
        create_price(genetic, price, price_type, date)
    else:
        typer.echo("❌ Debe especificar archivo CSV o parámetros para creación directa")

if __name__ == "__main__":
    app()