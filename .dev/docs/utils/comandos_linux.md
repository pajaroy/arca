Claro. Te paso un **resumen de comandos básicos de Linux** que te van a servir para moverte y trabajar en la terminal, explicado como para alguien que recién empieza:

---

## 1. Navegación de carpetas

```bash
pwd              # Muestra en qué carpeta estás (print working directory)
ls               # Lista los archivos y carpetas en la carpeta actual
ls -l            # Lista con detalles (permisos, tamaño, fecha)
ls -a            # Lista incluyendo archivos ocultos
cd nombre_carpeta  # Entrar en una carpeta
cd ..            # Subir un nivel en la carpeta
cd ~             # Ir al directorio home
```

---

## 2. Crear, mover y eliminar archivos o carpetas

```bash
mkdir nombre_carpeta       # Crear una carpeta
touch archivo.txt          # Crear un archivo vacío
cp archivo.txt copia.txt   # Copiar un archivo
mv archivo.txt nueva_carpeta/  # Mover archivo a otra carpeta
mv archivo.txt renombrado.txt  # Renombrar un archivo
rm archivo.txt             # Borrar un archivo
rm -r carpeta              # Borrar una carpeta y todo su contenido
```

> ⚠️ `rm -r` es peligroso, revisá dos veces antes de usarlo.

---

## 3. Ver contenido de archivos

```bash
cat archivo.txt      # Mostrar todo el contenido del archivo
less archivo.txt     # Ver el archivo página por página
head archivo.txt     # Ver las primeras líneas
tail archivo.txt     # Ver las últimas líneas
tail -f archivo.log  # Ver un archivo log en tiempo real
```

---

## 4. Buscar archivos o contenido

```bash
find . -name "archivo.txt"    # Buscar un archivo por nombre en la carpeta actual y subcarpetas
grep "palabra" archivo.txt    # Buscar una palabra dentro de un archivo
grep -r "palabra" .           # Buscar recursivamente en todas las carpetas
```

---

## 5. Información del sistema

```bash
whoami          # Saber con qué usuario estás
df -h           # Ver espacio disponible en disco
du -h carpeta/  # Ver tamaño de una carpeta
free -h         # Ver memoria disponible
uname -a        # Información del sistema
```

---

## 6. Permisos y propietario de archivos

```bash
chmod 755 archivo.sh  # Cambiar permisos (ej. lectura/escritura/ejecución)
chown usuario:grupo archivo.txt  # Cambiar propietario
```

---

## 7. Ejecutar programas y scripts

```bash
./script.sh        # Ejecutar un script en la carpeta actual
bash script.sh     # Ejecutar un script con bash
python3 script.py  # Ejecutar un script Python
```

---

## 8. Comandos útiles extras

```bash
history         # Ver el historial de comandos
clear           # Limpiar la pantalla
man comando     # Mostrar manual de un comando (ej. man ls)
```

---

