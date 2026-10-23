#!/usr/bin/env bash
# Edita estos datos con la información real del alumno y de la escuela.
PERIODO="[PERIODO]"
BOLETA="[BOLETA]"
NOMBRE="[NOMBRE DEL ALUMNO]"
CLAVE_SEP="[CLAVE SEP]"
PROGRAMA="Téc. en Computación"
PLAN="[PLAN]"
FOTO=""   # ruta a la foto (opcional), p. ej. imagenes/foto.jpg

ARGS=(materias.csv --periodo "$PERIODO" --boleta "$BOLETA" --nombre "$NOMBRE"
      --clave-sep "$CLAVE_SEP" --programa "$PROGRAMA" --plan "$PLAN"
      --logo-izq imagenes/logo_cecyt8.png --logo-der imagenes/logo_ipn.png
      --salida horario.svg)
[ -n "$FOTO" ] && ARGS+=(--foto "$FOTO")
python3 llenar_horario.py "${ARGS[@]}"
