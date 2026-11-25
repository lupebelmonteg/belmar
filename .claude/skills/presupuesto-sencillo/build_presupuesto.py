# -*- coding: utf-8 -*-
"""Genera el PDF de presupuesto sencillo de Lupe (estilo Digiocracy / Civitatis).

Uso:  python3 build_presupuesto.py ejemplos/civitatis-enero-2027.json
El JSON describe el contenido (ver SKILL.md). Las rutas de logos son relativas a esta carpeta.
"""
import json
import os
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = [
    "/usr/share/fonts/truetype/liberation/%s.ttf",
    "/usr/share/fonts/liberation/%s.ttf",
    "/usr/share/fonts/truetype/liberation2/%s.ttf",
]


def registrar_fuentes():
    for nombre, fichero in (("S", "LiberationSans-Regular"), ("S-B", "LiberationSans-Bold")):
        for patron in FUENTES:
            ruta = patron % fichero
            if os.path.exists(ruta):
                pdfmetrics.registerFont(TTFont(nombre, ruta))
                break
        else:
            raise SystemExit("No encuentro la fuente Liberation Sans. Instálala (fonts-liberation).")


def ruta(p):
    return p if os.path.isabs(p) else os.path.join(AQUI, p)


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    registrar_fuentes()
    TEAL = HexColor(cfg.get("color", "#74BBB5"))  # verde azulado de Lupe (recuadro "Sea Light Blue")
    DARK, GREY, LINE = HexColor("#2B2B2B"), HexColor("#7A7A7A"), HexColor("#E3E3E3")
    W, H = A4
    M = 62
    RW = W - M
    salida = cfg["salida"]
    c = canvas.Canvas(salida, pagesize=A4)
    c.setTitle(cfg.get("titulo_pdf", os.path.basename(salida)))
    c.setAuthor("Lupe Belmonte")

    def spaced(x, y, text, font, size, spacing):
        c.saveState()
        t = c.beginText(x, y)
        t.setFont(font, size)
        t.setCharSpace(spacing)
        t.textLine(text)
        c.drawText(t)
        c.restoreState()
        return x + pdfmetrics.stringWidth(text, font, size) + spacing * len(text)

    def wrap(text, font, size, maxw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if pdfmetrics.stringWidth(t, font, size) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # cabecera: PRESUPUESTO + logo del cliente (o su nombre)
    y = H - 62
    c.setFillColor(TEAL)
    end = spaced(M, y, "PRESUPUESTO", "S-B", 15, 2.6)
    if cfg.get("logo_cliente"):
        img = ImageReader(ruta(cfg["logo_cliente"]))
        iw, ih = img.getSize()
        ch = 15.5
        cw = ch * iw / ih
        c.drawImage(img, end + 6, y - 0.5, width=cw, height=ch, mask="auto")
        end += 6 + cw
    else:
        end = spaced(end + 6, y, cfg["cliente"].upper(), "S-B", 15, 2.6)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.4)
    c.line(M, y - 13, end, y - 13)

    y -= 52
    c.setFillColor(DARK)
    c.setFont("S-B", 25)
    c.drawString(M, y, cfg["titulo"])
    y -= 22
    c.setFillColor(GREY)
    c.setFont("S", 11)
    c.drawString(M, y, cfg["subtitulo"])

    y -= 34
    c.setFillColor(DARK)
    c.setFont("S", 11)
    for ln in wrap(cfg["intro"], "S", 11, W - 2 * M):
        c.drawString(M, y, ln)
        y -= 17

    def seccion(titulo):
        nonlocal y
        c.setStrokeColor(TEAL)
        c.setLineWidth(1.4)
        c.line(M, y, M + 168, y)
        y -= 32
        c.setFillColor(DARK)
        c.setFont("S-B", 16)
        c.drawString(M, y, titulo)

    y -= 14
    seccion("Siempre incluido")
    y -= 32
    c.setFont("S", 10.5)
    for b in cfg["incluido"]:
        c.setFillColor(TEAL)
        c.circle(M + 3, y + 3.5, 2, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.drawString(M + 22, y, b)
        y -= 19

    y -= 6
    seccion("Inversión")
    y -= 17
    c.setFillColor(GREY)
    c.setFont("S", 10)
    if cfg.get("inversion_nota"):
        c.drawString(M, y, cfg["inversion_nota"])
    y -= 14

    partidas = cfg["partidas"]
    y -= 22
    paso = 82
    disponible = y - 110  # reserva para el total y el pie
    if disponible / len(partidas) < paso:
        paso = disponible / len(partidas)
        if paso < 70:
            print("AVISO: con tantas partidas no cabe en una página; reduce el texto.")
    for p in partidas:
        top = y + 12
        bottom = y - 60
        c.setStrokeColor(TEAL)
        c.setLineWidth(2)
        c.line(M, top, M, bottom)
        c.setFillColor(GREY)
        spaced(M + 12, y, p["etiqueta"], "S", 8.5, 0.5)
        c.setFillColor(DARK)
        c.setFont("S-B", 18)
        c.drawString(M + 12, y - 24, p["nombre"])
        c.setFillColor(GREY)
        c.setFont("S", 10)
        c.drawString(M + 12, y - 43, p["detalle"])
        c.setFillColor(TEAL)
        c.setFont("S-B", 22)
        c.drawRightString(RW, y - 22, p["precio"])
        c.setFillColor(GREY)
        c.setFont("S", 9)
        c.drawRightString(RW, y - 38, cfg.get("iva", "+ IVA"))
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.line(M, bottom - 6, RW, bottom - 6)
        y -= paso

    c.setFillColor(DARK)
    c.setFont("S-B", 12)
    c.drawString(M, y - 4, "TOTAL")
    c.setFillColor(TEAL)
    c.setFont("S-B", 24)
    c.drawRightString(RW, y - 6, cfg["total"])
    c.setFillColor(GREY)
    c.setFont("S", 9)
    c.drawRightString(RW, y - 22, cfg.get("iva", "+ IVA"))

    # pie: solo enlaces + logo BELMAR TEAM (sin teléfono ni correo)
    enlaces = cfg["enlaces"]
    tam = 7.5
    sep = "   ·   "
    sw = pdfmetrics.stringWidth(sep, "S", tam)
    anchos = [pdfmetrics.stringWidth(n, "S-B", tam) for n, _ in enlaces]
    x = W / 2 - (sum(anchos) + sw * (len(enlaces) - 1)) / 2
    for i, (n, u) in enumerate(enlaces):
        c.setFillColor(TEAL)
        c.setFont("S-B", tam)
        c.drawString(x, 54, n)
        c.linkURL(u, (x, 52, x + anchos[i], 60), relative=0)
        x += anchos[i]
        if i < len(enlaces) - 1:
            c.setFillColor(GREY)
            c.setFont("S", tam)
            c.drawString(x, 54, sep)
            x += sw
    logo = ImageReader(ruta("assets/belmar-team.png"))
    lw_, lh_ = logo.getSize()
    LW = 78
    c.drawImage(logo, W / 2 - LW / 2, 14, width=LW, height=LW * lh_ / lw_, mask="auto")
    c.save()
    print(salida)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 build_presupuesto.py config.json")
    main(sys.argv[1])
