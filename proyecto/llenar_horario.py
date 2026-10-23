#!/usr/bin/env python3
"""Genera el horario (SVG) del CECyT 8 a partir de un CSV de materias.

Uso:
  python3 llenar_horario.py materias.csv \
      --periodo "XXXXX" --boleta "XXXXXXXXXX" --nombre "NOMBRE APELLIDOS" \
      --clave-sep "XXXXXXXXXX" --programa "Téc. en Computación" --plan "XX" \
      --logo-izq 382.png --logo-der logotipo_ipn.webp --foto foto.jpg \
      --salida horario.svg

Columnas del CSV:
  grupo,clave,unidad,creditos,profesor,lunes,martes,miercoles,jueves,viernes
Cada día se escribe como  HH:MM - HH:MM|Edificio|Salón   (vacío si no hay clase).
Los datos los proporciona quien usa el script (p. ej. la base de datos escolar).
El documento NO incluye QR ni código de barras: la validación oficial es de la institución.
"""
import argparse, base64, csv, io, datetime
from xml.sax.saxutils import escape

GUINDA = "#6b1d3f"
MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto",
         "Septiembre","Octubre","Noviembre","Diciembre"]
DIAS = ["lunes","martes","miercoles","jueves","viernes"]
COLS = [46, 93, 348, 400, 560, 685, 811, 936, 1061, 1186]

