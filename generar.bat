@echo off
REM Edita estos datos con la informacion real del alumno y de la escuela.
set PERIODO=[PERIODO]
set BOLETA=[BOLETA]
set NOMBRE=[NOMBRE DEL ALUMNO]
set CLAVE_SEP=[CLAVE SEP]
set PROGRAMA=Tec. en Computacion
set PLAN=[PLAN]
python llenar_horario.py materias.csv --periodo "%PERIODO%" --boleta "%BOLETA%" --nombre "%NOMBRE%" --clave-sep "%CLAVE_SEP%" --programa "%PROGRAMA%" --plan "%PLAN%" --logo-izq imagenes\logo_cecyt8.png --logo-der imagenes\logo_ipn.png --salida horario.svg
