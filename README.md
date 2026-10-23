# Generador de horario - CECyT 8 "Narciso Bassols"

1. `pip install -r requirements.txt`
2. Edita `materias.csv` (una fila por materia; cada día como `HH:MM - HH:MM|Edificio|Salón`).
3. Edita los datos en `generar.sh` (o `generar.bat` en Windows): periodo, boleta, nombre, clave SEP, programa y plan.
4. Ejecuta `bash generar.sh` -> se crea `horario.svg`. Para agregar foto, define `FOTO` en el script.

Notas
- La fecha es la del día en que se ejecuta.
- El documento no genera QR ni código de barras y trae la leyenda
  "DOCUMENTO INFORMATIVO SIN VALIDEZ OFICIAL". La validación oficial es de la institución.
- Los datos personales y la clave SEP deben ser los reales, proporcionados por la escuela.
