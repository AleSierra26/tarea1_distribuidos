# Citas e IA

> Para las distintas consultas ayudadas por IA, usamos la herramienta de ChatGPT. Este documento registra las distintas fuentes usadas, las consultas realizadas a ChatGPT y sus respuestas.

---

## Citas

### Cita 1

Para la conexión y creacion de serrvidores en base a instancias (clases), use parte del codgigo proporcionado en la clase 3 de este curso

## Uso de IA

### Interacción 1

Para aprender/recordar como hacer uso de threading.lock en python y poder aplicarlo en las distintos metodos del codigo que requerian uso de threads.

**Prompt:**

> ¿Como funciona el uso de threading.lock en python para el uso en objetos y en sus metodos?

**Respuesta:**

# Uso de `threading.Lock` en métodos de objetos (Python)

## 🧠 Concepto clave

Cada objeto puede tener su propio `lock`, y sus métodos lo usan para asegurar acceso exclusivo.

👉 Es decir: el lock **vive dentro del objeto (`self.lock`)**.

---

## ✅ Ejemplo típico

```python
import threading

class Contador:
    def __init__(self):
        self.valor = 0
        self.lock = threading.Lock()  # 🔒 lock del objeto

    def incrementar(self):
        with self.lock:
            self.valor += 1

    def obtener(self):
        with self.lock:
            return self.valor
```

## 🔍 ¿Qué está pasando?

- `self.lock` protege `self.valor`

- Si varios threads llaman `incrementar()`:
  - solo uno entra a la vez

- Evitas inconsistencias

## ⚠️ ¿Por qué también bloquear en getters?

Puede parecer innecesario, pero:

- otro thread podría estar modificando al mismo tiempo
- podrías leer un estado inconsistente

## 🧩 Ejemplo con múltiples threads

```python
import threading

contador = Contador()

def tarea():
    for _ in range(100000):
        contador.incrementar()

threads = [threading.Thread(target=tarea) for _ in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(contador.obtener())
```

## 🧠 Buenas prácticas

1. 🔒 Un lock por recurso crítico

- No bloquees todo el objeto si no es necesario.

```python
self.lock_dinero = threading.Lock()
self.lock_historial = threading.Lock()
```

2. ⚠️ Evita deadlocks entre métodos

- Si un método llama a otro que también usa el mismo lock:

```python
def metodo_a(self):
    with self.lock:
        self.metodo_b()

def metodo_b(self):
    with self.lock:  # ⚠️ problema aquí
        ...
```

- 👉 Esto puede romperse porque Lock no es reentrante.

- ✅ Solución: usar threading.RLock()

## 🔁 Lock vs RLock

- Lock → no permite que el mismo thread lo tome 2 veces
- RLock → sí permite (reentrante)

```python
self.lock = threading.RLock()
```

## 🧠 Resumen claro

- El lock se guarda en self
- Se usa en métodos que acceden/modifican atributos compartidos
- Protege la consistencia del objeto
- Usa with self.lock: siempre que puedas

Si quieres, puedo ver tu código (como ese del RPC que estás haciendo) y decirte exactamente dónde deberías poner locks 👀
