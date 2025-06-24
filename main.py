'''
Título del proyecto: "Sistema inteligente de extracción de datos de facturas"
Objetivo: Crear un programa que lea automáticamente facturas en PDF y extraiga datos clave como el nombre del proveedor, fecha, monto total, etc.

¿Cómo funciona?
Lectura de facturas: El sistema revisa una carpeta donde se colocan las facturas (PDFs). 
Pueden ser archivos que tienen texto digital o imágenes escaneadas.

Procesamiento con inteligencia artificial (IA): Usamos IA para “entender” cada factura, incluso si el diseño es diferente en cada una.

Extracción de datos: La IA detecta y extrae los datos importantes, sin necesidad de que alguien los escriba a mano.

¿Qué dificultad tiene?
Modelos de IA: Para que el sistema entienda bien las facturas, se usan modelos de inteligencia artificial. Existen modelos más potentes y precisos, pero requieren computadoras muy potentes (más memoria y tarjetas gráficas mejores).

Limitaciones actuales: Como estoy usando una computadora personal que no es muy potente, estoy usando un modelo más pequeño (de 7 mil millones de parámetros, llamado "modelo 7B"). Esto funciona, pero puede cometer más errores o tardar más que otros modelos más grandes (por ejemplo, modelos 13B o 70B).

Lo positivo: A pesar de las limitaciones de hardware, el sistema ya es capaz de leer varias facturas automáticamente desde una carpeta y procesarlas, lo que ahorra tiempo comparado con hacerlo manualmente.

¿Qué se necesitaría para mejorar?
Si queremos más precisión y velocidad, podríamos usar modelos más grandes, pero eso requiere:

Un mejor servidor (más memoria y una buena GPU).

O pagar un servicio en la nube que nos permita usar esos modelos sin comprar el hardware.

¿Qué resultados se pueden esperar ahora?
El sistema es funcional, pero no perfecto.

Puede tener dificultades con algunas facturas complejas o muy mal escaneadas.

A medida que se optimiza o se mejora el hardware, se puede lograr un nivel de precisión más alto.

Parte técnica (para ti):
Dado que las facturas vienen en PDF (texto y escaneadas), necesitas:

OCR (Reconocimiento Óptico de Caracteres):

Usa algo como Tesseract OCR para las facturas en imagen (o mejor aún, PaddleOCR o Google Vision OCR, que son más precisos).

Para PDFs con texto embebido, puedes usar PyMuPDF (fitz) o pdfplumber para extraer el texto directamente.

Modelos de lenguaje para extracción semántica:

Estás usando un modelo 7B, como un LLaMA 2 o Mistral 7B. Estos pueden funcionar, especialmente si los usas con instrucciones claras (instrucción tuning).

Mejores resultados los podrías obtener con modelos como:

GPT-4 (si usas la API de OpenAI)

Claude 3 (Anthropic)

Gemini Pro (Google)

O modelos open-source más grandes, como Mixtral 8x7B, LLaMA 3 13B, etc.

Estos últimos requieren:

GPU con al menos 24-48 GB de VRAM (para local)

O servicios como Hugging Face Inference Endpoints, Replicate, o OpenRouter.ai para ejecutarlos en la nube.

Formato de salida:
Excel
'''

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
    print("------------- Inicio -------------")
    print(respuesta)
    print("------------- Fin -------------")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py ruta_a_factura.pdf")
        sys.exit(1)

    ruta_factura = sys.argv[1]
    procesar_factura(ruta_factura)
