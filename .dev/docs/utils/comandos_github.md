Te lo explico paso a paso, como flujo básico de trabajo diario en Git:

---

## 1️⃣ Revisar cambios

Antes de hacer un commit, siempre revisá qué archivos cambiaste:

```bash
git status
```

* Te va a mostrar archivos **modificados**, **nuevos** o **borrados**.
* Esto te ayuda a asegurarte de que solo subís lo que querés.

---

## 2️⃣ Agregar archivos al área de staging

Git no guarda automáticamente todos los cambios; primero hay que decirle **qué cambios querés incluir en el commit**:

```bash
git add archivo1 archivo2
```

* Para agregar **todos los cambios** en el proyecto:

```bash
git add .
```

> El `.` significa “todos los archivos modificados y nuevos”.

---

## 3️⃣ Hacer el commit

Cada commit debería tener un mensaje **claro y descriptivo** sobre qué cambiaste:

```bash
git commit -m "Descripción corta de lo que hiciste"
```

Ejemplo:

```bash
git commit -m "Agrego módulo de conexión a la base de datos"
```

---

## 4️⃣ Subir los cambios al repositorio remoto (GitHub)

```bash
git push origin main
```

* La primera vez que hacés push con una nueva rama, agregá `-u` para que quede trackeada:

```bash
git push -u origin main
```

* Después, solo `git push` alcanza.

---

## 5️⃣ Flujo recomendado diario

1. `git pull` → Traé cambios del repositorio remoto (si alguien más trabajó antes que vos).
2. Trabajá en tu código o archivos.
3. `git status` → Revisá cambios.
4. `git add .` → Prepará los cambios para commit.
5. `git commit -m "Mensaje claro"` → Guardá los cambios localmente.
6. `git push` → Subí los cambios a GitHub.

---

💡 **Consejos útiles**:

* Hacé commits **pequeños y frecuentes**, no esperar hasta tener todo terminado.
* Usá mensajes **claros y cortos**, ejemplo:

  * “Agrego función de login”
  * “Corrijo bug en módulo de exportación”
  * “Actualizo documentación de proyecto”

---

Si querés, te puedo armar un **mini “script de Git diario”** que haga `status → add → commit → push` en un solo comando, para no estar tipeando todo cada vez.

¿Querés que haga eso?
