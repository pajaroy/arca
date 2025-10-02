---
uuid: ""
tipo: doc
formato: ""
nombre: ml_basics_bird
version: 0.1.0
estado: activo
fecha_creacion: ""
fecha_modificacion: ""
autor: Bird
descripcion: Conceptos basicos de ML para aplicar
hash_integridad: ""
---
# ✅ Machine Learning - Conceptos Básicos

## 🚀 Qué es Machine Learning

**Machine Learning (ML)** es un conjunto de técnicas matemáticas y estadísticas que permiten que las computadoras aprendan patrones a partir de datos, **sin que alguien las programe explícitamente para cada resultado.**

En vez de programar reglas fijas, entrenás un modelo con ejemplos y ese modelo **predice** o **clasifica** cosas nuevas.

---

## Índice

[[##  Conceptos Fundamentales]]
[[### 1. Datos (Data)]]
[[### 2. Modelo]]
[[### 3. Entrenamiento (Training)]]
[[### 4. Predicción (Prediction)]]
[[### 5. Overfitting / Underfitting]]
[[### 6. Dataset Split]]
[[### 7. Tipos de ML]]
[[## 🧩 ML en sistemas reales]]
[[#🎯 Conceptos a Aprender Primero]]


##  Conceptos Fundamentales

### 1. Datos (Data)

- **Features (X):** variables de entrada (edad, tamaño, temperatura…)
- **Target (y):** lo que querés predecir (precio, categoría, probabilidad…)

Ejemplo:

| tamaño | temperatura | rendimiento |
|--------|-------------|-------------|
| 10     | 20°C        | 15 kg       |
| 12     | 25°C        | 18 kg       |

- Features → tamaño, temperatura
- Target → rendimiento

---

### 2. Modelo

- Función matemática que **relaciona X con y.**
- Se entrena con datos conocidos → después predice para datos nuevos.

Ejemplo:
> rendimiento = a * tamaño + b * temperatura + c

---

### 3. Entrenamiento (Training)

- Proceso de “ajustar” el modelo para que **se aproxime bien a los datos.**
- Se usa el método `.fit(X, y)` en casi todas las librerías de ML.

Ejemplo en scikit-learn:

```python
from sklearn.linear_model import LinearRegression

modelo = LinearRegression()
modelo.fit(X, y)
```

---

### 4. Predicción (Prediction)

 - Una vez entrenado, el modelo puede predecir valores de y para datos nuevos.
  
```python
modelo.predict([[14, 22]])
```

---

### 5. Overfitting / Underfitting

 - Overfitting: el modelo memoriza datos de entrenamiento → mal resultado en datos nuevos.

 - Underfitting: el modelo es demasiado simple → no aprende nada útil.

Objetivo: equilibrio.

---

### 6. Dataset Split

Para evitar engañarte con resultados, siempre se separa el dataset:

 - Train Set: para entrenar.

 - Test Set: para medir si aprendió bien.

Ejemplo:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

--- 

### 7. Tipos de ML

✅ Supervised Learning (Aprendizaje supervisado)

 - Tenés datos etiquetados (X y y).

 - Ej.: predicción de precios, clasificación de imágenes.

✅ Unsupervised Learning (Aprendizaje no supervisado)

 - No tenés y.

 - Buscás patrones, agrupamientos (clusters).

 - Ej.: segmentar clientes, detectar anomalías.

✅ Reinforcement Learning (Aprendizaje por refuerzo)

 - El modelo aprende mediante “premios” y “castigos”.

 - Ej.: robots, juegos.

---

## 🧩 ML en sistemas reales

En un sistema como el tuyo:

 - Primero armás arquitectura (config, logs, índices).

 - Después, juntás datos relevantes.

 - Luego, entrenás modelos para:

     - Predecir qué archivos crear.

     - Detectar anomalías.

     - Automatizar decisiones.

---

## 🎯 Conceptos a Aprender Primero

✅ Qué son Features y Target
✅ Qué es entrenar un modelo (fit)
✅ Qué es predecir (predict)
✅ Qué es Overfitting
✅ Qué es un Dataset Split
✅ Tipos de problemas (Regresión, Clasificación, Clustering)
✅ Guardar modelos entrenados (.pkl, .joblib)
📚 Bibliotecas Útiles

 - scikit-learn → ML clásico y simple.

 - pandas → manipular datasets.

 - numpy → cálculos numéricos.

 - joblib o pickle → guardar modelos entrenados.

👌 Keep it simple

→ No metas ML en cada paso.
→ Empezá entrenando algo muy básico.
→ Agregá complejidad solo si hace falta.

---

[[#✅ Machine Learning - Conceptos Básicos]]

Fin del resulado basico.

---