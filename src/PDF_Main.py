# ----------------------------------------------------------------------------------------
#                        Proyecto Python: PDF Lector
#
# Programa que extraerá información de varios PDF en una estructura homogénea 
# Autor: SteveCarpio
# Versión: V1 2025
# ----------------------------------------------------------------------------------------

from   cfg.PDF_librerias import *
from   cfg.PDF_ayuda     import sTv_ayuda
from   pdf.PDF_paso0     import sTv_paso0
from   pdf.PDF_paso1     import sTv_paso1
from   pdf.PDF_paso2     import sTv_paso2
from   pdf.PDF_paso3     import sTv_paso3
from   pdf.PDF_paso4     import sTv_paso4
from   pdf.PDF_paso5     import sTv_paso5
from   pdf.PDF_paso6     import sTv_paso6


var_Parametro = ""
if len(sys.argv) > 1:
    var_Parametro = str(sys.argv[1])

if var_Parametro == "?":
    sTv_ayuda()
    sys.exit(0)

var_Entorno="DEV"
if var_Parametro == "PRO":
    var_Entorno = "PRO"

# Inicializar colorama
init(autoreset=True)

# ----------------------------------------------------------------------------------------
#                                  PARÁMETROS DE ENTRADA
# ----------------------------------------------------------------------------------------


# Nombres de Salida
var_NombreSalida= f'PDF'

var_Fecha = dt.now()
var_Fechas1 = var_Fecha.strftime('%Y-%m-%d')  # Formato "2025-03-04"

# ----------------------------------------------------------------------------------------
#                                  EJECUCION PASOS
# ----------------------------------------------------------------------------------------
var_tit0 = f'--- 0'
var_tit1 = f'--- 1'
var_tit2 = f'--- 2'
var_tit3 = f'--- 3'
var_tit4 = f'--- 4'
var_tit5 = f'--- 5'
var_tit6 = f'--- 6'
var_tit9 = f'EJECUTAR TODOS LOS PASOS'
var_tmp0 = " "
var_tmp1 = " "
var_tmp2 = " "
var_tmp3 = " "
var_tmp4 = " "
var_tmp5 = " "
var_tmp6 = " "
var_tmp9 = " "

while True:
    os.system('cls')
    
    print(Fore.MAGENTA + "=" * 94)
    print(Fore.MAGENTA + "  Proceso PDF Lector                               |  Modo   : " + var_Entorno)
    print(Fore.MAGENTA + "                                                             ")
    print(Fore.MAGENTA + "    Ejecutar los pasos del proyecto                          ")
    print(Fore.MAGENTA + "    Escriba otro valor para salir del programa               ")
    print(Fore.MAGENTA + "                                                             ")
    print(Fore.MAGENTA + "=" * 94 + "\n")

    print(Fore.LIGHTWHITE_EX + f'{var_tmp0}   0 = {var_tit0}')
    print(Fore.YELLOW + f'{var_tmp1}   1 = {var_tit1}')
    print(Fore.GREEN + f'{var_tmp2}   2 = {var_tit2}')
    print(Fore.YELLOW + f'{var_tmp3}   3 = {var_tit3}')
    print(Fore.BLUE + f'{var_tmp4}   4 = {var_tit4}')
    print(Fore.BLUE + f'{var_tmp5}   5 = {var_tit5}')
    print(Fore.YELLOW + f'{var_tmp6}   6 = {var_tit6}')
    print(Fore.LIGHTWHITE_EX + f'{var_tmp9}   9 = {var_tit9}') 
    print(Fore.MAGENTA + f'    ? = AYUDA')
    print(Fore.MAGENTA + f'\n                      ¡ Para SALIR escriba otro valor !')
    var_PASO = input(Fore.MAGENTA + "\n>>> ")

    match var_PASO:
        case "0":
            # Ejecución del paso 0
            print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida)
            var_tmp0 = '*'

        case "1":
            # Ejecución del paso 1

            if var_tmp0 != '*':  # Si no ejecuto el paso 0 lo invoco
                # Ejecución del paso 0
                print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
                sTv_paso0(var_NombreSalida)
                var_tmp0 = '*'

            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida)
            var_tmp1 = '*'

        case "2":        
            # Ejecución del paso 2
            print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida)
            var_tmp2 = '*'

        case "3":
            # Ejecución del paso 3 
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3} ]\n ')
            sTv_paso3(var_NombreSalida)
            var_tmp3 = '*'

        case "4":
            # Ejecución del paso 4 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida)
            var_tmp4 = '*'
            
        case "5":
            # Ejecución del paso 5 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida)
            var_tmp5 = '*'

        case "6":
            # Ejecución del paso 6 
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ]\n ')
            sTv_paso6(var_NombreSalida)
            var_tmp6 = '*'

        case "9":
            print(Fore.LIGHTWHITE_EX + f' \n--------------------------------- [ {var_tit0} ]\n ')
            sTv_paso0(var_NombreSalida)
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit1} ]\n ')
            sTv_paso1(var_NombreSalida)
            print(Fore.GREEN + f' \n--------------------------------- [ {var_tit2} ]\n ')
            sTv_paso2(var_NombreSalida)
            print(Fore.YELLOW + f' \n--------------------------------- [ {var_tit3}]\n ')
            sTv_paso3(var_NombreSalida)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit4} ]\n ')
            sTv_paso4(var_NombreSalida)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit5} ]\n ')
            sTv_paso5(var_NombreSalida)
            print(Fore.BLUE + f' \n--------------------------------- [ {var_tit6} ]\n ')
            sTv_paso6(var_NombreSalida)
            var_tmp9 = '*'

        case "?":
            sTv_ayuda()

        case _:
            print(Fore.RED + f"    ¡Saliendo del programa!\n")
            sys.exit(0)
    
    continuar = input(Fore.MAGENTA + "\n\n¡Pulse una tecla para continuar! ").strip()
    #if continuar.upper() != "S":
    #    break

