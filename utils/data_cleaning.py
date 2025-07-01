# data_cleaning.py
# -------------------------------------------
# Limpieza de campos numéricos y fechas
# para estandarizar la salida del modelo.
# -------------------------------------------

from datetime import datetime

def normalizar_fecha(fecha):
    """
    Convierte una fecha en distintos formatos a 'YYYY-MM-DD'.
    """
    if not fecha:
        return ""

    original = str(fecha).strip()
    formatos = ("%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d")

    for fmt in formatos:
        try:
            return datetime.strptime(original, fmt).strftime("%Y-%m-%d")
        except:
            continue

    return original

def normalizar_numero(valor):
    """
    Convierte un valor numérico (string o número) a decimal con dos cifras.
    """
    if valor is None:
        return ""

    original = valor
    try:
        if isinstance(valor, str):
            cleaned = valor.strip().replace("€", "").replace(",", ".")
        else:
            cleaned = str(valor)

        return "{:.2f}".format(float(cleaned))
    except:
        return original

def limpiar_campos(data):
    """
    Limpia y normaliza los campos numéricos y de fecha.
    """
    campos_num = ["Base_imponible", "IVA", "Total_factura", "IRPF"]
    campos_fecha = ["Fecha_emision"]

    for f in campos_num:
        data[f] = normalizar_numero(data.get(f, ""))

    for f in campos_fecha:
        data[f] = normalizar_fecha(data.get(f, ""))

    return data
