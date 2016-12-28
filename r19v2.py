# coding=utf-8
import sys, os, os.path, shutil, time
from lxml import etree


def conviertenumero(numero, decimales):
    if str.isnumeric(str(decimales)) == 'False':
        decimales = 0
    # convierte el importe en float sin decimales
    importe = "{:.0f}".format(float(numero))
    # calcula la longitud del importe
    limporte = len(importe)
    # dos ultimas posiciones para los decimales, el resto parte entera y . decimal
    if decimales != 0:
        importe = importe[0:limporte - decimales] + "." + importe[limporte - decimales:limporte]
    return importe


def cargararraycabecera01(t):
    cabecera[0] = t[123:158]  # Identificacion del mensaje
    cabecera[1] = t[115:123]  # Fecha y hora de creacion
    cabecera[4] = t[45:115]  # Nombre
    cabecera[6] = t[10:26]  # Identificacion
    cabecera[8] = t[166:177]  # IBAN
    if not cabecera[8].strip():
        cabecera[8] = "NOTPROVIDED"


def cargararraycabecera02(t):
    cabecera[7] = t[265:290]  # IBAN Empresa emite remesa


def parseartotal99(t):
    cabecera[2] = t[19:27]  # Numero de operaciones
    cabecera[3] = t[2:19]  # Control de suma


def parsearcabecera01():
    fecha = time.strftime("%Y-%m-%dT%H:%M:%S")
    GrpHdr = etree.SubElement(CstmrPmtRvsl, "GrpHdr")
    MsgId = etree.SubElement(GrpHdr, "MsgId")
    CreDtTm = etree.SubElement(GrpHdr, "CreDtTm")
    NbOfTxs = etree.SubElement(GrpHdr, "NbOfTxs")
    CtrlSum = etree.SubElement(GrpHdr, "CtrlSum")
    InitgPty = etree.SubElement(GrpHdr, "InitgPty")
    Nm = etree.SubElement(InitgPty, "Nm")
    Id = etree.SubElement(InitgPty, "Id")
    OrgId = etree.SubElement(Id, "OrgId")
    Othr = etree.SubElement(OrgId, "Othr")
    Id = etree.SubElement(Othr, "Id")

    MsgId.text = cabecera[0].strip()
    # CreDtTm.text = cabecera[1].strip()
    CreDtTm.text = fecha
    # NbOfTxs.text = "{:.0f}".format(float(cabecera[2].strip()))
    # convierte el importe en float sin decimiales
    # importe = "{:.0f}".format(float(cabecera[3].strip()))
    # calcula la longitud del importe
    # limporte = len(importe)
    # dos ultimas posiciones para los decimales, el resto parte entera y . decimal
    # importe = importe[0:limporte-2] + "." + importe[limporte-2:limporte]
    # CtrlSum.text = importe
    NbOfTxs.text = conviertenumero(cabecera[2].strip(), 0)
    CtrlSum.text = conviertenumero(cabecera[3].strip(), 2)
    Nm.text = cabecera[4].strip()
    Id.text = cabecera[6].strip()


