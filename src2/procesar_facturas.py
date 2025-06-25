import os
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path

import os
os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"

# Descargar modelo y procesador
#processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
#model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

# Descargarlos desde este URL:  https://huggingface.co/naver-clova-ix/donut-base-finetuned-cord-v2/tree/main
#                               todos los files a una ruta de cualquiera y ponerlo aquí
processor = DonutProcessor.from_pretrained(r"C:\MisCompilados\ia\model\donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained(r"C:\MisCompilados\ia\model\donut-base-finetuned-cord-v2")

# Define los campos y variantes
CAMPOS = {
    "Numero_factura": ["Nº factura", "Número de factura", "Factura nº", "Expediente"],
    "Fecha_emision": ["Fecha", "Fecha emisión", "Emisión", "Expedida"],
    "Nombre_proveedor": ["emisor", "proveedor", "seller", "vendor", "razón social emisor"],
    "NIF_CIF_proveedor": ["NIF","CIF"],
    "Base_imponible": ["base", "base imponible"],    
    "IVA": ["importe del IVA"],
    "Total_factura": ["Total", "Total a Pagar", "monto total", "total factura"],
    "Tipo_fondo": ["debe ser exactamente TDA 22 o TDA 28"],
    "Id_prestamo": ["número de 14 dígitos que comienza por 5200015, si contiene puntos su tamaño será mayor a 14"],
    "Numero_Procd": ["Procd"],
    "IRPF": ["IRPF", "RPF", "LR.P.F"]
    }

def extraer_campos_desde_texto(texto, campos):
    salida = {}
    texto_lower = texto.lower()
    for campo, variantes in campos.items():
        for variante in variantes:
            idx = texto_lower.find(variante)
            if idx != -1:
                linea = texto[idx:].split("\n", 1)[0]
                valor = linea.replace(variante, "").replace(":", "").strip()
                salida[campo] = valor
                break
    return salida

def extraer_de_imagen(imagen_path):
    image = Image.open(imagen_path).convert("RGB")
    task_prompt = "<s_cord-v2>"
    pixel_values = processor(image, return_tensors="pt").pixel_values
    outputs = model.generate(
        pixel_values,
        max_length=512,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )
    result = processor.batch_decode(outputs.sequences)[0]
    return extraer_campos_desde_texto(result, CAMPOS)

def procesar_carpeta(ruta_carpeta):
    resultados = {}
    for fname in os.listdir(ruta_carpeta):
        ruta = os.path.join(ruta_carpeta, fname)
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Procesando imagen: {fname}")
            datos = extraer_de_imagen(ruta)
            resultados[fname] = datos
        elif fname.lower().endswith(".pdf"):
            print(f"Procesando PDF: {fname}")
            paginas = convert_from_path(ruta, dpi=200, first_page=1, last_page=1)
            temp_img = "temp_img.png"
            paginas[0].save(temp_img, "PNG")
            datos = extraer_de_imagen(temp_img)
            resultados[fname] = datos
            os.remove(temp_img)
    return resultados

# USO
carpeta_facturas = "C:/Users/scarpio/Documents/GitHub/proy_py_pdf_lector/facturas_pdf"
resultados = procesar_carpeta(carpeta_facturas)
print("--------------------")
print(resultados)
print("--------------------")