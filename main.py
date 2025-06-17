import sys
from extract.pdf_reader import extraer_texto_pdf, convertir_pdf_a_imagenes
from extract.ocr_engine import imagen_a_texto
from ia.ollama_interface import extraer_datos_factura

def procesar_factura(path_pdf):
    tiene_texto, texto = extraer_texto_pdf(path_pdf)

    if not tiene_texto:
        print("Factura escaneada. Usando OCR...")
        imagenes = convertir_pdf_a_imagenes(path_pdf)
        texto = ""
        for imagen in imagenes:
            texto += imagen_a_texto(imagen) + "\n"

    print("\n📄 Texto extraído:\n")
    print(texto[:1000])  # Solo muestra los primeros caracteres

    print("\n🤖 Extrayendo datos con IA...")
    respuesta = extraer_datos_factura(texto)
    print("\n🧾 Datos extraídos:\n")
    print(respuesta)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py ruta_a_factura.pdf")
        sys.exit(1)

    ruta_factura = sys.argv[1]
    procesar_factura(ruta_factura)
