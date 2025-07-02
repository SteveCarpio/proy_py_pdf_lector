# ---------------------------------------------------------------
# Proyecto IA: Lector de facturas en formato PDF
#
# Nombre: PDF_LECTOR
# Run:  streamlit run factura_app.py --server.address=0.0.0.0
# 
# ---------------------------------------------------------------

import streamlit as st 
import os
import io
import glob
import asyncio
import concurrent.futures
import pandas as pd

from datetime import datetime
from utils.ocr_utils import extract_text
from utils.model_runner import run_model
from utils.validation import valida_campos
from utils.data_cleaning import limpiar_campos
from utils.constants import CAMPOS


# Configuración de la página
st.set_page_config(page_title="📄 Extractor de Facturas con IA", layout="wide")
st.image("C:\\MisCompilados\\img\\logotipo.gif", width=120)
st.markdown(
    """
    <h1 style='text-align: center;'>Extractor de Facturas con IA</h1>
    """,
    unsafe_allow_html=True
)

# Subida o carga de archivos
uploaded_files = st.file_uploader("Sube varios PDFs o TXT", type=["pdf", "txt"], accept_multiple_files=True)
ruta_carpeta = st.text_input("O escribe una ruta local con facturas (Windows o Ubuntu):")

if st.button("Cargar desde carpeta"):
    if os.path.isdir(ruta_carpeta):
        archivos_en_ruta = glob.glob(os.path.join(ruta_carpeta, "*.pdf")) + glob.glob(os.path.join(ruta_carpeta, "*.txt"))
        uploaded_files = [open(ruta, "rb") for ruta in archivos_en_ruta]
    else:
        st.warning("⚠️ Ruta no válida.")

# Funciones de procesamiento
async def procesar_archivo(file_bytes, filename):
    loop = asyncio.get_event_loop()
    text = await loop.run_in_executor(None, extract_text, file_bytes)
    data = await loop.run_in_executor(None, run_model, text)

    data = limpiar_campos(data)
    valid, msg = valida_campos(data)

    data["Archivo"] = filename
    data["Ok"] = valid
    data["Error"] = msg
    return data

async def procesar_todo(files, contenedor_progreso):
    resultados = []
    total = len(files)

    for idx, file in enumerate(files, start=1):
        nombre = file.name if hasattr(file, "name") else f"desconocido_{idx}.pdf"
        contenedor_progreso.info(f"⏳ Procesando archivos, por favor espera... [{idx}/{total}] {nombre}")

        file_bytes = file.read()
        resultado = await procesar_archivo(file_bytes, nombre)
        resultados.append(resultado)

    contenedor_progreso.success("✅ Procesamiento completado.")
    return resultados

# Procesamiento principal
if uploaded_files:
    hora_inicio = datetime.now()
    total_archivos = len(uploaded_files)

    st.info(f"Procesando {total_archivos} archivo(s)...")
    st.write(f"🕐 Inicio del proceso: {hora_inicio.strftime('%H:%M:%S')}")

    # Contenedor dinámico para mostrar progreso
    progreso_placeholder = st.empty()

    # Ejecutar proceso
    resultados = asyncio.run(procesar_todo(uploaded_files, progreso_placeholder))

    # Mostrar resultados
    df = pd.DataFrame(resultados)
    st.dataframe(df)
    
    # Descargar CSV
    #csv = df.to_csv(index=False).encode("utf-8")
    #st.download_button("📥 Descargar CSV", data=csv, file_name="facturas.csv", mime="text/csv")

    # Descargar Excel en memoria
    #output = io.BytesIO()
    #with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    #    df.to_excel(writer, index=False, sheet_name='Facturas')
    #output.seek(0)
    #processed_data = output.getvalue()
    #st.download_button(
    #    "📥 Descargar Excel",
    #    data=processed_data,
    #    file_name="facturas.xlsx",
    #    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #)
    
    # Guardar automáticamente Excel en ruta local si es válida
    if ruta_carpeta and os.path.isdir(ruta_carpeta):
        ruta_salida = os.path.join(ruta_carpeta, "salida.xlsx")
        df.to_excel(ruta_salida, index=False)
        st.success(f"✅ Excel guardado automáticamente en: `{ruta_salida}`")

    # Calculo de tiempo de ejecución en horas y minutos
    hora_fin = datetime.now()
    duracion = int((hora_fin - hora_inicio).total_seconds())
    horas = duracion // 3600
    minutos = (duracion % 3600) // 60
    st.write(f"🕔 Fin del proceso: {hora_fin.strftime('%H:%M:%S')}")
    st.write(f"⏱ Duración total: {horas} h {minutos} min")

# Información de uso
st.markdown("---")
st.markdown("### ℹ️ Instrucciones de uso.")
st.markdown("""
- Puedes subir múltiples archivos PDF o TXT directamente.
- O bien, indicar una ruta local con facturas para procesar todo el contenido de esa carpeta.
- Los datos procesados se muestran en pantalla y puedes descargarlos como CSV o Excel.
- Si se proporciona una ruta válida, el Excel se guarda automáticamente en esa carpeta.
""")

# Información del autor y empresa
st.markdown("---")
st.markdown("""

**🏢 Empresa:** Titulización de Activos S.G.F.T., S.A.  
**👨‍💻 Dudas:** Steve Carpio  
**✉️ Contacto:** carpios@tda-sgft.com  
**🧾 Versión:** 1.0.0  
**🧾 Modelo:** Mistral  
            
""")
