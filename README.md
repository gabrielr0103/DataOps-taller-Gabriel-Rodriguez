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
├── .github/workflows/ci.yml
├── data/
├── notebooks/exploracion.ipynb


## Comandos básicos de Git utilizados
- `git checkout -b feature/pipeline-inicial` — crear la rama de trabajo
- `git add <archivo>` — preparar cambios (staging)
- `git commit -m "mensaje"` — confirmar cambios de forma atómica
- `git push -u origin feature/pipeline-inicial` — subir la rama al repositorio remoto
├── src/ (extract.py, transform.py, train.py, utils.py)
├── tests/ (test_extract.py, test_transform.py, test_train.py)
├── scripts/create_db.py
├── requirements.txt
├── .gitignore
└── README.md

