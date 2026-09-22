# DataOps-taller-Gabriel-Rodriguez

##Pipeline de Datos para Tienda en Línea

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

## Estructura del repositorio

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

