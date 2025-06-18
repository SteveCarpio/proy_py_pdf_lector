import subprocess

def extraer_datos_factura(texto_factura, modelo="mistral"):
    prompt = f"""
Eres un sistema inteligente de extracción de datos de facturas. A partir del siguiente texto extraído de una factura, genera un JSON con los siguientes campos:
- Numero_factura
- Fecha_emisión
- Nombre_proveedor
- NIF_CIF_proveedor
- Base_imponible
- IVA
- Total_factura

Además quiero que me crees un campo 'Tipo_fondo', que podrá tener el texto 'TDA 22' o 'TDA 28'
Además en las facturas vienen un valor con 14 dígitos, donde los primeros 7 primeros vienen con el valor: 5200015 ese valor me lo debes crear como un campo 'Id_prestamo'
Texto de la factura:
\"\"\"
{texto_factura}
\"\"\"
"""
    proceso = subprocess.run(
        ['ollama', 'run', modelo],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )
    return proceso.stdout.decode()
