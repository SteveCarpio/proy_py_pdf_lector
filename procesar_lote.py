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
        print(respuesta_str)
        datos = json.loads(respuesta_str)
        return datos
    except json.JSONDecodeError as e:
        print(f"❌ Error interpretando JSON en {path_pdf}: {e}")
        return {}
    except Exception as e:
        print(f"❌ Error inesperado en {path_pdf}: {e}")
        return {}

def formatear_importes(valor):
    if isinstance(valor, str):
        try:
            numero = float(valor.replace('.', '').replace(',', '.'))
            return f"{numero:,.2f}"
        except:
            return valor
    return valor

def normalizar_fila(datos):
    # Homogeneizamos claves para facilitar compatibilidad con Excel
    claves = {
        'Numero_factura': 'Número de factura',
        'Fecha_emision': 'Fecha de emisión',
        'Nombre_proveedor': 'Nombre del proveedor',
        'NIF_CIF_proveedor': 'NIF/CIF del proveedor',
        'Base_imponible': 'Base imponible',
        'IVA': 'IVA',
        'Total_factura': 'Total factura',
        'Tipo_fondo': 'Tipo de fondo',
        'Id_prestamo': 'ID_PRESTAMO'
    }

    fila = {}
    for clave_origen, clave_destino in claves.items():
        valor = datos.get(clave_origen, "")
        if clave_destino in ['Base imponible', 'IVA', 'Total factura']:
            valor = formatear_importes(valor)
        fila[clave_destino] = valor

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
