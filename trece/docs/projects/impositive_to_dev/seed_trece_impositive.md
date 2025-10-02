# Trece Impositive

## Rol: 

Quiero qe actues como programador en python, sql y maestro en el proceso

## Objetivo:

El objetivo es mantener una base de datos relacional en sql con las socios, cosechas, retiros y gastos de 13cc, en la cual se puedan guardar datos desde varias pcs, no muchas 3 o 4.
Y Generar un prompt_impositive_v0.1.0.md para poder trabajar en los scripts.

## Contexto: 

Estamos trabajando en el manejo del proyecto 13 cannabis club, una ONG de cannabis, y la idea seria llevar el control de las socios, cosechas, retiros, y gastos dentro de la empresa

## Requisitos: 

 - Formalizar una base de datos que pueda registrar socios y proveedores dentro de una lista de entidades o la forma que te paresca conveniente.
 - Poder registrar cosechas con cantidades por genetica para el posterior retiro.
 - Poder registrar retiros de cada genetica y aclarar qe socio la retiro.
 - Poder registrar gastos y a qe proveedor se fueron.
 - Todo deberia estar cargados en una base de datos 

## Estructura fisica del proyecto:

```txt
root@e3133ded37b4:/trece# t
.
├── Dockerfile
├── README.md
├── config
│   └── config.yaml                         # Configuracion de Trece
├── database
│   └── trece.db                            # Base de datos de Trece
├── meta
│   └── schema.sql                          # Esquema completo con consultas
├── pyproject.toml
└── src
    ├── core
    │   └── impositive
    │       ├── command
    │       │   ├── load_entitie.py         # Script para cargar entidades al listado
    │       │   ├── load_expense.py         # Script para cargar gastos
    │       │   ├── load_harvest.py         # Script para cargar cosechas
    │       │   └── load_withdrawal.py      # Script para cargar retiros
    │       └── impositive.py               # Terminal cli persistente que carga comandos
    ├── script
    └── test

```

## Tablas actuales:

Te voy a dejar las tablas qe tengo en archivos .csv para qe sepas masomenos como vengo trabajando

 - expenses.csv         # id,date,amount,concept_id,entitie_id,caja_id,folio,description,notes
 - withdrawals.csv      # id,date,entitie_id,genetic_id,harvest_id,grams,price_id,status,paymethod_id,concept_id,notes,created_at
 - entities.csv         # id,name,entities_type_id,tel,mail,notes
 - genetics.csv         # id,name,description,tag
 - harvest.csv          # id,harvest_id,genetic_id,grams
 - harvest_detail.csv   # id,cut_date,module_id,description,notes
 - modules.csv          # id,name,description

> Tenia una tabla que era entities type ya qe ahi socios consumidores, reventa mayorista, inversores y empleados pero bueno espero sugerencias de mejora

## Respuesta esperada: 

 - Deberiamos en principio crear el schema sql y despues crearemos los scripts necesarios para el proyecto los cuales iran en en src/core/cli/*
 - Los scripts los subdividiremos en comandos internos para todos los calulos y poder manejarlos desde un terminal cli con los sub-scripts en una carpeta interna.
 - Dentro de los impositive/command deberia haber mas script para hacer balances como por ejemplo del mes actual, para hacer balances mes a mes, balances trimestrales entre otras cosas.
 - Me gustaria que me dijeras si estoy olvidando algun detalle y como podriamos mejorarlo
 - Tambien en vezde tantos script se podrian agregar consultas en la base de datos creo pero bueno tu me diras cual es la mejor manera de hacerlo
 - Una vez que tengamos todo pensado, ya que esto es una seed, deberiamos hacer el prompt_impositive_0.1.0.md