def uri(path):
    from PIL import Image
    im = Image.open(path).convert("RGBA"); b = io.BytesIO(); im.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def img(path, x, y, w, h):
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}" '
            f'preserveAspectRatio="xMidYMid meet" href="{uri(path)}"/>') if path else \
           (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f4f4f4" '
            f'stroke="#999" stroke-dasharray="4 3"/>')

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--periodo", default="[PERIODO]")
    p.add_argument("--boleta", default="[BOLETA]")
    p.add_argument("--nombre", default="[NOMBRE DEL ALUMNO]")
    p.add_argument("--clave-sep", default="[CLAVE SEP]")
    p.add_argument("--programa", default="Téc. en Computación")
    p.add_argument("--plan", default="[PLAN]")
    p.add_argument("--modalidad", default="Escolarizada")
    p.add_argument("--logo-izq"); p.add_argument("--logo-der"); p.add_argument("--foto")
    p.add_argument("--salida", default="horario.svg")
    a = p.parse_args()

    with open(a.csv, newline="", encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))

    hoy = datetime.date.today()
    fecha = f"Ciudad de México a los {hoy.day} días de {MESES[hoy.month-1]} de {hoy.year}"
    cred = sum(float(r["creditos"] or 0) for r in filas)

    # alturas de fila
    alturas = [54 if any((r[d] or "").strip() for d in DIAS) else 24 for r in filas]
    ys = [322]
    for h in alturas: ys.append(ys[-1] + h)
    fin = ys[-1]
    H = max(927, fin + 330)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1236 {H}" width="1236" height="{H}" '
         f'font-family="Arial, Helvetica, sans-serif"><rect width="1236" height="{H}" fill="#fff"/>',
         '<rect x="46" y="28" width="1142" height="96" rx="8" fill="#eeeeee"/>',
         img(a.logo_izq, 48, 32, 90, 90), img(a.logo_der, 1110, 34, 70, 86),
         f'<text x="157" y="57" font-size="20" font-weight="bold" fill="{GUINDA}">'
         'CENTRO DE ESTUDIOS CIENTÍFICOS Y TECNOLÓGICOS No. 8</text>',
         '<text x="157" y="76" font-size="15" font-weight="bold">&quot;NARCISO BASSOLS&quot;</text>',
         f'<text x="157" y="113" font-size="13">CCT (Clave SEP): {escape(a.clave_sep)}</text>',
         '<path d="M468 116H768V132Q768 140 760 140H476Q468 140 468 132Z" fill="#eeeeee"/>',
         '<text x="616" y="133" font-size="16" font-weight="bold" text-anchor="middle">Horario del alumno</text>',
         img(a.foto, 46, 127, 135, 164),
         f'<line x1="203" y1="140" x2="203" y2="278" stroke="{GUINDA}" stroke-width="2"/>']
    info = [("Periodo escolar: ", a.periodo), ("Boleta: ", a.boleta), ("Nombre: ", a.nombre),
            ("Programa Académico: ", a.programa), ("Plan de Estudios: ", a.plan),
            ("Carga inscrita: ", f"{len(filas)} unidades de aprendizaje, {cred:g} créditos"),
            ("Modalidad: ", a.modalidad)]
    for i, (k, v) in enumerate(info):
        o.append(f'<text x="217" y="{152+i*20}" font-size="15">{escape(k)}'
                 f'<tspan font-weight="bold">{escape(v)}</tspan></text>')
    o.append(f'<text x="1186" y="289" font-size="15" text-anchor="end">{fecha}</text>')
    o.append(f'<rect x="46" y="297" width="1140" height="25" fill="{GUINDA}"/>')
    for i, h in enumerate(["Gpo.","Unidad de aprendizaje","Créditos","Profesor",
                           "Lunes","Martes","Miércoles","Jueves","Viernes"]):
        cx = (COLS[i] + COLS[i+1]) / 2
        o.append(f'<text x="{cx}" y="314" font-size="{9 if h=="Créditos" else 14}" '
                 f'font-weight="bold" fill="#fff" text-anchor="middle">{h}</text>')

    for r, row in enumerate(filas):
        m = (ys[r] + ys[r+1]) / 2
        o.append(f'<text x="69" y="{m+3}" font-size="9.5" text-anchor="middle">{escape(row["grupo"])}</text>')
        unidad = f'{row["clave"]} - {row["unidad"]}'.strip(" -")
        if len(unidad) > 50:
            corte = unidad.rfind(" ", 0, 50)
            o.append(f'<text x="97" y="{m-1}" font-size="7">{escape(unidad[:corte])}</text>'
                     f'<text x="97" y="{m+8}" font-size="7">{escape(unidad[corte+1:])}</text>')
        else:
            o.append(f'<text x="97" y="{m+3}" font-size="7">{escape(unidad)}</text>')
        o.append(f'<text x="374" y="{m+3}" font-size="7.5" text-anchor="middle">{escape(row["creditos"])}</text>')
        prof = row["profesor"]
        if len(prof) > 30:
            corte = prof.rfind(" ", 0, 30)
            o.append(f'<text x="404" y="{m-1}" font-size="7">{escape(prof[:corte])}</text>'
                     f'<text x="404" y="{m+8}" font-size="7">{escape(prof[corte+1:])}</text>')
        else:
            o.append(f'<text x="404" y="{m+3}" font-size="7">{escape(prof)}</text>')
        for d, dia in enumerate(DIAS):
            celda = (row[dia] or "").strip()
            if not celda: continue
            partes = [x.strip() for x in celda.split("|")] + ["", ""]
            cx = (COLS[4+d] + COLS[5+d]) / 2
            o.append(f'<text x="{cx}" y="{m-8}" font-size="8" text-anchor="middle">{escape(partes[0])}</text>'
                     f'<text x="{cx}" y="{m+6}" font-size="7" text-anchor="middle">Edificio: {escape(partes[1])}</text>'
                     f'<text x="{cx}" y="{m+15}" font-size="7" text-anchor="middle">Salón: {escape(partes[2])}</text>')

    for y in ys: o.append(f'<line x1="46" y1="{y}" x2="1186" y2="{y}" stroke="#000" stroke-width="0.8"/>')
    for x in COLS: o.append(f'<line x1="{x}" y1="322" x2="{x}" y2="{fin}" stroke="#000" stroke-width="0.8"/>')
    o.append(f'<text x="46" y="{H-21}" font-size="9" font-family="Courier New, monospace">'
             'DOCUMENTO INFORMATIVO SIN VALIDEZ OFICIAL. LA VALIDACIÓN CORRESPONDE A LA INSTITUCIÓN.</text></svg>')

    with open(a.salida, "w", encoding="utf-8") as f: f.write("\n".join(o))
    print("Generado:", a.salida)

if __name__ == "__main__":
    main()
