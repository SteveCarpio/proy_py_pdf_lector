import os
import json
import pandas as pd
from extract.pdf_reader import extraer_texto_pdf, convertir_pdf_a_imagenes
from extract.ocr_engine import imagen_a_texto
from ia.ollama_interface import extraer_datos_factura

def procesar_factura(path_pdf):
    tiene_texto, texto = extraer_texto_pdf(path_pdf)

    if not tiene_texto:
        print(f"{path_pdf} parece escaneado. Aplicando OCR...")
        imagenes = convertir_pdf_a_imagenes(path_pdf)
        texto = ""
        for imagen in imagenes:
            texto += imagen_a_texto(imagen) + "\n"

    print(f"📄 Procesando: {os.path.basename(path_pdf)}")

    try:
        respuesta_str = extraer_datos_factura(texto)
        datos = json.loads(respuesta_str)
        return datos
    except json.JSONDecodeError as e:
        print(f"❌ Error al interpretar JSON en {path_pdf}: {e}")
        return {}
    except Exception as e:
        print(f"❌ Error inesperado en {path_pdf}: {e}")
        return {}

def formatear_importes(dato):
    if isinstance(dato, str):
        try:
            num = float(dato.replace('.', '').replace(',', '.'))
            return f"{num:,.2f}"
        except:
            return dato
    return dato

def normalizar_fila(datos):
    campos_objetivo = [
        'Número de factura', 'Fecha de emisión', 'Nombre del proveedor',
        'NIF/CIF del proveedor', 'Base imponible', 'IVA', 'Total factura',
        'Tipo de fondo', 'ID_PRESTAMO', 'id_prestamo'  # añadimos variante por si acaso
    ]
    fila = {}
    for campo in campos_objetivo:
        if campo in datos:
            fila[campo] = datos[campo]

    for campo in ['Base imponible', 'IVA', 'Total factura']:
        if campo in fila:
            fila[campo] = formatear_importes(fila[campo])
    return fila

if __name__ == "__main__":
    carpeta_facturas = "facturas_pdf"
    archivos = [f for f in os.listdir(carpeta_facturas) if f.lower().endswith(".pdf")]

    filas = []
    for archivo in archivos:
        path = os.path.join(carpeta_facturas, archivo)
        datos = procesar_factura(path)
        if datos:
            fila = normalizar_fila(datos)
            fila['Archivo'] = archivo
            filas.append(fila)

    if filas:
        df = pd.DataFrame(filas)
        df.to_excel("facturas_consolidadas.xlsx", index=False)
        print("\n✅ Excel generado: facturas_consolidadas.xlsx")
    else:
        print("⚠️ No se generó ninguna fila. Verifica las respuestas.")
