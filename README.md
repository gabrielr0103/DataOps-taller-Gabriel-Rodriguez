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
6. 6. Generar la base de datos de prueba: `python3 scripts/create_db.py`

## Estructura del repositorio
```bash
dataops-taller-gabriel-rodriguez/ 
│
├── .github/ 
│ └── workflows/ 
│     └── ci.yml 
│ 
├── data/ 
│ 
├── notebooks/ 
│   └── exploracion.ipynb 
│ 
├── src/ 
│   ├── extract.py 
│   ├── transform.py 
│   ├── train.py 
│   └── utils.py 
│ 
├── tests/ 
│   ├── test_extract.py 
│   ├── test_transform.py 
│   └── test_train.py 
│ 
├── scripts/ 
│   └── create_db.py 
│ 
├── requirements.txt 
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
