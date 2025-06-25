import os
import json
from PIL import Image
from transformers import DonutProcessor, VisionEncoderDecoderModel
from pdf2image import convert_from_path

# Configuración de rutas
MODELO_PATH = r"C:\MisCompilados\ia\model\donut-base-finetuned-cord-v2"
CARPETA_FACTURAS = r"C:\Users\scarpio\Documents\GitHub\proy_py_pdf_lector\facturas_pdf"

# Carga modelo y procesador
processor = DonutProcessor.from_pretrained(MODELO_PATH)
model = VisionEncoderDecoderModel.from_pretrained(MODELO_PATH)

# Mapeo campos salida Donut -> tus campos
MAPEADO = {
    "invoice_number": "Numero_factura",
    "date": "Fecha_emision",
    "company_name": "Nombre_proveedor",
    "company_id": "NIF_CIF_proveedor",
    "total": "Total_factura",
    "vat": "IVA",
    "tax_base": "Base_imponible",
    # Agrega aquí más campos si tu modelo los devuelve
}

def extraer_de_imagen(imagen_path):
    image = Image.open(imagen_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values
    outputs = model.generate(
        pixel_values,
        max_length=512,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )
    result = processor.batch_decode(outputs.sequences)[0]
    # Extrae el JSON (puede venir con texto antes/después, limpiamos)
    try:
        json_str = result[result.find("{"):result.rfind("}")+1]
        datos = json.loads(json_str)
    except Exception as e:
        print(f"Error al decodificar JSON en {imagen_path}:", e)
        datos = {}

    # Mapea campos de Donut a tus campos en español
    salida = {v: datos.get(k, None) for k, v in MAPEADO.items()}
    return salida

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
if __name__ == "__main__":
    resultados = procesar_carpeta(CARPETA_FACTURAS)
    print("--------------------")
    print(json.dumps(resultados, ensure_ascii=False, indent=2))
    print("--------------------")