# 📓 Bitácora diaria – 2025-06-01

## 🧠 Día de Reinicio Total y Consolidación de Núcleo

---

### 💻 1. Formateo y reinstalación de sistemas
- Se **formatearon ambas máquinas**:
  - 🖥️ **ALMA_CORE** (PC de escritorio): se instaló Parrot OS como sistema principal.
  - 💻 **ALMA_RESIST** (Notebook): se instaló Parrot OS limpio, operando como nodo espejo.

- Se definió **la arquitectura de operación**:
  - `alma-core` = nodo maestro y núcleo del sistema.
  - `alma-resist` = nodo secundario portátil, con funciones espejo y tareas remotas.

---

### 🔁 2. Sincronización y control remoto por SSH

- Se configuró **acceso SSH sin contraseña entre ambos nodos**:
  - Generación de claves `ed25519`.
  - Alias rápidos `core` y `resist` agregados a `~/.bashrc`.
  - Validación de acceso remoto funcional desde ambos extremos.

- Confirmado control terminal **completo entre nodos**:
  - Desde `alma-core` se puede manejar `alma-resist` (y viceversa) sin necesidad de password.

---

### 🖱️ 3. Instalación de Input Leap

- Se instaló y compiló `input-leap` en ambas máquinas desde fuente.
- Se configuró el archivo `input-leap.conf` con los siguientes vínculos:

  ```conf
  section: screens
      alma-core:
      alma-resist:
  end

  section: links
      alma-core:
          left = alma-resist
      alma-resist:
          right = alma-core
  end

    Confirmado el uso compartido de mouse y teclado entre ambas PCs.

    Funciona incluso en CLI. Operación coordinada y sin errores.

🗃️ 4. Organización del sistema

    Se estableció /home/bird/ALMA_RESIST/ como raíz del entorno de trabajo replicado.

    Se creó .rsync_exclude para excluir archivos innecesarios en sincronizaciones.

    Se dejó preparado el script alma_autostart_tmux.sh para automatizar todo al iniciar.

✅ Conclusión del día

Sistema completamente limpio, sincronizado y funcional.
Ambos nodos se comunican, comparten periféricos y pueden ejecutar tareas cruzadas.
La infraestructura mínima para comenzar a trabajar con ALMA_RESIST como entorno modular portátil ya está operativa.