def parseardetalle03(t):
    # PmtInf = etree.SubElement(CstmrPmtRvsl, "PmtInf")
    PmtInfId = etree.SubElement(PmtInf, "PmtInfId")
    PmtMtd = etree.SubElement(PmtInf, "PmtMtd")
    # BtchBookg = etree.SubElement(PmtInf, "BtchBookg") lo elimino para que haga un apunte por el total en nuestra cuenta
    PmtInfId.text = t[10:45].strip()
    PmtMtd.text = "DD"
    # BtchBookg.text = "true"  lo elimino para que haga un apunte por el total en nuestra cuenta
    PmtTpInf = etree.SubElement(PmtInf, "PmtTpInf")
    SvcLvl = etree.SubElement(PmtTpInf, "SvcLvl")
    Cd = etree.SubElement(SvcLvl, "Cd")
    Cd.text = "SEPA"
    LclInstrm = etree.SubElement(PmtTpInf, "LclInstrm")
    Cd = etree.SubElement(LclInstrm, "Cd")
    if t[2:7] == "19143":
        Cd.text = "CORE"
    else:
        Cd.text = "COR1"
    SeqTp = etree.SubElement(PmtTpInf, "SeqTp")
    SeqTp.text = t[80:84].strip()
    ReqdColltnDt = etree.SubElement(PmtInf, "ReqdColltnDt")
    ReqdColltnDt.text = t[26:30] + "-" + t[30:32] + "-" + t[32:34]
    Cdtr = etree.SubElement(PmtInf, "Cdtr")
    Nm = etree.SubElement(Cdtr, "Nm")
    Nm.text = cabecera[4].strip()
    # ----------------------------------------------------------
    # deshabilitado pq no quiero que pase la direccion
    # Nm.text = t[118:188].strip()
    # PstlAdr = etree.SubElement(Cdtr, "PstlAdr")
    # Ctry = etree.SubElement(PstlAdr, "Ctry")
    # Ctry.text = t[328:330]
    # AdrLine = etree.SubElement(PstlAdr, "AdrLine")
    # AdrLine.text = t[188:238].strip()
    # -----------------------------------------------------------
    CdtrAcct = etree.SubElement(PmtInf, "CdtrAcct")
    Id = etree.SubElement(CdtrAcct, "Id")
    IBAN = etree.SubElement(Id, "IBAN")
    IBAN.text = cabecera[7].strip()
    # ------------------------------------------------------------
    # solo si tiene más de una moneda la cuenta
    # IBAN.text = t[403:437].strip()
    # Ccy = etree.SubElement(CdtrAcct, "Ccy")
    # Ccy.text = "EUR"
    # ------------------------------------------------------------
    CdtrAgt = etree.SubElement(PmtInf, "CdtrAgt")
    FinInstnId = etree.SubElement(CdtrAgt, "FinInstnId")
    BIC = etree.SubElement(FinInstnId, "BIC")
    BIC.text = cabecera[8].strip()
    # ChrgBr = etree.SubElement(PmtInf, "ChrgBr")
    # ChrgBr.text = "SLEV"
    CdtrSchmeId = etree.SubElement(PmtInf, "CdtrSchmeId")
    Id = etree.SubElement(CdtrSchmeId, "Id")
    PrvtId = etree.SubElement(Id, "PrvtId")
    Othr = etree.SubElement(PrvtId, "Othr")
    Id = etree.SubElement(Othr, "Id")
    Id.text = cabecera[6].strip()
    SchmeNm = etree.SubElement(Othr, "SchmeNm")
    Prtry = etree.SubElement(SchmeNm, "Prtry")
    Prtry.text = "SEPA"


def parseardetalle03mismovto(t):
    # DrctDbtTxInf = etree.SubElement(PmtInf, "DrctDbtTxInf")
    PmtId = etree.SubElement(DrctDbtTxInf, "PmtId")
    InstrId = etree.SubElement(PmtId, "InstrId")
    InstrId.text = t[26:40] + "-" + t[40:45]
    EndToEndId = etree.SubElement(PmtId, "EndToEndId")
    EndToEndId.text = t[10:45].strip()
    InstdAmt = etree.SubElement(DrctDbtTxInf, "InstdAmt")  # Anyadir Ccy = "EUR"
    InstdAmt.set("Ccy", "EUR")
    # convierte el importe en float sin decimiales
    # importe = "{:.0f}".format(float(t[88:99].strip()))
    # calcula la longitud del importe
    # limporte = len(importe)
    # dos ultimas posiciones para los decimales, el resto parte entera y . decimal
    # importe = importe[0:limporte-2] + "." + importe[limporte-2:limporte]
    # InstdAmt.text = importe
    # InstdAmt.text = t[88:99].strip()
    InstdAmt.text = conviertenumero(t[88:99].strip(), 2)

    DrctDbtTx = etree.SubElement(DrctDbtTxInf, "DrctDbtTx")
    MndtRltdInf = etree.SubElement(DrctDbtTx, "MndtRltdInf")
    MndtId = etree.SubElement(MndtRltdInf, "MndtId")
    MndtId.text = t[45:54].strip()
    DtOfSgntr = etree.SubElement(MndtRltdInf, "DtOfSgntr")
    DtOfSgntr.text = t[99:103] + "-" + t[103:105] + "-" + t[105:107]
    AmdmntInd = etree.SubElement(MndtRltdInf, "AmdmntInd")
    AmdmntInd.text = "false"
    DbtrAgt = etree.SubElement(DrctDbtTxInf, "DbtrAgt")
    FinInstnId = etree.SubElement(DbtrAgt, "FinInstnId")
    BIC = etree.SubElement(FinInstnId, "BIC")
    vbic = t[581:592]
    if not vbic.strip():
        vbic = "NOTPROVIDED"
    BIC.text = vbic
    Dbtr = etree.SubElement(DrctDbtTxInf, "Dbtr")
    Nm = etree.SubElement(Dbtr, "Nm")
    Nm.text = t[118:188].strip()
    # --------------------------------------------------------------
    # DESACTIVADO PARA QUE NO CARGUE LA DIRECCION
    # PstlAdr = etree.SubElement(Dbtr, "PstlAdr")
    # Ctry = etree.SubElement(PstlAdr, "Ctry")
    # Ctry.text = t[328:330].strip()
    # AdrLine = etree.SubElement(PstlAdr, "AdrLine")
    # AdrLine.text = t[188:238].strip()
    # ---------------------------------------------------------------
    DbtrAcct = etree.SubElement(DrctDbtTxInf, "DbtrAcct")
    Id = etree.SubElement(DbtrAcct, "Id")
    IBAN = etree.SubElement(Id, "IBAN")
    IBAN.text = t[403:437].strip()
    RmtInf = etree.SubElement(DrctDbtTxInf, "RmtInf")
    Ustrd = etree.SubElement(RmtInf, "Ustrd")
    Ustrd.text = t[441:581].strip()


