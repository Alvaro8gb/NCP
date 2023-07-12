# NCP : NLP Cancer Pipeline

Conversión de un juicio clinico escrito en lenguaje natural a un JSON con los campos mas importantes para su analisis y minado.

![img](static/img/pipeline.png)

# Preprocesamiento

Solo se desacronimiza si es conocido [link](http://www.redsamid.net/archivos/201612/diccionario-de-siglas-medicas.pdf?0) y no tiene conflictos con otras palabras. El objetivo principal es corregir errores de escritura para mejorar los resultados de la red.


# Anotacion

Se realiza con la herramienta Prodigy de Explosion

# Transformers Networks

Modelos NER, finetuneados a partir de un modelo prentrenado.

# Postprocesamiento: 

Dos fases: 

## Normalizar  

Terminos definitivos de la base de datos

## Estructuración

Como se estrcutura


# CMDS

## demo
	python demo/use_pk.py
	
## build
	python setup.py sdist

# Other 
- Interpretabilidad del pipeline

Para ver de donde venis siempre se guardara un registro de la entrada del modelo.

- ¿ tratar por nota o sentencia?