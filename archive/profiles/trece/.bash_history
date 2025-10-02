mkdir doc
mkdir -p archive/history,backup
mkdir config
nano config/config.yaml
mkdir meta
nano meta/schema.sql
nano meta/schema.yaml
mkdir src
mkdir database
nano database/trece.db
nano archive/README.md
mkdir tmp && echo tmp/README.md
echo tmp/README.md
echo ~/trece/tmp/README.md
rm -rf archive/history,backup/
mkdir -p archive/backup history
mkdir -p archive/exports
mkdir -p archive/history
mkdir -p src/{util,script,core}
tree -l
tree
sqlite3 database/trece.db 
ls
mv ~/\@arca/modules/13cc/docs/* ~/trece/doc/
tree -l doc/
rm -rf archive/*
mv ~/\@arca/modules/13cc/archive/* ~/trece/archive/
mkdir templates
ls
cd archive/
ls
cd ..
mv ~/\@arca/modules/13cc/templates/* ~/trece/templates/
mv ~/\@arca/modules/13cc/templates/* ~/trece/templates/
cd archive/
cd ..
cd ..
cd ..
cd archive/
tree -l
cd ..
ls
tree -L 2
mkdir logs
ls
ls
TRECE_CONFIG
tree -L 2
mkdir -p archive/history/13cc_db && mv ~/\@arca/modules/13cc/database/* archive/history/13cc_db
mkdir -p archive/history/schemas && mv ~/\@arca/modules/13cc/meta/* archive/history/schemas
mkdir -p data/impositive
rm -rf data/impositive
nano data/tables.csv
nix-shell
ls
mv data src/
ls
ls src
mv src/data ~/trece/
ls tmp
ls
rm history/
rm -rf history/
ls
cd templates/
ls
mv contables impositive
ls
mkdir -p data/impositive
ls data/
ls
ls data/
rm -rf data/
ls
cd ..
mkdir -p data/impositive && mv data/tables.csv data/impositive/
nano data/README.md
nano data/impositive/README.md
tree -L 3
mkdir -p data/entitys
nano data/entitys/reprocanns.csv
nano data/withdraws.csv
cp archive/exports/genetics_20250813_171746.csv data/genetics.csv
ls data
cp archive/exports/harvest_detail_20250813_171746.csv data/harvest_detail.csv
ls data
mv data/withdraws.csv data/withdrawals.csv
ls data
mkdir -p src/doc
tree -l
rm -rf data/entitys/
ls data
rm data/withdrawals.csv 
rm data/harvest_detail.csv 
rm data/reprocanns.csv 
rm data/genetics.csv 
md data/impositive/tables.csv data/actual_tables.csv
mv data/impositive/tables.csv data/actual_tables.csv
rm -rf data/impositive/
mkdir -p data/actual_tables && mv data/actual_tables.csv data/actual_tables/ 
mkdir -p data/gastos_2025 && nano data/gastos_2025/gastos_2025.csv
python3
nano setup.py
cd src/util/
nano config.py
cd ..
mkdir test
nano test/test_config.py
cd .
cd ..
nano __init__.py
mv src/util/config.py src/core/
mv src/core/config.py src/core/load_config.py
pip install -e
pytest --version
pytest -vs src/test/test_config.py
pytest src/test/test_config.py 
pip install -e .
nano src/__init__.py
pytest src/test/test_config.py 
cp src/__init__.py src/core/
cp src/__init__.py src/util/
cp src/__init__.py src/test/
cd src/
ls
mv script scripts
mv util utils
mv test tests
mv scripts script
mv utils util
mv tests test
# Desde /home/arca/trece/
pip install -e .
cd ..
# Desde /home/arca/trece/
pip install -e .
mkdir -p archive/backup/nix-shell && cp shell.nix archive/backup/nix-shell/202508172025_shell.nix.bak
exit
clear
mkdir -p doc/src/
mkdir -p doc/src/core
nano doc/src/core/load_config.md
13
nix-shell
rm -rf doc/src/
ls doc/
mkdir -p doc/prompt
nano doc/prompt/prompt_load_config.md
nano .gitignore
ls
nano tmp/README.md
nano src/core/version.py
cp shell.nix archive/backup/nix-shell/202508180747_shell.nix.bak
ls
exit
ls
python -c "from core.version import __version__; print(__version__)"
rm setup.py 
mv src/doc/backup.py.md doc/prompt/backup_mannager.md
rm -rf src/doc/
rm __init__.py 
nano templates/README.md
rm -rf src/core/__pycache__
exit
13
13
nix-shell --pure
which nix-shell || echo "Nix no está instalado"
cd ..
ls
nix-shell --version
# Debería mostrar algo como: "nix-shell (Nix) 2.23.1"
nix-shell --version
mkdir /tmp/test-nix && cd /tmp/test-nix
echo '{ pkgs ? import <nixpkgs> {} }: pkgs.mkShell { buildInputs = [ pkgs.bash ]; }' > shell.nix
nix-shell --pure
ls
exit
13
exit
nix-shell --pure
exit
nix-shell
mv data/gastos_2025 data/gastos
mv data/gastos/gastos_2025.csv data/gastos/gastos.csv
python3
mv data/gastos/gastos.csv data/actual_tables/expenses.csv
ls data/actual_tables/
rmdir data/gastos/
mv src/test/test_config.py src/test/test_load_config.py
rmdir src/test/__pycache__/
rm -rf src/test/__pycache__/
cd src/
tree -l
mkdir -p .vscode && nano .vscode/settings.json
mv .vscode/ ../
cd ..
python -m pip show pytest
nano setup.py
pip install -e
pip install -e .
exit
13
pip install -e .
PYTHONPATH=src pytest src/test/test_load_config.py -v
exit
nix-shell
exit
13
13
nix-shell
nix-shell --pure
exit
nix-shell
nix-shell
nix-shell
nix-shell
xd ~/trece/
cd ~/trece/
ls
pytest
find ~/trece/src -type d -name "__pycache__" -exec rm -rf {} +
tree -l src
nano src/core/backup_manager.py
mv doc/prompt/ dev/
mv dev/ doc/
mv doc/dev/prompt/ doc/
nano src/test/test_backup_manager.py
pytest
pytest src/core/test/test_backup_manager.py -v
find . -name "test_backup_manager.py"
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
python3 -m py_compile src/core/backup_manager.py
pytest src/test/test_backup_manager.py -v
find . -name "*.pyc" -delete
rm -rf .pytest_cache
exit
nix-shell
cd ..
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest src/test/test_backup_manager.py -v
pytest
find ~/trece/src -type d -name "__pycache__" -exec rm -rf {} +
tree -l src/
echo "Contenido inicial" > ~/trece/database/prueba.txt
for i in {1..15}; do   echo "Versión $i" > ~/trece/database/prueba.txt;   python3 -m src.core.backup_manager backup database/prueba.txt;   sleep 1  # Esperar para generar timestamps diferentes
done
python3 -m src.core.backup_manager list database/prueba.txt
python3 -m src.core.backup_manager backup database/prueba.txt 
# Desde el directorio raíz del proyecto (~/trece)
python3 -m src.core.backup_manager backup database/prueba.txt
mv src/test/ src/core/
mv src/util/ src/core/
find ~/trece/src -type d -name "__pycache__" -exec rm -rf {} +
pytest
find ~/trece/src -type d -name "__pycache__" -exec rm -rf {} +
tree -l src/
# Verificar estructura de archivos
[trece:~/trece]$ find src/ -type f -name "*.py"
src/__init__.py
src/core/__init__.py
src/core/backup_manager.py
src/core/load_config.py
src/core/test/__init__.py
src/core/test/test_backup_manager.py
src/core/test/test_load_config.py
src/core/util/__init__.py
src/core/version.py
pip install -e
pip install -e .
nano setup.cfg
mkdir requirements
ls
nano requirements/base.txt
nano requirements/dev.txt
nano requirements/prod.txt
nano pyproject.toml
tree -L 2
rm database/prueba.txt 
rm -rf requirements/
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"  # Instala el paquete en modo editable + extras de desarrollo
pip list  # Mostrará "trece" como paquete instalado
rm setup.py
rm setup.cfg 
pip freeze > requirements.txt  # Solo para ese caso
pytest
find ~/trece/src -type d -name "__pycache__" -exec rm -rf {} +
nano doc/dev/utils/commands.md
nano src/cli.py
pip install -e .
pytest trece/src/core/test/test_load_config.py -v
pip uninstall trece
pip install -e .
pip install -e .
pip uninstall trece  # Por si acaso hay una instalación previa
pip install -e .
python -c "from trece.src.core.load_config import config; print(config)"
nano data/actual_tables/withdrawals.csv
nano data/actual_tables/settings.csv
mkdir -p data/impositive
nano data/impositive/entities.csv
mkdir -p archive/bakcu/data/actual_tables
mkdir -p archive/bakcup/data/actual_tables
mkdir -p archive/backup/data/actual_tables
rmdir archive/bakcu
rm -rf archive/bakcu
rm -rf archive/bakcup
cp data/actual_tables/expenses.csv archive/backup/data/actual_tables/202508192318_withdrawals.csv.bak
cp data/actual_tables/withdrawals.csv archive/backup/data/actual_tables/202508192323_withdrawals.csv.bak
cp data/actual_tables/actual_tables.csv archive/backup/data/actual_tables/202508192323_actual_tables.csv.bak
rm data/actual_tables/settings.csv 
mv data/impositive/entities.csv data/
rm -rf data/entities.csv 
rm -rf data/impositive/
nano data/entities.csv
nano data/entities_types.csv
nano data/concepts.csv
mv data/actual_tables/expenses.csv data/
mv data/actual_tables/withdrawals.csv data/
nano data/genetics.csv
nano data/modules.csv
nano data/harvest.csv
nano data/harvest_detail.csv
rm -rf data/actual_tables/
tree -l data/
import pandas as pd
# Ruta al CSV
csv_path = "~/trece/data/expenses.csv"
# Cargar el archivo
df = pd.read_csv(csv_path)
# Calcular el total de la columna amount
total_amount = df["amount"].sum()
print("Total amount en expenses:", total_amount)
nano src/script/sum_expenses.py
python3 src/script/sum_expenses.py 
nano src/script/sum_withdrawals.py
python3 src/script/sum_withdrawals.py 
nano src/script/harvest_stock.py
python3 src/script/harvest_stock.py 
python3 src/script/harvest_stock.py 
python3 src/script/harvest_stock.py 
python3 src/script/harvest_stock.py 
nano doc/prompt/prompt_base_de_datos_trece_db.md
mv meta/schema.sql meta/trecedb.sql
nano src/script/import_data.py
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
tree -l data
nano src/script/retiros_por_socio.py
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
python3 src/script/import_data.py 
sqlite3 database/trece.db 
python3 src/script/retiros_por_socio.py 
mkdir -p src/script/data
python3 src/script/data/retiros_por_socio.py 
python3 src/script/data/harvest_stock.py 
python3 src/script/data/sum_expenses.py 
python3 src/script/data/sum_withdrawals.py 
python3 src/script/data/sum_withdrawals.py 
python3 src/script/data/sum_withdrawals.py 
nano src/script/data/gastos_por_entidad_y_concepto.py
cd ~/trece/src/script
python3 gastos_por_entidad_y_concepto.py
cd ..
cd ..
python3 src/script/data/gastos_por_entidad_y_concepto.py 
nano src/script/data/stock_actual.py
python3 src/script/data/stock_actual.py 
python3 src/script/data/sum_expenses.py 
python3 src/script/data/sum_withdrawals.py 
python3 src/script/data/sum_expenses.py 
python3 src/script/data/sum_withdrawals.py 
nano src/script/data/dashboard_mensual.py
python3 src/script/data/dashboard_mensual.py 
python3 src/script/data/dashboard_mensual.py 
python3 src/script/data/dashboard_mensual.py 
nano src/script/data/balance_mes_actual.py
python3 src/script/data/balance_mes_actual.py 
python3 src/script/data/balance_mes_actual.py 
nano doc/text.txt
python3 src/core/backup.py backup ~/trece/doc/text.txt 
python3 src/core/backup.py restore ~/trece/doc/text.txt 
python3 src/core/backup.py restore ~/trece/doc/text.txt 
sqlite3 database/trece.db 
rm database/trece.db && nano database/trece.db 
rm database/trece.db && nano database/trece.db 
stock
stock
rps
rps
rps
rps
with
with
with
with
with
nano data/withdrawals.prices.csv 
nano data/paymethods.csv
tree -l data/
tree -l data/
backup src/script/data/balance_mes_actual.py 
python3 ~/trece/src/script/data/balance_mes_actual.py 
python3 ~/trece/src/core/backup.py backup src/script/data/balance_mes_actual.py 
python3 ~/trece/src/core/backup.py backup src/script/data/*
python3 ~/trece/src/core/backup.py backup src/script/data/dashboard_mensual.py 
python3 ~/trece/src/core/backup.py backup src/script/data/gastos_por_entidad_y_concepto.py 
python3 ~/trece/src/core/backup.py backup src/script/data/harvest_stock.py 
python3 ~/trece/src/core/backup.py backup src/script/data/retiros_por_socio.py 
python3 ~/trece/src/core/backup.py backup src/script/data/stock_actual.py 
python3 ~/trece/src/core/backup.py backup src/script/data/sum_expenses.py 
python3 ~/trece/src/core/backup.py backup src/script/data/sum_withdrawals.py 
nano doc/prompt/trece.data.cli.py
mv doc/prompt/trece.data.cli.py doc/prompt/trece.data.cli.md
mv doc/prompt/trece.data.cli.md doc/prompt/data_cli.md
tree -l data
tree -l src/script/data/
nano src/core/data_cli.py
python3 src/core/data_cli.py 
python3 src/core/data_cli.py 
13
python3 src/core/data_cli.py 
source .venv/bin/activate
asd
ls
ls
env
actenv
13
tmux
source .bashrc
backup doc/prompt/prompt_data_cli_v0.1.0.py.md 
backup src/core/data_cli.py 
source .bashrc
restore doc/prompt/prompt_data_cli_v0.1.0.py.md 
cd ~/trece/
ls
13
cd ..
source .bashrc
13
nano .bashrc
source .bashrc
imp
imp
im
python3 src/core/data_cli.py 
mkdir -p data/impositive
mv data/* data/impositive/
mv data/* data/impositive
cp data/* data/impositive/
cp -r data/* data/impositive/
rm -rf data/impositive/impositive/
mv data/impositive/README.md data/
imp
tree -l archive/
nano doc/prompt/prompt_versionado.md
nano src/core/versionado.py
nano trece
chmod +x ~/trece/trece
echo 'export PATH="$HOME/trece:$PATH"' >> ~/.bashrc
source .bashrc
trece versionar doc/prompt/prompt_versionado.md 
which trece
python3 ~/trece/src/core/versionado.py versionar doc/text.txt 
nano doc/test.md
python3 ~/trece/src/core/versionado.py versionar doc/test.md 
python3 ~/trece/src/core/versionado.py versionar doc/test.md 
mv archive/exports/ archive/active/
python3 ~/trece/src/core/versionado.py versionar src/core/backup.py 
python3 ~/trece/src/core/versionado.py versionar src/core/backup.py 
python3 ~/trece/src/core/versionado.py versionar src/core/backup.py 
python3 ~/trece/src/core/versionado.py versionar src/core/backup.py 
imp
imp
nano doc/control_general/vege.xlsx
imp
13
13
13
imp
imp
13
imp
13
13
nano data/impositive/boxes.csv
nano data/impositive/boxes_types.csv
rm data/impositive/boxes_types.csv 
cd ..
nano .bashrc
13
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar doc/prompt/prompt_versionado.md 
rm -rf archive/history/doc/
rm archive/history/trece/doc/test_v0.1.0.md 
versionar src/core/backup.py 
versionar src/core/backup.py 
nano templates/metadatos_script.py
versionar src/script/data/balance_mes_actual.py 
rm src/script/data/balance_mes_actual.py 
versionar src/script/data/dashboard_mensual.py && rm src/script/data/dashboard_mensual.py 
versionar src/script/data/gastos_por_entidad_y_concepto.py && rm src/script/data/gastos_por_entidad_y_concepto.py 
versionar src/script/data/sum_expenses.py && rm src/script/data/sum_expenses.py 
versionar src/script/data/stock_actual.py && rm src/script/data/stock_actual.py 
versionar src/script/data/retiros_por_socio.py && rm src/script/data/retiros_por_socio.py 
versionar src/script/data/harvest_stock.py && rm src/script/data/harvest_stock.py 
versionar src/script/data/sum_withdrawals.py && rm src/script/data/sum_withdrawals.py 
rm -rf src/script/data/
rm src/script/import_data.py 
which trece
versionar src/core/data_cli.py 
mkdir -p src/cli
cp src/core/data_cli.py src/cli/data.py
python3 src/cli/data.py 
versionar src/cli/data.py 
nano test.txt
cp src/core/backup.py src/script/backup.py
python3 src/script/backup.py backup test.txt 
rm /home/arca/trece/archive/backup/trece/test.txt.20250821_175503.bak
rm test.txt 
source .bashrc
versionar src/script/backup.py 
mv src/core/versionado.py src/script/versionado.py
source .bashrc
versionar src/script/versionado.py 
mkdir -p src/util
rm -rf src/core/util/
python3 src/cli/data.py 
source .bashrc
ipm
imp
mkdir .dev
mv doc/dev/* .dev
rm -rf doc/dev/
mkdir -p doc/cannabis_club
mv doc/compliance/ doc/cannabis_club/
mv doc/legal/ doc/cannabis_club/
rm doc/test.md 
rm doc/text.txt 
mv doc docs
mv docs/journal/ docs/cannabis_club/
backup data/impositive/boxes.csv 
13
imp
mv src/cli/data.py tmp/
versionar src/cli/data.py 
rm src/cli/data.py 
mv tmp/data.py src/cli/
versionar doc/prompt/backup.py.md 
versionar doc/prompt/base_de_datos_trece_db.md 
versionar doc/prompt/data_cli_v0.1.1.py.md 
versionar doc/prompt/load_config.md 
versionar doc/prompt/versionado.md 
mv doc/prompt/data_cli.md tmp/
versionar doc/prompt/data_cli.md 
rm doc/prompt/data_cli.md 
mv tmp/data_cli.md doc/prompt/
imp
mv doc/gestion_conjunta/ doc/control_general/
backup src/cli/data.py 
versionar src/core/load_config.py 
versionar src/core/version.py 
imp
imp
imp
imp
versionar data/impositive/boxes.csv 
backup data/impositive/concepts.csv 
backup data/impositive/entities_types.csv 
backup data/impositive/entities.csv 
backup data/impositive/expenses.csv 
backup data/impositive/genetics.csv 
backup data/impositive/harvest_detail.csv 
backup data/impositive/harvest.csv 
backup data/impositive/modules.csv 
backup data/impositive/paymethods.csv 
backup data/impositive/prices.csv 
backup data/impositive/withdrawals.csv 
mkdir -p doc/prompt/data_cli
mv doc/prompt/data_cli.md doc/prompt/data_cli/
mkdir -p doc/prompt/backup headers_trece_db load_config versionado
rm -rf doc/prompt/backup
mkdir -p doc/prompt/{backup,headers_trece_db,load_config,versionado}
versionar doc/prompt/backup/backup.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/headers_trece_db/headers_trece_db.md 
versionar doc/prompt/load_config/load_config.md 
versionar doc/prompt/versionado/versionado.md 
versionar doc/prompt/data_cli/data_cli.md 
restore src/cli/data.py 
imp
mkdir data/impositive/movements
mv data/impositive/withdrawals.csv data/impositive/movements/
imp
help
clear
imp
imp
13
13
13
13
13
imp
imp
tmux
tmux
imp
13
tree -L 2
13
imp
mkdir -p data/impositive/settings
imp
versionar src/cli/data.py 
mkdir -p src/cli/impositive
cp src/cli/data.py src/cli/impositive/main.py
source .bashrc
imp
13
cd data
tree -l
mkdir impositive/harvest
mv impositive/harvest.csv impositive/harvest
tree -l
mv impositive/harvest_detail.csv impositive/harvest
tree -l
mkdir -p shed
tree -l
mv impositive/paymethods.csv impositive/settings/
tree -l
mdkir -p management
mkdir management
tree -l
mv impositive/ management/
tree -l
mv shed/ management/
tree -l
mv management/impositive/modules.csv management/shed/
tree -l
mv management/impositive/harvest/ management/shed/
tree -l
mv management/impositive/settings/ management/
tree -l
mkdir -p management/shed/genetics && mv management/impositive/genetics.csv management/shed/genetics/ 
tree -l
mkdir -p management/people
tree -l
mv management/impositive/entities.csv management/people/
tree -l
mkdir -p management/impositive/boxes
mv management/impositive/boxes.csv management/impositive/boxes
tree -l
mkdir -p management/shed/modules
mv management/shed/modules.csv management/shed/modules
tree -l
imp
imp
imp
tree -l
cd ..
tree -L 1
rm -rf load_config/
imp
mkdir -p data/bitacoras
mkdir -p templates/prompt/
nano templates/prompt/prompt.md
mkdir -p templates/metadatos
mkdir -p templates/script
mkdir -p templates/file
ls
mkdir -p doc/prompt/bitacora
cp templates/prompt/prompt.md doc/prompt/bitacora/bitacora.md
imp
versionar src/cli/impositive/data.py 
versionar doc/prompt/data_cli/data_cli.md 
imp
versionar doc/prompt/data_cli/data_cli.md 
mkdir -p doc/respuesta
mkdir -p doc/respuesta/data_cli
imp
imp
versionar src/cli/impositive/data.py 
imp
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/changelog.md 
imp
imp
13
imp
python3 archive/history/trece/src/cli/impositive/data_v0.1.4.py
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
nano config/config.py
rm config/config.py 
cp templates/script/script.py config/config.py
python3
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
mkdir -p .dev/src/{core,util,script,config}
ls .dev/src/
nano .dev/src/config/config.py
mkdir -p .dev/doc
mv .dev/* .dev/doc/
mv .dev/doc/src/ .dev/
nano .dev/.bashrc
nano .dev/requirements.txt
mkdir -p .dev/data/bitacora
mkdir -p .dev/database
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
dev
cd .dev/
tree -l
cd ..
home
13
13
home
backup doc/utils/tmux.md 
versionar doc/utils/tmux.md 
versionar doc/utils/comandos_utiles_sql.md 
deactivate
python3 -m venv ~/trece/.dev/.venv
cd ..
cd ..
nano .bashrc
13
home
deactiva
deactivate
cd ..
home
which python
echo $VIRTUAL_ENV
13
which python
echo $VIRTUAL_ENV
home
cp ../templates/ 
cp ../templates/ .
cp ../templates/ .dev/
mkdir -p doc/prompt/config && cp ../templates/prompt/prompt.md doc/prompt/config.md 
cp ../templates/script/script.py src/config/config.py
mkdir archive/{backup,history}
mkdir -p archive/{backup,history}
mkdir templates
mkdir meta
python3 src/config/config.py 
python3 config.py 
python3 config.py 
python3 config.py 
mkdir logs
python3 config.py 
python3 config.py 
python3 config.py 
python3 config.py 
versionar config.py 
python3
python3 config.py 
mv config.py config/
mv utils/ doc/
mkdir -p templates/script
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
cd data/management/
tree -l
imp
cd ..
cd ..
ls
nano data/impositive/boxes_types.csv
rm data/impositive/boxes_types.csv 
cd ..
nano .bashrc
13
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar doc/prompt/prompt_versionado.md 
rm -rf archive/history/doc/
rm archive/history/trece/doc/test_v0.1.0.md 
versionar src/core/backup.py 
versionar src/core/backup.py 
nano templates/metadatos_script.py
versionar src/script/data/balance_mes_actual.py 
rm src/script/data/balance_mes_actual.py 
versionar src/script/data/dashboard_mensual.py && rm src/script/data/dashboard_mensual.py 
versionar src/script/data/gastos_por_entidad_y_concepto.py && rm src/script/data/gastos_por_entidad_y_concepto.py 
versionar src/script/data/sum_expenses.py && rm src/script/data/sum_expenses.py 
versionar src/script/data/stock_actual.py && rm src/script/data/stock_actual.py 
versionar src/script/data/retiros_por_socio.py && rm src/script/data/retiros_por_socio.py 
versionar src/script/data/harvest_stock.py && rm src/script/data/harvest_stock.py 
versionar src/script/data/sum_withdrawals.py && rm src/script/data/sum_withdrawals.py 
rm -rf src/script/data/
rm src/script/import_data.py 
which trece
versionar src/core/data_cli.py 
mkdir -p src/cli
cp src/core/data_cli.py src/cli/data.py
python3 src/cli/data.py 
versionar src/cli/data.py 
nano test.txt
cp src/core/backup.py src/script/backup.py
python3 src/script/backup.py backup test.txt 
rm /home/arca/trece/archive/backup/trece/test.txt.20250821_175503.bak
rm test.txt 
source .bashrc
versionar src/script/backup.py 
mv src/core/versionado.py src/script/versionado.py
source .bashrc
versionar src/script/versionado.py 
mkdir -p src/util
rm -rf src/core/util/
python3 src/cli/data.py 
source .bashrc
ipm
imp
mkdir .dev
mv doc/dev/* .dev
rm -rf doc/dev/
mkdir -p doc/cannabis_club
mv doc/compliance/ doc/cannabis_club/
mv doc/legal/ doc/cannabis_club/
rm doc/test.md 
rm doc/text.txt 
mv doc docs
mv docs/journal/ docs/cannabis_club/
backup data/impositive/boxes.csv 
13
imp
mv src/cli/data.py tmp/
versionar src/cli/data.py 
rm src/cli/data.py 
mv tmp/data.py src/cli/
versionar doc/prompt/backup.py.md 
versionar doc/prompt/base_de_datos_trece_db.md 
versionar doc/prompt/data_cli_v0.1.1.py.md 
versionar doc/prompt/load_config.md 
versionar doc/prompt/versionado.md 
mv doc/prompt/data_cli.md tmp/
versionar doc/prompt/data_cli.md 
rm doc/prompt/data_cli.md 
mv tmp/data_cli.md doc/prompt/
imp
mv doc/gestion_conjunta/ doc/control_general/
backup src/cli/data.py 
versionar src/core/load_config.py 
versionar src/core/version.py 
imp
imp
imp
imp
versionar data/impositive/boxes.csv 
backup data/impositive/concepts.csv 
backup data/impositive/entities_types.csv 
backup data/impositive/entities.csv 
backup data/impositive/expenses.csv 
backup data/impositive/genetics.csv 
backup data/impositive/harvest_detail.csv 
backup data/impositive/harvest.csv 
backup data/impositive/modules.csv 
backup data/impositive/paymethods.csv 
backup data/impositive/prices.csv 
backup data/impositive/withdrawals.csv 
mkdir -p doc/prompt/data_cli
mv doc/prompt/data_cli.md doc/prompt/data_cli/
mkdir -p doc/prompt/backup headers_trece_db load_config versionado
rm -rf doc/prompt/backup
mkdir -p doc/prompt/{backup,headers_trece_db,load_config,versionado}
versionar doc/prompt/backup/backup.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/headers_trece_db/headers_trece_db.md 
versionar doc/prompt/load_config/load_config.md 
versionar doc/prompt/versionado/versionado.md 
versionar doc/prompt/data_cli/data_cli.md 
restore src/cli/data.py 
imp
mkdir data/impositive/movements
mv data/impositive/withdrawals.csv data/impositive/movements/
imp
help
clear
imp
imp
13
13
13
13
13
imp
imp
tmux
tmux
imp
13
tree -L 2
13
imp
mkdir -p data/impositive/settings
imp
versionar src/cli/data.py 
mkdir -p src/cli/impositive
cp src/cli/data.py src/cli/impositive/main.py
source .bashrc
imp
13
cd data
tree -l
mkdir impositive/harvest
mv impositive/harvest.csv impositive/harvest
tree -l
mv impositive/harvest_detail.csv impositive/harvest
tree -l
mkdir -p shed
tree -l
mv impositive/paymethods.csv impositive/settings/
tree -l
mdkir -p management
mkdir management
tree -l
mv impositive/ management/
tree -l
mv shed/ management/
tree -l
mv management/impositive/modules.csv management/shed/
tree -l
mv management/impositive/harvest/ management/shed/
tree -l
mv management/impositive/settings/ management/
tree -l
mkdir -p management/shed/genetics && mv management/impositive/genetics.csv management/shed/genetics/ 
tree -l
mkdir -p management/people
tree -l
mv management/impositive/entities.csv management/people/
tree -l
mkdir -p management/impositive/boxes
mv management/impositive/boxes.csv management/impositive/boxes
tree -l
mkdir -p management/shed/modules
mv management/shed/modules.csv management/shed/modules
tree -l
imp
imp
imp
tree -l
cd ..
tree -L 1
rm -rf load_config/
imp
mkdir -p data/bitacoras
mkdir -p templates/prompt/
nano templates/prompt/prompt.md
mkdir -p templates/metadatos
mkdir -p templates/script
mkdir -p templates/file
ls
mkdir -p doc/prompt/bitacora
cp templates/prompt/prompt.md doc/prompt/bitacora/bitacora.md
imp
versionar src/cli/impositive/data.py 
versionar doc/prompt/data_cli/data_cli.md 
imp
versionar doc/prompt/data_cli/data_cli.md 
mkdir -p doc/respuesta
mkdir -p doc/respuesta/data_cli
imp
imp
versionar src/cli/impositive/data.py 
imp
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/changelog.md 
imp
imp
13
imp
python3 archive/history/trece/src/cli/impositive/data_v0.1.4.py
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
nano config/config.py
rm config/config.py 
cp templates/script/script.py config/config.py
python3
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
mkdir -p .dev/src/{core,util,script,config}
ls .dev/src/
nano .dev/src/config/config.py
mkdir -p .dev/doc
mv .dev/* .dev/doc/
mv .dev/doc/src/ .dev/
nano .dev/.bashrc
nano .dev/requirements.txt
mkdir -p .dev/data/bitacora
mkdir -p .dev/database
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
dev
cd .dev/
tree -l
cd ..
home
13
13
home
backup doc/utils/tmux.md 
versionar doc/utils/tmux.md 
versionar doc/utils/comandos_utiles_sql.md 
deactivate
python3 -m venv ~/trece/.dev/.venv
cd ..
cd ..
nano .bashrc
13
home
deactiva
deactivate
cd ..
home
which python
echo $VIRTUAL_ENV
13
which python
echo $VIRTUAL_ENV
home
cp ../templates/ 
cp ../templates/ .
cp ../templates/ .dev/
mkdir -p doc/prompt/config && cp ../templates/prompt/prompt.md doc/prompt/config.md 
cp ../templates/script/script.py src/config/config.py
mkdir archive/{backup,history}
mkdir -p archive/{backup,history}
mkdir templates
mkdir meta
python3 src/config/config.py 
python3 config.py 
python3 config.py 
python3 config.py 
mkdir logs
python3 config.py 
python3 config.py 
python3 config.py 
python3 config.py 
versionar config.py 
python3
python3 config.py 
mv config.py config/
mv utils/ doc/
mkdir -p templates/script
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
cd data/management/
tree -l
imp
cd ..
cd ..
ls
home
home
source .bashrc
home
nano ../../.bashrc
imp
python3 ../archive/history/trece/src/cli/impositive/data_v0.1.3.py 
python3 ../archive/history/trece/src/cli/impositive/data_v0.1.2.py 
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
python3 ~/trece/.dev/src/script/backup/backup.py backup .dev/src/script/backup/backup.py 
home
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/backup/backup.py backup src/backup/backup.py 
python3 src/backup/backup.py backup src/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
home
nano data/impositive/boxes_types.csv
rm data/impositive/boxes_types.csv 
cd ..
nano .bashrc
13
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar doc/prompt/prompt_versionado.md 
rm -rf archive/history/doc/
rm archive/history/trece/doc/test_v0.1.0.md 
versionar src/core/backup.py 
versionar src/core/backup.py 
nano templates/metadatos_script.py
versionar src/script/data/balance_mes_actual.py 
rm src/script/data/balance_mes_actual.py 
versionar src/script/data/dashboard_mensual.py && rm src/script/data/dashboard_mensual.py 
versionar src/script/data/gastos_por_entidad_y_concepto.py && rm src/script/data/gastos_por_entidad_y_concepto.py 
versionar src/script/data/sum_expenses.py && rm src/script/data/sum_expenses.py 
versionar src/script/data/stock_actual.py && rm src/script/data/stock_actual.py 
versionar src/script/data/retiros_por_socio.py && rm src/script/data/retiros_por_socio.py 
versionar src/script/data/harvest_stock.py && rm src/script/data/harvest_stock.py 
versionar src/script/data/sum_withdrawals.py && rm src/script/data/sum_withdrawals.py 
rm -rf src/script/data/
rm src/script/import_data.py 
which trece
versionar src/core/data_cli.py 
mkdir -p src/cli
cp src/core/data_cli.py src/cli/data.py
python3 src/cli/data.py 
versionar src/cli/data.py 
nano test.txt
cp src/core/backup.py src/script/backup.py
python3 src/script/backup.py backup test.txt 
rm /home/arca/trece/archive/backup/trece/test.txt.20250821_175503.bak
rm test.txt 
source .bashrc
versionar src/script/backup.py 
mv src/core/versionado.py src/script/versionado.py
source .bashrc
versionar src/script/versionado.py 
mkdir -p src/util
rm -rf src/core/util/
python3 src/cli/data.py 
source .bashrc
ipm
imp
mkdir .dev
mv doc/dev/* .dev
rm -rf doc/dev/
mkdir -p doc/cannabis_club
mv doc/compliance/ doc/cannabis_club/
mv doc/legal/ doc/cannabis_club/
rm doc/test.md 
rm doc/text.txt 
mv doc docs
mv docs/journal/ docs/cannabis_club/
backup data/impositive/boxes.csv 
13
imp
mv src/cli/data.py tmp/
versionar src/cli/data.py 
rm src/cli/data.py 
mv tmp/data.py src/cli/
versionar doc/prompt/backup.py.md 
versionar doc/prompt/base_de_datos_trece_db.md 
versionar doc/prompt/data_cli_v0.1.1.py.md 
versionar doc/prompt/load_config.md 
versionar doc/prompt/versionado.md 
mv doc/prompt/data_cli.md tmp/
versionar doc/prompt/data_cli.md 
rm doc/prompt/data_cli.md 
mv tmp/data_cli.md doc/prompt/
imp
mv doc/gestion_conjunta/ doc/control_general/
backup src/cli/data.py 
versionar src/core/load_config.py 
versionar src/core/version.py 
imp
imp
imp
imp
versionar data/impositive/boxes.csv 
backup data/impositive/concepts.csv 
backup data/impositive/entities_types.csv 
backup data/impositive/entities.csv 
backup data/impositive/expenses.csv 
backup data/impositive/genetics.csv 
backup data/impositive/harvest_detail.csv 
backup data/impositive/harvest.csv 
backup data/impositive/modules.csv 
backup data/impositive/paymethods.csv 
backup data/impositive/prices.csv 
backup data/impositive/withdrawals.csv 
mkdir -p doc/prompt/data_cli
mv doc/prompt/data_cli.md doc/prompt/data_cli/
mkdir -p doc/prompt/backup headers_trece_db load_config versionado
rm -rf doc/prompt/backup
mkdir -p doc/prompt/{backup,headers_trece_db,load_config,versionado}
versionar doc/prompt/backup/backup.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/headers_trece_db/headers_trece_db.md 
versionar doc/prompt/load_config/load_config.md 
versionar doc/prompt/versionado/versionado.md 
versionar doc/prompt/data_cli/data_cli.md 
restore src/cli/data.py 
imp
mkdir data/impositive/movements
mv data/impositive/withdrawals.csv data/impositive/movements/
imp
help
clear
imp
imp
13
13
13
13
13
imp
imp
tmux
tmux
imp
13
tree -L 2
13
imp
mkdir -p data/impositive/settings
imp
versionar src/cli/data.py 
mkdir -p src/cli/impositive
cp src/cli/data.py src/cli/impositive/main.py
source .bashrc
imp
13
cd data
tree -l
mkdir impositive/harvest
mv impositive/harvest.csv impositive/harvest
tree -l
mv impositive/harvest_detail.csv impositive/harvest
tree -l
mkdir -p shed
tree -l
mv impositive/paymethods.csv impositive/settings/
tree -l
mdkir -p management
mkdir management
tree -l
mv impositive/ management/
tree -l
mv shed/ management/
tree -l
mv management/impositive/modules.csv management/shed/
tree -l
mv management/impositive/harvest/ management/shed/
tree -l
mv management/impositive/settings/ management/
tree -l
mkdir -p management/shed/genetics && mv management/impositive/genetics.csv management/shed/genetics/ 
tree -l
mkdir -p management/people
tree -l
mv management/impositive/entities.csv management/people/
tree -l
mkdir -p management/impositive/boxes
mv management/impositive/boxes.csv management/impositive/boxes
tree -l
mkdir -p management/shed/modules
mv management/shed/modules.csv management/shed/modules
tree -l
imp
imp
imp
tree -l
cd ..
tree -L 1
rm -rf load_config/
imp
mkdir -p data/bitacoras
mkdir -p templates/prompt/
nano templates/prompt/prompt.md
mkdir -p templates/metadatos
mkdir -p templates/script
mkdir -p templates/file
ls
mkdir -p doc/prompt/bitacora
cp templates/prompt/prompt.md doc/prompt/bitacora/bitacora.md
imp
versionar src/cli/impositive/data.py 
versionar doc/prompt/data_cli/data_cli.md 
imp
versionar doc/prompt/data_cli/data_cli.md 
mkdir -p doc/respuesta
mkdir -p doc/respuesta/data_cli
imp
imp
versionar src/cli/impositive/data.py 
imp
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/changelog.md 
imp
imp
13
imp
python3 archive/history/trece/src/cli/impositive/data_v0.1.4.py
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
nano config/config.py
rm config/config.py 
cp templates/script/script.py config/config.py
python3
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
mkdir -p .dev/src/{core,util,script,config}
ls .dev/src/
nano .dev/src/config/config.py
mkdir -p .dev/doc
mv .dev/* .dev/doc/
mv .dev/doc/src/ .dev/
nano .dev/.bashrc
nano .dev/requirements.txt
mkdir -p .dev/data/bitacora
mkdir -p .dev/database
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
dev
cd .dev/
tree -l
cd ..
home
13
13
home
backup doc/utils/tmux.md 
versionar doc/utils/tmux.md 
versionar doc/utils/comandos_utiles_sql.md 
deactivate
python3 -m venv ~/trece/.dev/.venv
cd ..
cd ..
nano .bashrc
13
home
deactiva
deactivate
cd ..
home
which python
echo $VIRTUAL_ENV
13
which python
echo $VIRTUAL_ENV
home
cp ../templates/ 
cp ../templates/ .
cp ../templates/ .dev/
mkdir -p doc/prompt/config && cp ../templates/prompt/prompt.md doc/prompt/config.md 
cp ../templates/script/script.py src/config/config.py
mkdir archive/{backup,history}
mkdir -p archive/{backup,history}
mkdir templates
mkdir meta
python3 src/config/config.py 
python3 config.py 
python3 config.py 
python3 config.py 
mkdir logs
python3 config.py 
python3 config.py 
python3 config.py 
python3 config.py 
versionar config.py 
python3
python3 config.py 
mv config.py config/
mv utils/ doc/
mkdir -p templates/script
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
cd data/management/
tree -l
imp
cd ..
cd ..
ls
nano data/impositive/boxes_types.csv
rm data/impositive/boxes_types.csv 
cd ..
nano .bashrc
13
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar src/core/versionado.py 
versionar doc/prompt/prompt_versionado.md 
rm -rf archive/history/doc/
rm archive/history/trece/doc/test_v0.1.0.md 
versionar src/core/backup.py 
versionar src/core/backup.py 
nano templates/metadatos_script.py
versionar src/script/data/balance_mes_actual.py 
rm src/script/data/balance_mes_actual.py 
versionar src/script/data/dashboard_mensual.py && rm src/script/data/dashboard_mensual.py 
versionar src/script/data/gastos_por_entidad_y_concepto.py && rm src/script/data/gastos_por_entidad_y_concepto.py 
versionar src/script/data/sum_expenses.py && rm src/script/data/sum_expenses.py 
versionar src/script/data/stock_actual.py && rm src/script/data/stock_actual.py 
versionar src/script/data/retiros_por_socio.py && rm src/script/data/retiros_por_socio.py 
versionar src/script/data/harvest_stock.py && rm src/script/data/harvest_stock.py 
versionar src/script/data/sum_withdrawals.py && rm src/script/data/sum_withdrawals.py 
rm -rf src/script/data/
rm src/script/import_data.py 
which trece
versionar src/core/data_cli.py 
mkdir -p src/cli
cp src/core/data_cli.py src/cli/data.py
python3 src/cli/data.py 
versionar src/cli/data.py 
nano test.txt
cp src/core/backup.py src/script/backup.py
python3 src/script/backup.py backup test.txt 
rm /home/arca/trece/archive/backup/trece/test.txt.20250821_175503.bak
rm test.txt 
source .bashrc
versionar src/script/backup.py 
mv src/core/versionado.py src/script/versionado.py
source .bashrc
versionar src/script/versionado.py 
mkdir -p src/util
rm -rf src/core/util/
python3 src/cli/data.py 
source .bashrc
ipm
imp
mkdir .dev
mv doc/dev/* .dev
rm -rf doc/dev/
mkdir -p doc/cannabis_club
mv doc/compliance/ doc/cannabis_club/
mv doc/legal/ doc/cannabis_club/
rm doc/test.md 
rm doc/text.txt 
mv doc docs
mv docs/journal/ docs/cannabis_club/
backup data/impositive/boxes.csv 
13
imp
mv src/cli/data.py tmp/
versionar src/cli/data.py 
rm src/cli/data.py 
mv tmp/data.py src/cli/
versionar doc/prompt/backup.py.md 
versionar doc/prompt/base_de_datos_trece_db.md 
versionar doc/prompt/data_cli_v0.1.1.py.md 
versionar doc/prompt/load_config.md 
versionar doc/prompt/versionado.md 
mv doc/prompt/data_cli.md tmp/
versionar doc/prompt/data_cli.md 
rm doc/prompt/data_cli.md 
mv tmp/data_cli.md doc/prompt/
imp
mv doc/gestion_conjunta/ doc/control_general/
backup src/cli/data.py 
versionar src/core/load_config.py 
versionar src/core/version.py 
imp
imp
imp
imp
versionar data/impositive/boxes.csv 
backup data/impositive/concepts.csv 
backup data/impositive/entities_types.csv 
backup data/impositive/entities.csv 
backup data/impositive/expenses.csv 
backup data/impositive/genetics.csv 
backup data/impositive/harvest_detail.csv 
backup data/impositive/harvest.csv 
backup data/impositive/modules.csv 
backup data/impositive/paymethods.csv 
backup data/impositive/prices.csv 
backup data/impositive/withdrawals.csv 
mkdir -p doc/prompt/data_cli
mv doc/prompt/data_cli.md doc/prompt/data_cli/
mkdir -p doc/prompt/backup headers_trece_db load_config versionado
rm -rf doc/prompt/backup
mkdir -p doc/prompt/{backup,headers_trece_db,load_config,versionado}
versionar doc/prompt/backup/backup.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/headers_trece_db/headers_trece_db.md 
versionar doc/prompt/load_config/load_config.md 
versionar doc/prompt/versionado/versionado.md 
versionar doc/prompt/data_cli/data_cli.md 
restore src/cli/data.py 
imp
mkdir data/impositive/movements
mv data/impositive/withdrawals.csv data/impositive/movements/
imp
help
clear
imp
imp
13
13
13
13
13
imp
imp
tmux
tmux
imp
13
tree -L 2
13
imp
mkdir -p data/impositive/settings
imp
versionar src/cli/data.py 
mkdir -p src/cli/impositive
cp src/cli/data.py src/cli/impositive/main.py
source .bashrc
imp
13
cd data
tree -l
mkdir impositive/harvest
mv impositive/harvest.csv impositive/harvest
tree -l
mv impositive/harvest_detail.csv impositive/harvest
tree -l
mkdir -p shed
tree -l
mv impositive/paymethods.csv impositive/settings/
tree -l
mdkir -p management
mkdir management
tree -l
mv impositive/ management/
tree -l
mv shed/ management/
tree -l
mv management/impositive/modules.csv management/shed/
tree -l
mv management/impositive/harvest/ management/shed/
tree -l
mv management/impositive/settings/ management/
tree -l
mkdir -p management/shed/genetics && mv management/impositive/genetics.csv management/shed/genetics/ 
tree -l
mkdir -p management/people
tree -l
mv management/impositive/entities.csv management/people/
tree -l
mkdir -p management/impositive/boxes
mv management/impositive/boxes.csv management/impositive/boxes
tree -l
mkdir -p management/shed/modules
mv management/shed/modules.csv management/shed/modules
tree -l
imp
imp
imp
tree -l
cd ..
tree -L 1
rm -rf load_config/
imp
mkdir -p data/bitacoras
mkdir -p templates/prompt/
nano templates/prompt/prompt.md
mkdir -p templates/metadatos
mkdir -p templates/script
mkdir -p templates/file
ls
mkdir -p doc/prompt/bitacora
cp templates/prompt/prompt.md doc/prompt/bitacora/bitacora.md
imp
versionar src/cli/impositive/data.py 
versionar doc/prompt/data_cli/data_cli.md 
imp
versionar doc/prompt/data_cli/data_cli.md 
mkdir -p doc/respuesta
mkdir -p doc/respuesta/data_cli
imp
imp
versionar src/cli/impositive/data.py 
imp
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/data_cli.md 
versionar doc/prompt/data_cli/changelog.md 
imp
imp
13
imp
python3 archive/history/trece/src/cli/impositive/data_v0.1.4.py
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
nano config/config.py
rm config/config.py 
cp templates/script/script.py config/config.py
python3
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
python3 config/test.py 
mkdir -p .dev/src/{core,util,script,config}
ls .dev/src/
nano .dev/src/config/config.py
mkdir -p .dev/doc
mv .dev/* .dev/doc/
mv .dev/doc/src/ .dev/
nano .dev/.bashrc
nano .dev/requirements.txt
mkdir -p .dev/data/bitacora
mkdir -p .dev/database
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
python3 .dev/src/script/backup.py backup .dev/src/script/backup.py 
dev
cd .dev/
tree -l
cd ..
home
13
13
home
backup doc/utils/tmux.md 
versionar doc/utils/tmux.md 
versionar doc/utils/comandos_utiles_sql.md 
deactivate
python3 -m venv ~/trece/.dev/.venv
cd ..
cd ..
nano .bashrc
13
home
deactiva
deactivate
cd ..
home
which python
echo $VIRTUAL_ENV
13
which python
echo $VIRTUAL_ENV
home
cp ../templates/ 
cp ../templates/ .
cp ../templates/ .dev/
mkdir -p doc/prompt/config && cp ../templates/prompt/prompt.md doc/prompt/config.md 
cp ../templates/script/script.py src/config/config.py
mkdir archive/{backup,history}
mkdir -p archive/{backup,history}
mkdir templates
mkdir meta
python3 src/config/config.py 
python3 config.py 
python3 config.py 
python3 config.py 
mkdir logs
python3 config.py 
python3 config.py 
python3 config.py 
python3 config.py 
versionar config.py 
python3
python3 config.py 
mv config.py config/
mv utils/ doc/
mkdir -p templates/script
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
cd data/management/
tree -l
imp
cd ..
cd ..
ls
home
home
source .bashrc
home
nano ../../.bashrc
imp
python3 ../archive/history/trece/src/cli/impositive/data_v0.1.3.py 
python3 ../archive/history/trece/src/cli/impositive/data_v0.1.2.py 
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
python3 ~/trece/.dev/src/script/backup/backup.py backup .dev/src/script/backup/backup.py 
home
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
python3 src/backup/backup.py backup src/backup/backup.py 
python3 src/backup/backup.py backup src/backup/backup.py 
python3 src/script/backup/backup.py backup src/script/backup/backup.py 
home
cd ..
nano .bashrc
home
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
home
PYTHONPATH
python3 -c "import sys; print('\n'.join(sys.path))"
13
python3 -c "import sys; print('\n'.join(sys.path))"
home
python3 -c "import sys; print('\n'.join(sys.path))"
echo $PYTHONPATH
echo $PYTHONPATH
13
echo $PYTHONPATH
home
cli_versionar src/core/script/bitacora.py 
13
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
imp
imp
13
imp
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
python3 archive/history/trece/src/cli/impositive/data_v0.1.3.py 
find ~/trece -type d -name "__pycache__" -exec rm -rf {} +
home
mkdir -p src/cli
python3 src/cli/backup_cli.py backup src/cli/backup_cli.py 
13
ls
mkdir -p src/trece && mkdir -p src/dev
cd .dev/src/
tree -l
cd ../../
tree -l src/
cd src/
mv script/ core/
tree -l
mv util/ core/
tree -l
cd ..
mkdir -p data/trece && mkdir -p data/dev
mv data/management/ data/trece/
tree -l data
mkdir -p doc/dev
mv doc/prompt/ doc/dev/
13
mkdir -p doc/trece
13
backup doc/dev/prompt/backup/backup.md 
source .bashrc
source .bashrc
backup doc/dev/prompt/backup/backup.md 
archive
source .bashrc
source .bashrc
source .bashrc
source .bashrc
source .bashrc
source .bashrc
cd ..
13
source .bashrc
bash -x ~/.bashrc
source .bashrc
source .bashrc
source .bashrc
source .bashrc
source .bashrc
restore .bashrc 
source .bashrc
source .bashrc
cd ..
nano .bashrc
