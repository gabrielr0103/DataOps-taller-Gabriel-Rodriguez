# DataOps-taller-Gabriel-Rodriguez

## Pipeline de Datos para Tienda en Línea

## Descripción del proyecto
Repositorio del taller práctico de DataOps. Implementar un pipeline de datos que extrae,
transforma y entrena un modelo de predicción de ventas para una tienda en línea, con
control de versiones, pruebas automatizadas y CI/CD.

## Instrucciones de instalación
1. Clonar el repositorio:
   `git clone https://github.com/<tu-usuario>/dataops-taller-gabriel-rodriguez.git`
2. Entrar a la carpeta: `cd dataops-taller-gabriel-rodriguez`
3. Crear entorno virtual: `python -m venv venv`
4. Activar entorno: `source venv/bin/activate` (Mac/Linux)
5. Instalar dependencias: `pip install -r requirements.txt`
6. Generar la base de datos de prueba: `python3 scripts/create_db.py`

## Estructura del repositorio
```bash
dataops-taller-gabriel-rodriguez/
│
├── .dvc/
│   └── config
├── .dvcignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── .gitkeep
│   └── ventas.db.dvc
├── migrations/
│   ├── V001_create_ventas_table.sql
│   ├── V002_add_index_on_fecha.sql
│   └── V003_add_column_descuento.sql
├── notebooks/
│   └── exploracion.ipynb
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── train.py
│   └── utils.py
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   ├── test_train.py
│   ├── test_data_quality.py
│   └── test_integration.py
├── scripts/
│   ├── create_db.py
│   └── create_snapshot.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Comandos básicos de Git utilizados

Durante el desarrollo del proyecto se utilizaron los siguientes comandos:

#### Crear la rama de trabajo
git checkout -b feature/pipeline-inicial

#### Preparar los cambios
git add <archivo>

#### Confirmar los cambios
git commit -m "mensaje"

#### Subir la rama al repositorio remoto
git push -u origin feature/pipeline-inicial

### Descripción

* `git checkout -b feature/pipeline-inicial`: crea la rama de trabajo.
* `git add <archivo>`: prepara los cambios para el commit.
* `git commit -m "mensaje"`: confirma los cambios realizados.
* `git push -u origin feature/pipeline-inicial`: sube la rama al repositorio remoto.

## Uso del pipeline
El pipeline se ejecuta encadenando los módulos de `src/`:
1. `extract_data(db_path)` — lee la tabla ventas de la base de datos.
2. `clean_data(df)` — elimina duplicados, rellena nulos y convierte tipos.
3. `calculate_metrics(df)` — calcula venta_total y mes.
4. `aggregate_sales(df)` — agrupa ventas por categoría y mes.
5. `train_model(df)` — entrena una regresión lineal y guarda el modelo.
6. `save_to_csv(df, path)` — exporta el resultado agregado a CSV.

Los archivos generados (`data/ventas.db`, `data/aggregated_sales.csv`,
`models/model.pkl`) no se versionan en Git: se generan localmente al
ejecutar el pipeline.

## Pruebas
El proyecto cuenta con tres niveles de pruebas automatizadas, ubicadas en tests:

- **Unitarias** (test_transform.py): validan la lógica de limpieza y
  cálculo de métricas de forma aislada, con datos de ejemplo controlados.
- **Calidad de datos** (test_data_quality.py): validan el esquema y las
  reglas de negocio sobre los datos crudos de ventas.db (columnas
  esperadas, valores no negativos, sin fechas futuras).
- **Integración** (test_integration.py): ejecuta el pipeline completo
  (extraer → transformar → agregar) y valida el resultado final.

Para ejecutarlas:
```bash
python3 scripts/create_db.py   # si aún no existe la base de datos
pytest -v
```

## CI/CD
El proyecto usa **GitHub Actions** (`.github/workflows/ci.yml`) para automatizar
la validación de cada cambio. El pipeline se dispara con cada `push` a `main` o
a cualquier rama `feature/*`, y con cada Pull Request hacia `main`.

Pasos del job `build-and-test`:
1. Checkout del código.
2. Configuración de Python 3.9.
3. Instalación de dependencias (`requirements.txt`).
4. Creación de la base de datos de prueba.
5. Análisis estático: `pylint` (calidad), `black --check` (formato), `bandit` (seguridad).
6. Pruebas unitarias con cobertura (`pytest --cov=src`).
7. Pruebas de calidad de datos.
8. Entrenamiento del modelo (`python -m src.train`).
9. Publicación del modelo entrenado como artefacto descargable de la ejecución.


## Versionamiento de datos y esquemas

- **Datos** (DVC): `data/ventas.db` se trackea con DVC
  en vez de Git directamente, Git guarda solo el puntero `ventas.db.dvc`
  (con el hash del contenido), mientras el archivo real se sincroniza a
  un remoto configurado con `dvc push` / `dvc pull`. En este proyecto el
  remoto es una carpeta local (`/tmp/dvcstore`), solo para fines
  demostrativos del taller en un entorno real sería almacenamiento en
  la nube (S3, GCS, Azure Blob, etc.).
- **Esquema** (`migrations/`): cambios estructurales a la tabla `ventas`
  se documentan como scripts SQL secuenciales y numerados
  (`V001`, `V002`, `V003`), aplicables con `sqlite3 data/ventas.db < migrations/<archivo>.sql`.
  En un pipeline de CI/CD real, estas migraciones se aplicarían
  automáticamente con una herramienta como Flyway antes de correr las
  pruebas.
- **Snapshots** (`scripts/create_snapshot.py`): genera copias fechadas
  de la base de datos en `data/snapshots/ventas_YYYYMMDD.db`, útiles
  como respaldo puntual independiente del versionamiento continuo de DVC.


## Diagrama de flujo del pipeline

## Diagrama de flujo del pipeline
```bash
Base de datos (data/ventas.db)
        │
        ▼
  extract_data()      ->  DataFrame crudo
        │
        ▼
  clean_data()         ->  sin duplicados, sin nulos, fecha en datetime
        │
        ▼
  calculate_metrics()  ->  + venta_total, + mes
        │
        ▼
  aggregate_sales()    ->  ventas agrupadas por categoria y mes
        │
        ├───────────────────────────────┐
        │                                │
        ▼                                ▼
  train_model()                   save_to_csv()
  -> models/model.pkl             -> data/aggregated_sales.csv
```

## Resultados de las pruebas

Estas dos capturas muestran el estado final de las pruebas automatizadas:
la ejecución completa de la suite con pytest, y la ejecución exitosa del
pipeline de CI/CD en GitHub Actions.

<!-- Captura: resultado de pytest -v -->
![Resultado de pytest -v](docs/screenshots/tarea%203%20test%20entregable.png)

<!-- Captura: ejecución exitosa del pipeline en GitHub Actions -->
![Ejecución exitosa del pipeline en GitHub Actions](docs/screenshots/Tarea%204%20ENTREGABLE%20CI.png)

## Informe Final

### Introducción

Este taller buscaba cerrar la brecha entre construir un modelo y ponerlo
a funcionar de forma continua y confiable, que es la pregunta con la que
arrancó la parte teórica. El objetivo de la parte práctica era aplicar
eso a escala pequeña pero real: montar un pipeline de datos completo
para una tienda en línea, desde la extracción hasta el entrenamiento de
un modelo, con control de versiones, pruebas automatizadas, integración
continua y versionamiento de datos. La idea no era que cada pieza
funcionara aislada, sino que el conjunto se comportara como un sistema
reproducible: que otra persona, o el propio GitHub Actions, pudiera
clonar el repositorio y correr el pipeline completo sin depender de
configuraciones manuales.

### Desarrollo

**Tarea 1.** El punto de partida fue crear el repositorio en GitHub con
la estructura de carpetas que pedía el taller (`src/`, `tests/`,
`scripts/`, `notebooks/`, `.github/workflows/`) y una rama de trabajo,
`feature/pipeline-inicial`, separada de `main`. Cada archivo se
confirmó con un commit atómico y un mensaje siguiendo la convención
`tipo: descripción` (`feat:`, `test:`, `chore:`), la misma que pide el
enunciado del taller. En el proceso apareció un error de tipeo en el
nombre de una carpeta (`workfollow` en vez de `workflows`), que hubo
que corregir antes de seguir, porque GitHub Actions busca los workflows
exactamente en esa ruta.

<!-- Captura: estructura de carpetas del repositorio (Tarea 1) -->
![Estructura de carpetas](docs/screenshots/Tarea%201%20ENDO%20entregable%201.png)

<!-- Captura: historial de commits (Tarea 1), parte 1 -->
![Historial de commits (parte 1)](docs/screenshots/Tarea%201%20ENDO%20historial%201.png)

<!-- Captura: historial de commits (Tarea 1), parte 2 -->
![Historial de commits (parte 2)](docs/screenshots/Tarea%201%20ENDO%20hitorial%202.png)

**Tarea 2.** Con la estructura lista, se implementaron los módulos del
pipeline: `extract.py` lee la base de datos SQLite y la convierte en un
DataFrame, `transform.py` limpia los datos y calcula las métricas de
venta, `train.py` entrena una regresión lineal, `utils.py` guarda los
resultados en CSV. El script `create_db.py` genera datos simulados con
algunos valores nulos y registros duplicados a propósito, para que las
pruebas de calidad de la Tarea 3 tuvieran algo real que detectar. La
limpieza de duplicados en `clean_data` compara todas las columnas
excepto el `id`, porque dos ventas iguales en fecha, producto, cantidad
y cliente casi siempre son el mismo evento registrado dos veces por
error, aunque el sistema les haya asignado ids distintos. Los nulos en
`cantidad` se rellenan con 0, una decisión conservadora para no inflar
las ventas, y los de `precio_unitario` con la media de la columna,
porque un precio en 0 rompería el cálculo de `venta_total`. En este
punto apareció el primer problema real de reproducibilidad del taller:
un `requirements.txt` que había quedado con texto suelto en vez de la
lista de dependencias, y que hizo fallar la instalación completa antes
de correr una sola línea de código propio.

**Tarea 3.** Las pruebas se dividieron en los tres niveles que pide la
teoría: unitarias (`test_transform.py`), que usan un DataFrame armado a
mano y corren en una fracción de segundo porque no tocan disco; de
calidad de datos (`test_data_quality.py`), que sí leen la base de datos
real y validan reglas como que no haya cantidades negativas o fechas
futuras; y de integración (`test_integration.py`), que corre el
pipeline completo de punta a punta. Al ejecutar pytest por primera vez
apareció un `ModuleNotFoundError: No module named 'src'`, porque pytest
no agregaba la raíz del proyecto a la ruta de búsqueda de Python. Se
resolvió agregando `pythonpath = .` a `pytest.ini` (captura en la
sección de Resultados de las pruebas, arriba).

**Tarea 4.** El pipeline de CI/CD se armó en `.github/workflows/ci.yml`,
siguiendo la estructura del taller pero con tres ajustes necesarios
para que funcionara de verdad: `actions/upload-artifact@v3` ya no
existe (GitHub la dio de baja el 30 de enero de 2025), así que se
cambió a `v4`; se agregó `pytest-cov` a `requirements.txt`, que faltaba
para el flag `--cov=src`; y se le agregó una función `main()` a
`train.py`, porque tal como estaba escrito solo definía la función de
entrenamiento sin ejecutarla, así que el paso de subir el modelo como
artefacto habría fallado por no encontrar el archivo. El mismo
`ModuleNotFoundError` de la Tarea 3 volvió a aparecer, esta vez en el
propio pipeline, y se resolvió de la misma forma: cambiando
`python src/train.py` por `python -m src.train`. Las primeras
ejecuciones en Actions fallaron mientras se corregían estos detalles,
hasta llegar a una ejecución completa en verde (captura arriba, en
Resultados de las pruebas).

**Tarea 5.** La última pieza fue el versionamiento de datos y esquema.
La base de datos se trackea con DVC en vez de Git directamente: Git
guarda solo un archivo puntero (`ventas.db.dvc`) con el hash del
contenido, y el archivo real se sincroniza aparte con un remoto (una
carpeta local, `/tmp/dvcstore`, solo para efectos del taller). Los
cambios de esquema se documentaron como tres migraciones SQL numeradas
(`V001` a `V003`) en vez de alterar la tabla directamente, y se agregó
un script para generar snapshots fechados de la base de datos como
respaldo independiente. Instalar DVC reveló un problema de entorno que
no tenía nada que ver con DVC en sí: `pip install dvc` se quedaba
colgado tratando de compilar una de sus dependencias (`cryptography`)
desde código fuente, porque no existía una versión precompilada para
Python 3.14 en un Mac con procesador Intel. La solución fue instalar
Python 3.12 en paralelo y recrear el entorno virtual del proyecto con
esa versión. Después, `dvc push` mostraba "Everything is up to date"
sin haber subido nada la primera vez, porque no detectaba el archivo
`ventas.db.dvc` hasta que ese archivo quedó confirmado en Git: DVC
depende de Git para saber qué archivos le pertenecen al proyecto, no
solo de que existan en el disco.

### Análisis

¿Qué diferencias encontró entre CI/CD tradicional y CI/CD para datos?
En CI/CD tradicional, un build casi siempre es determinista: el mismo
código produce el mismo resultado. Acá no: `create_db.py` genera datos
distintos cada vez que corre, porque usa números aleatorios, así que
hubo que hacerlo idempotente en otro sentido, borrando la base de datos
antes de recrearla para que el resultado sea estructuralmente el mismo
aunque los valores cambien. También las pruebas son distintas: además
de las unitarias sobre funciones, hay pruebas de calidad de datos que
no existen en un pipeline de software normal, y que validan el
contenido, no el comportamiento del código. Y el artefacto final no es
un ejecutable, es un archivo `.pkl` con un modelo entrenado, que el
propio CI sube como artefacto descargable de la ejecución.

¿Qué desafíos específicos enfrentó al versionar datos? El más concreto
fue que Git no está pensado para esto: un archivo `.db` binario no
tiene una estructura de líneas comparable, así que cada cambio
duplicaría el archivo completo en el historial en vez de guardar solo
la diferencia. DVC resuelve esto separando el puntero, liviano, que va
en Git, del contenido real, pesado, que va a un remoto aparte. El otro
desafío fue de expectativas: asumí que `dvc push` se iba a comportar
como cualquier comando que sube archivos, sin darme cuenta de que
primero necesita que el archivo puntero esté confirmado en Git. No es
un error de la herramienta, es el diseño: DVC no es independiente de
Git, es una capa que se apoya en él.

¿Cómo aseguró la reproducibilidad del experimento? No depende de un
solo mecanismo sino de varios trabajando juntos: `requirements.txt`
fija las dependencias exactas de Python, `create_db.py` es idempotente
en su estructura aunque no en sus valores, el `.gitignore` separa con
claridad qué es código versionado y qué es artefacto que se regenera
solo, y DVC versiona el dato real por fuera de Git sin perder la
trazabilidad de qué versión corresponde a qué commit. Ninguna de esas
piezas por sí sola garantiza nada; la reproducibilidad salió de que
todas apuntan en la misma dirección.

### Conclusiones

El pipeline terminó siendo pequeño, pero tocó casi todos los problemas
que menciona la parte teórica del taller, a escala real: el
`requirements.txt` vacío es un ejemplo literal del problema de "en mi
máquina sí funciona"; el error de importación repetido en pytest y en
el CI muestra que un mismo problema de configuración puede aparecer en
más de un lugar si no se resuelve de raíz; y el pipeline de CI/CD no
pasó en verde al primer intento, lo cual es normal, no un fracaso.

La limitación más clara de este enfoque es que casi todo es local y de
juguete: el remoto de DVC es una carpeta temporal del propio
computador, la base de datos es SQLite con datos simulados, y el
modelo es una regresión lineal simple sobre pocos meses de datos
agregados. Ninguna de esas decisiones sería aceptable en un proyecto
con datos de producción.

Para un equipo real, la recomendación que más claramente sale de este
taller es no tratar la configuración del entorno como un detalle
menor. Varios de los problemas que más tiempo costaron acá (el
`requirements.txt` vacío, la versión de Python incompatible con una
dependencia, las rutas de importación) no tenían nada que ver con la
lógica del pipeline en sí, y aun así bloquearon el avance por completo
hasta resolverse.

### Referencias

- Documentación de DVC: https://dvc.org/doc
- Documentación de pytest: https://docs.pytest.org/
- Documentación de GitHub Actions: https://docs.github.com/actions
- Documentación de pylint: https://pylint.readthedocs.io/
- Documentación de black: https://black.readthedocs.io/
- Documentación de bandit: https://bandit.readthedocs.io/
- scikit-learn, LinearRegression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

### Reflexión final

¿Qué haría diferente si tuviera que implementar este pipeline en una
empresa con 10 TB de datos y 20 científicos de datos? Casi ninguna de
las decisiones tomadas aquí por simplicidad seguiría siendo válida. El
remoto de DVC en `/tmp/` tendría que ser almacenamiento en la nube con
control de acceso real, como S3 o Google Cloud Storage, porque ese
volumen no cabe ni tiene sentido moverlo a una carpeta local. SQLite
dejaría de ser viable como base de datos: con esa escala y esa
cantidad de gente leyendo y escribiendo a la vez, se necesita algo
pensado para concurrencia, como PostgreSQL o un almacén columnar. La
orquestación manual que usamos, correr los scripts en orden desde la
terminal o desde el CI, tendría que reemplazarse por una herramienta
como Airflow, que ya se mencionaba en la parte teórica, para programar,
reintentar y monitorear cada paso de forma independiente. Y con 20
personas tocando el mismo repositorio, el flujo de una sola rama de
feature ya no alcanzaría: haría falta una política de ramas y
revisiones, con pull requests obligatorios, para evitar el mismo caos
de colaboración que menciona la Sección 1 de la teoría, pero a una
escala donde sí importa de verdad.

¿Qué herramientas comerciales podrían facilitar el proceso y por qué?
Databricks resolvería varias piezas del taller de una sola vez: usa
Delta Lake, que da versionamiento de datos inmutable con soporte para
consultar el estado de una tabla en una fecha pasada, algo que DVC no
ofrece directamente. Dataiku está más orientado a que varias personas
con distintos niveles técnicos, no solo ingenieros, puedan colaborar
sobre el mismo pipeline, con control de linaje y gobierno de datos,
que es justo el problema de tener 20 personas trabajando a la vez.
AWS SageMaker resolvería la parte de entrenamiento y despliegue de
modelos que aquí se hizo a mano con joblib: entrenamiento gestionado,
versionamiento de modelos y endpoints de predicción sin montar esa
infraestructura desde cero. Ninguna de las tres reemplaza por completo
lo que se armó en este taller, pero cada una resuelve, de forma más
madura, una de las partes que aquí quedaron simplificadas a propósito.
