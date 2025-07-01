# validation.py
# -------------------------------------------
# Verifica que los campos extraídos tengan
# formato válido (fechas y números).
# -------------------------------------------

import re

def valida_campos(d):
    """
    Valida:
    - Fecha_emision tenga formato válido YYYY-MM-DD
    - Valores numéricos puedan convertirse a float
    """
    ok = True
    msg = ""

    if not re.match(r"\d{4}-\d{2}-\d{2}", d.get("Fecha_emision", "")):
        ok = False
        msg += "❌ Fecha inválida. "

    for campo in ["Base_imponible", "IVA", "Total_factura"]:
        try:
            float(d[campo])
        except:
            ok = False
            msg += f"❌ '{campo}' no es numérico. "

    return ok, msg
