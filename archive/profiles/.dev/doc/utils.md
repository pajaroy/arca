# Comandos basicos de terminal

## Clear __pycache__

```bash
find ~/trece/.dev -type d -name "__pycache__" -exec rm -rf {} +
```

---

## Borrar carpetas vacias

```bash
find ~/trece/.dev -type d -empty -delete
```

---

## Atajos de `tmux`

👉 **Prefijo por defecto:** `Ctrl-b` (primero presionás eso, después la tecla siguiente).

* **Dividir ventana verticalmente**: `Ctrl-b` `%`

* **Dividir ventana horizontalmente**: `Ctrl-b` `"`

* **Cambiar entre paneles**: `Ctrl-b` y luego flechas (`←↑↓→`)

* **Cerrar un panel**: `Ctrl-d` (o `exit` dentro del shell del panel)

---

# Sql

## Connect db

```bash
sqlite3 database/13cc.db
```
## **Ver datos en formato tabla** (para cada tabla):
```sql
-- Configurar formato (ejecutar solo una vez)
    .mode box
    .headers on

-- Ver tablas una por una:
SELECT * FROM genetics LIMIT 5;
SELECT * FROM harvest LIMIT 5;
SELECT * FROM harvest_detail LIMIT 5;
SELECT * FROM withdrawals LIMIT 5;
```

---