# Cloud Models Classifier

Aplicacion de escritorio en Java con interfaz grafica Swing para clasificar texto como IaaS, PaaS, SaaS o FaaS usando reglas simples, palabras clave y expresiones regulares.

## Requisitos Java

- Java 26 o superior

## Compilacion

```bash
mkdir -p out
javac -d out $(find src -name '*.java')
```

## Ejecucion

```bash
java -cp out cloudmodelsclassifier.CloudServiceClassifierApp
```

## Version Python con Tkinter

La version Python separa el preprocesamiento NLP (`nlp.py`), las reglas y el
servicio de clasificacion (`classifier.py`), los modelos de dominio
(`models.py`) y la interfaz (`gui.py`). No requiere dependencias externas.

### Ejecucion

Desde la raiz del proyecto:

```bash
python3 main.py
```

Para usar la interfaz de linea de comandos:

```bash
python3 classifier.py --text "ejecutar una función cuando se suba una imagen"
```

Salida esperada:

```text
Modelo identificado: FaaS
```

La GUI y la CLI reutilizan `CloudServiceClassifier`; ninguna interfaz duplica
las reglas de NLP o clasificacion.

Para ejecutar las pruebas del clasificador:

```bash
python3 -m unittest discover -s tests -v
```

## Estructura

- `src/cloudmodelsclassifier/CloudServiceClassifierApp.java`: interfaz grafica y manejo de eventos.
- `src/cloudmodelsclassifier/CloudServiceClassifier.java`: reglas de clasificacion por modelo Cloud.
- `models.py`: modelos de dominio y resultado estructurado.
- `nlp.py`: normalizacion y filtrado de stopwords.
- `classifier.py`: reglas reutilizables de clasificacion.
- `gui.py`: interfaz grafica Tkinter.
- `cli.py`: interfaz de linea de comandos con `argparse`.
- `classifier.py`: lanzador de la CLI desde la raiz del proyecto.