print ("==============================================================")
print ("==  Aplicacion creada por Antonio Vila Juan en Python 3.40  ==")
print ("==  INICIO APLICACION PARA GENERAR FICHERO XML A PARTIR     ==")
print ("==  DE UN TXT (TEXTO PLANO)                                 ==")
print ("==  Lee el fichero de remesa sepa en txt y lo convierte     ==")
print ("==  segun disenyo de BCE a xml                              ==")
print ("==  Si tienes alguna duda visita www.avjsite.com            ==")
print ("==  encontraras tutoriales de como funciona el pgm          ==")
print ("==============================================================")
# Cargo el nombre del fichero txt
fichero = sys.argv[1]

# Inicializo el array
cabecera = [""] * 17

# Inicializo la variable root que es la que almacenara todo el xml
xsi = "http://www.w3.org/2001/XMLSchema-instance"
xmlns = "urn:iso:std:iso:20022:tech:xsd:pain.008.001.02"
ns = {"xsi": xsi}
root = etree.Element("Document", nsmap=ns)
# root = etree.Element("Document",)
# root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
root.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.02')

CstmrPmtRvsl = etree.SubElement(root, "CstmrDrctDbtInitn")

# Abro el fichero para leer la primera vez
f = open(fichero)
lines = f.readlines()

# ------------------------------------------------------------------------------
# Leo las lineas una a una la primera vez para cargar la cabecera
# ------------------------------------------------------------------------------
for l in lines:
    if l[:2] == "01":
        cargararraycabecera01(l)
    elif l[:2] == '02':
        cargararraycabecera02(l)
    elif l[:2] == '99':
        parseartotal99(l)
# Leo las lineas una a una la primera vez para cargar la cabecera

# Muevo los datos del array a xml
parsearcabecera01()
# Abro el fichero para leer la segunda vez
f = open(fichero)
lines = f.readlines()
# ------------------------------------------------------------------------------
# Leo las lineas una a una la segunda vez para grabar el detalle
# ------------------------------------------------------------------------------
# creo un switch para que solo entre en parseardetalle03 cabecera una vez, el resto entrara en parseardetalle03mismovto
entraendetalle = 0
for l in lines:
    if l[:2] == '03':
        if entraendetalle == 0:
            entraendetalle = 1
            # se añade esta linea para poder iniciar el xml en parseardetalle03mismovto
            PmtInf = etree.SubElement(CstmrPmtRvsl, "PmtInf")
            parseardetalle03(l)
        if entraendetalle == 1:
            # se añade esta linea para poder iniciar el xml en parseardetalle03mismovto
            DrctDbtTxInf = etree.SubElement(PmtInf, "DrctDbtTxInf")
            parseardetalle03mismovto(l)
# Leo las lineas una a una la segunda vez para grabar el detalle


# Grabar el fichero de salida xml
tree = etree.ElementTree(root)

# Creo el nombre del fichero de salida.
t = fichero.split(os.sep)
fset = t[len(t) - 1].split('.')
fse = fset[0]

ruta_salida = ""
for i in range(len(t) - 1):
    ruta_salida = ruta_salida + t[i] + chr(92)

salida = ruta_salida + fse + ".xml"

tree.write(salida, pretty_print=True, encoding='utf-8', xml_declaration=True)

ruta_temporal = ruta_salida + "Tmp" + chr(92)
# Se crea el directorio para almacenar los ficheros en texto plano.
if (os.path.isdir(ruta_temporal)):
    print ("exite tmp")
else:
    print ("no existe el directorio tmp")
    os.mkdir(ruta_temporal)
# Cerramos el fichero f.
f.close()

# mueve el fichero txt a tmp
shutil.move(fichero, ruta_temporal + t[len(t) - 1])