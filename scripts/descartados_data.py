"""Entradas descartadas en curaduría v1.1."""
from datetime import date

TODAY = str(date.today())

DESCARTADOS = [
    {
        "id": "fifa-23",
        "titulo": "FIFA 23",
        "motivo_exclusion": "Argentina es una selección entre muchas; no cumple criterio deporte central",
        "fecha_descarte": TODAY,
    },
    {
        "id": "efootball-pes-2021",
        "titulo": "eFootball PES 2021",
        "motivo_exclusion": "Selección argentina entre decenas de equipos internacionales; no es eje central",
        "fecha_descarte": TODAY,
    },
    {
        "id": "roots-of-pacha",
        "titulo": "Roots of Pacha",
        "motivo_exclusion": "Desarrollado en Argentina pero sin escenario, protagonista ni temática argentina específica",
        "fecha_descarte": TODAY,
    },
    {
        "id": "dark-rage-1997",
        "titulo": "Dark Rage",
        "motivo_exclusion": "Primer shoot'em up comercial argentino sin vínculo temático con Argentina (solo origen del desarrollo)",
        "fecha_descarte": TODAY,
    },
]

DESCARTADOS_IDS = {d["id"] for d in DESCARTADOS}
