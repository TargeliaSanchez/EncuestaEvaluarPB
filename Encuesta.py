import streamlit as st
import pandas as pd
from datetime import datetime
import uuid  # Para generar IDs únicos
#import openpyxl
from datetime import date
import json

# Lista de nombres de variables en el orden deseado
orden_columnas = [
    "fecha", "departamento", "municipio", "nombre_institucion", "nit", "nombre_responsable",
    "naturaleza_juridica", "empresa_social_estado", "nivel_atencion_prestador",
    "servicio_1", "servicio_2", "servicio_3", "servicio_4", "servicio_5", "servicio_6", "servicio_7",
    # Agrega aquí el resto de keys que quieras guardar y su orden
]

# Inicializar un diccionario para almacenar los valores de los widgets con key, en el orden deseado
def extraer_variables_con_key_ordenado():
    data = {}
    for key in orden_columnas:
        if key in st.session_state:
            data[key] = st.session_state[key]
        else:
            data[key] = None
    return data

# Crear un DataFrame vacío al inicio (puedes usarlo para almacenar varias respuestas si lo deseas)
if "df_respuestas" not in st.session_state:
    st.session_state.df_respuestas = pd.DataFrame(columns=orden_columnas)

# Ejemplo de uso: para obtener los datos actuales en un DataFrame
# df_actual = pd.DataFrame([extraer_variables_con_key_ordenado()], columns=orden_columnas)

st.markdown("""
<style>
.vertical-divider {
    border-left: 1px solid #ccc;
    padding-left: 14px;
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
    <style>
        .main .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

#st.set_page_config(layout="wide")  # Esto ayuda un poco pero no siempre es suficiente
# Supón que ya tienes tu diccionario "dimensiones" definido
# --- Estilos CSS ---
st.markdown("""
<style>
    .question {
        padding: 0.2rem 0;
        border-bottom: 1px solid #eee; 
    }
    .question-number {
        font-weight: bold;
        color: #2a9d8f;
    }
    .section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .section-title {
        color: #264653;
        font-weight: 500;
        font-size: 0.1rem;
        margin: 0.1rem 0 0.25rem 0 !important;
    }
    .subsection-title {
        color: #2a9d8f;
        font-weight: 500;
        margin: 0.5rem 0 0.5rem 0;
        font-size: 1.1rem;
        margin-bottom: 0.5rem !important;
    }
    .rating-tag {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
        vertical-align: middle;
        font-weight: bold;
    }
    .nav-buttons {
        display: flex;
        justify-content: space-between;
        margin-top: 0.1rem;
    }
    .progress-container {
        margin: 0.1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Ajusta el ancho de los selectbox y las columnas para que preguntas y opciones estén más cerca
# Añade una línea horizontal para delimitar cada pregunta/opción
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 700px;
    }
    .stTextArea textarea {
        min-height: 100px;
    }
    html, body, [class*="css"]  {
        font-size: 9px !important;
    }
    .section-title, .subsection-title, .question, .dimension-rating {
        font-size: 2rem !important;
    }
    .stSelectbox label, .stTextArea label {
        font-size: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)


if "alcance" not in st.session_state:
    st.session_state.alcance = "Seleccione"


# Define los pasos para cada alcance
pasos_completo = list(range(1, 35))  # o hasta el paso final que tengas
pasos_basico = [9,10, 12, 13, 14, 15, 19, 20, 23, 24, 26, 27, 28, 32, 34]

if 'historico' not in st.session_state:
    st.session_state.historico = []

# ----------------------------
# INICIALIZAR
# ----------------------------

if 'paso' not in st.session_state:
    st.session_state.paso = 1
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

def guardar_respuesta(key, value):
    st.session_state.respuestas[key] = value

# ----------------------------
# FUNCIONES DE NAVEGACIÓN
# ----------------------------


def siguiente():
    actual = st.session_state.paso

    if actual < 8:
        st.session_state.paso += 1

    elif actual == 8:
        alcance = st.session_state.get("alcance", "Seleccione")
        if alcance == "Seleccione":
            st.warning("Por favor seleccione el alcance antes de continuar.")
            return
        siguiente_paso = pasos_basico[0] if alcance == "Básico" else 9
        st.session_state.paso = siguiente_paso

    else:
        alcance = st.session_state.get("alcance", "Completo")
        pasos = pasos_basico if alcance == "Básico" else pasos_completo
        idx = pasos.index(actual)
        if idx < len(pasos) - 1:
            st.session_state.paso = pasos[idx + 1]


def anterior():
    actual = st.session_state.paso

    if actual <= 8:
        if actual > 1:
            st.session_state.paso -= 1

    else:
        alcance = st.session_state.get("alcance", "Completo")
        pasos = pasos_basico if alcance == "Básico" else pasos_completo
        if actual in pasos:
            idx = pasos.index(actual)
            if idx > 0:
                st.session_state.paso = pasos[idx - 1]

if "departamento" not in st.session_state:
    st.session_state.departamento = ""

if "municipio" not in st.session_state:
    st.session_state.municipio = ""
# Si no se ha inicializado el alcance, establecer un valor por defecto  
if "alcance" not in st.session_state:
    st.session_state.alcance = "Seleccione"
# Si no se ha inicializado el nombre de la institución, establecer un valor por defecto
if "nombre_institucion" not in st.session_state:
    st.session_state.nombre_institucion = ""
# Si no se ha inicializado el NIT, establecer un valor por defecto
if "nit" not in st.session_state:
    st.session_state.nit = ""
# Si no se ha inicializado el nombre del responsable, establecer un valor por defecto
if "nombre_responsable" not in st.session_state:
    st.session_state.nombre_responsable = ""
# Si no se ha inicializado la naturaleza jurídica, establecer un valor por defecto
if "naturaleza_juridica" not in st.session_state:
    st.session_state.naturaleza_juridica = "Seleccione una opción..."
# Si no se ha inicializado la empresa social de estado, establecer un valor por defecto
if "empresa_social_estado" not in st.session_state:
    st.session_state.empresa_social_estado = "Seleccione una opción..."
# Si no se ha inicializado el nivel de atención del prestador, establecer un valor por defecto
if "nivel_atencion_prestador" not in st.session_state:
    st.session_state.nivel_atencion_prestador = "Seleccione una opción..."
# Si no se ha inicializado el servicio 1, establecer un valor por defecto
if "servicio_1" not in st.session_state:
    st.session_state.servicio_1 = "Seleccione"
# Si no se ha inicializado el servicio 2, establecer un valor por defecto
if "servicio_2" not in st.session_state:
    st.session_state.servicio_2 = "Seleccione"


#def siguiente():
    # Para pasos normales
#    st.session_state.paso += 1

                


#def anterior():
#    st.session_state.paso -= 1


opciones = [
    ("Seleccione...", 0),
    ("1 - No cumple", 1),
    ("2 - Incipiente", 2),
    ("3 - Aceptable", 3),
    ("4 - Satisfecho", 4),
    ("5 - Óptimo", 5)
]

unique_id = str(uuid.uuid4())  # genera un ID único aleatorio
guardar_respuesta("unique_id", unique_id)  # Guarda el ID único en el estado de la sesión

####################### título y encabezado #######################

#st.title("EVALUAR – BPS \n  **EVALUACIÓN DE CONDICIONES ESENCIALES DEL ENFOQUE BIOPSICOSOCIAL EN SERVICIOS DE REHABILITACIÓN**")
st.markdown("""
<div style="
    background-color: #FFE066; 
    padding: 1px 8px;
    border-radius: 10px; 
    text-align: center;
    font-weight: bold;
    font-size: 1.2rem;
    line-height: 1.6;
    border: 1px solid #f0c040;
">
    EVALUAR – BPS<br>
    <span style="font-size: 1rem; padding: 1px 3px;">
        EVALUACIÓN DE CONDICIONES ESENCIALES DEL ENFOQUE BIOPSICOSOCIAL EN SERVICIOS DE REHABILITACIÓN
    </span>
</div>
""", unsafe_allow_html=True)

if st.session_state.paso == 1:
#Información de la institución
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 2px 8px;
                border-radius: 3px;
                font-size: 18px;
                font-weight: bold;
                ">
                I. INFORMACIÓN DE LA INSTITUCIÓN
                </div>
                """, unsafe_allow_html=True)


    col1, col2, col3 = st.columns([5, 1, 2])
    with col1:
        st.markdown("""
                <div style="
                background-color: #e8f0fe;
                color: black;
                padding: 2px 8px;
                font-weight: bold;
                border-radius: 0.5px;
                ">
                Diligenciar previo a la visita y validar posteriormente con los delegados de la institución.
                </div>
                """, unsafe_allow_html=True)

        #st.markdown("Diligencias previo a la visita y validar posteriormente con los delegados de la institución.")
    with col2:
    # Alineación vertical + espaciado elegante
        st.markdown('<div style="padding-top: 0.6rem; text-align:right;"><strong>FECHA</strong></div>', unsafe_allow_html=True)
    with col3:
    # Selector de fecha sin etiqueta visible
        fecha=st.date_input("", date.today(), label_visibility="collapsed", key="fecha")
        guardar_respuesta("fecha", fecha)
    
    col1, col2 = st.columns([4,4])
    with col1:
        st.markdown("**DEPARTAMENTO**")
        departamento=st.text_input(
            "DEPARTAMENTO", 
            value=st.session_state.respuestas.get("departamento", ""),
            label_visibility="collapsed", 
            key="departamento"
        )
        guardar_respuesta("departamento", departamento)
    with col2:
        st.markdown("**MUNICIPIO**")
        municipio=st.text_input(
            "MUNICIPIO", 
            value=st.session_state.municipio,
            label_visibility="collapsed", 
            key="municipio"
        )
        guardar_respuesta("municipio", municipio)

    
    col1,col2 = st.columns([4, 2])
    with col1:
        st.markdown("**INSTITUCIÓN PRESTADORA DE SERVIVIOS DE SALUD**")
        st.text_input("INSTITUCIÓN", "",placeholder="Digite nombre completo del prestador", label_visibility="collapsed",key="nombre_institucion")
        guardar_respuesta("nombre_institucion", st.session_state.nombre_institucion)
    with col2:
        st.markdown("**NIT**")
        st.text_input("NIT", "", placeholder="Digite número-DV", label_visibility="collapsed",key="nombre_responsable")
        guardar_respuesta("nit", st.session_state.nit)
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.markdown("**NATURALEZA JURÍDICA**")
        st.selectbox("",[("Seleccione una opción...",0),("Pública",1),("Privada",2),("Mixta",3)], format_func=lambda x: x[0], key="naturaleza_juridica")
        guardar_respuesta("naturaleza_juridica", st.session_state.naturaleza_juridica)
    with col2:
        st.markdown("**EMPRESA SOCIAL DE ESTADO**")
        st.selectbox("",[("Seleccione una opción...",0),("Si",1),("No",2)], format_func=lambda x: x[0], key="empresa_social_estado")
        guardar_respuesta("empresa_social_estado", st.session_state.empresa_social_estado)
    with col3:
        st.markdown("**NIVEL DE ATENCIÓN DEL PRESTADOR**")
        st.selectbox("",[("Seleccione una opción...",0),("1",1),("2",2),("3",3)], format_func=lambda x: x[0], key="nivel_atencion_prestador")
        guardar_respuesta("nivel_atencion_prestador", st.session_state.nivel_atencion_prestador)
    st.markdown('</div>', unsafe_allow_html=True)
    

    col1, col2= st.columns([5, 1])

    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


#--------------------------------11111111111

elif st.session_state.paso == 2:

#Información de la institución
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 18px;
                font-weight: bold;
                ">
                II. OFERTA DE SERVICIOS DE REHABILITACIÓN
                </div>
                """, unsafe_allow_html=True)    
    
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 2px 8px;
                font-weight: bold;
                border-radius: 0.5px;
                ">
                Diligenciar con los delegados de la institución.
                </div>
                
                <div style="padding: 8px; border: 1px solid #ccc; font-size: 7.2px;">
                <p><strong>DÍAS DE ATENCIÓN</strong> &nbsp; L: lunes &nbsp; M: martes &nbsp; Mi: miércoles &nbsp; J: jueves &nbsp; V: viernes &nbsp; S: sábado &nbsp; D: domingo</p><p><strong>ÁREA DE ATENCIÓN</strong> &nbsp; CE: Consulta externa &nbsp; HOS: Hospitalización &nbsp; UR: Urgencias &nbsp; UCI: Unidad de Cuidado Intensivo &nbsp; Qt: Otra área</p>
                <p><strong>MODALIDADES DE PRESTACIÓN</strong> &nbsp; AMB: Ambulatoria &nbsp; HOSP: Hospitalaria &nbsp; DOM: Domiciliaria &nbsp; JORN: Jornada de Salud &nbsp; UN.MOV: Unidad Móvil &nbsp; TM-IA: Telemedicina interactiva &nbsp; TM-NIA: Telemedicina no interactiva</p>
                <p><strong>TE:</strong> Teleexperticia &nbsp; <strong>TMO:</strong> Telemonitoreo</p>
                <p><strong>PRESTADOR DE TELEMEDICINA</strong> &nbsp; P.REM: Prestador remisior &nbsp; P.REF: Prestador de referencia</p>
                </div>
                """, unsafe_allow_html=True)

    #col_servicio, 
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 1. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_1 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_1"
    )   
    guardar_respuesta("servicio_1", servicio_1)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
# Columna 2: Días de atención
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_1 = st.checkbox("", key="L_1")
            guardar_respuesta("dia_L_1", dia_L_1)
        with col2:
            st.markdown(f"**M**")
            dia_M_1 = st.checkbox("", key="M_1")
            guardar_respuesta("dia_M_1", dia_M_1)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_1 = st.checkbox("", key="Mi_1")
            guardar_respuesta("dia_Mi_1", dia_Mi_1)
        with col4:
            st.markdown(f"**J**")
            dia_J_1 = st.checkbox("", key="J_1")
            guardar_respuesta("dia_J_1", dia_J_1)
        with col5:
            st.markdown(f"**V**")
            dia_V_1 = st.checkbox("", key="V_1")
            guardar_respuesta("dia_V_1", dia_V_1)
        with col6:
            st.markdown(f"**S**")
            dia_S_1 = st.checkbox("", key="S_1")
            guardar_respuesta("dia_S_1", dia_S_1)
        with col7:
            st.markdown(f"**D**")
            dia_D_1 = st.checkbox("", key="D_1")
            guardar_respuesta("dia_D_1", dia_D_1)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
# Columna 3: Áreas asistenciales
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_1 = st.checkbox("", key="CE_1")
            guardar_respuesta("area_CE_1", area_CE_1)
        with col2:
            st.markdown("**HO**")
            area_HO_1 = st.checkbox("", key="HO_1")
            guardar_respuesta("area_HO_1", area_HO_1)
        with col3:
            st.markdown("**UR**")
            area_UR_1 = st.checkbox("", key="UR_1")
            guardar_respuesta("area_UR_1", area_UR_1)
        with col4:
            st.markdown("**U**")
            area_U_1 = st.checkbox("", key="U_1")
            guardar_respuesta("area_U_1", area_U_1)
        with col5:
            st.markdown("**UCI**")
            area_UCI_1 = st.checkbox("", key="UCI_1")
            guardar_respuesta("area_UCI_1", area_UCI_1)
        with col6:
            st.markdown("**Otr**")
            area_Otr_1 = st.checkbox("", key="Otr_1")
            guardar_respuesta("area_Otr_1", area_Otr_1)
        with sep2:
            st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 4: Modalidades
        with col_modalidades:
            st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
            st.markdown("Marque con X  las modalidades habilitadas")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Intramural**")
                mod_AMB_1 = st.checkbox("AMB", key="AMB_1")
                guardar_respuesta("mod_AMB_1", mod_AMB_1)
                mod_HOS_1 = st.checkbox("HOS", key="HOS_1")
                guardar_respuesta("mod_HOS_1", mod_HOS_1)

        with col2:
            st.markdown("**Extramural**")
            mod_DOM_1 = st.checkbox("DOM", key="DOM_1")
            guardar_respuesta("mod_DOM_1", mod_DOM_1)
            mod_JORN_1 = st.checkbox("JORN", key="JORN_1")
            guardar_respuesta("mod_JORN_1", mod_JORN_1)
            mod_UNMOV_1 = st.checkbox("UN.MOV", key="UNMOV_1")
            guardar_respuesta("mod_UNMOV_1", mod_UNMOV_1)

        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_1 = st.checkbox("TM-IA", key="TMIA_1")
            guardar_respuesta("mod_TMIA_1", mod_TMIA_1)
            mod_TMNIA_1 = st.checkbox("TM-NIA", key="TMNIA_1")
            guardar_respuesta("mod_TMNIA_1", mod_TMNIA_1)
            mod_TE_1 = st.checkbox("TE", key="TE_1")
            guardar_respuesta("mod_TE_1", mod_TE_1)
            mod_TMO_1 = st.checkbox("TMO", key="TMO_1")
            guardar_respuesta("mod_TMO_1", mod_TMO_1)
        with sep3:
            st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 5: Prestador
        with col_prestador:
            st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
            st.markdown("marque con una X el tipo de prestador")
            prestador_1 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_1")
            guardar_respuesta("prestador_1", prestador_1)


    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

elif st.session_state.paso == 3:
    # --------------------- 222222
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 2. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    with st.expander("🔍 Ver respuestas guardadas en esta sección"):
        st.write("**Datos ingresados:**")
        st.json({
            "fecha": st.session_state.respuestas.get("fecha", ""),
            "Departamento": st.session_state.respuestas.get("departamento", ""),
            "Municipio": st.session_state.respuestas.get("municipio", "")
        })

    servicio_2 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_2"
    )   
    guardar_respuesta("servicio_2", servicio_2)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    # Columna 2: Días de atención
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_2 = st.checkbox("", key="L_2")
            guardar_respuesta("dia_L_2", dia_L_2)
        with col2:
            st.markdown(f"**M**")
            dia_M_2 = st.checkbox("", key="M_2")
            guardar_respuesta("dia_M_2", dia_M_2)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_2 = st.checkbox("", key="Mi_2")
            guardar_respuesta("dia_Mi_2", dia_Mi_2)
        with col4:
            st.markdown(f"**J**")
            dia_J_2 = st.checkbox("", key="J_2")
            guardar_respuesta("dia_J_2", dia_J_2)
        with col5:
            st.markdown(f"**V**")
            dia_V_2 = st.checkbox("", key="V_2")
            guardar_respuesta("dia_V_2", dia_V_2)
        with col6:
            st.markdown(f"**S**")
            dia_S_2 = st.checkbox("", key="S_2")
            guardar_respuesta("dia_S_2", dia_S_2)
        with col7:
            st.markdown(f"**D**")
            dia_D_2 = st.checkbox("", key="D_2")
            guardar_respuesta("dia_D_2", dia_D_2)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 3: Áreas asistenciales
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_2 = st.checkbox("", key="CE_2")
            guardar_respuesta("area_CE_2", area_CE_2)
        with col2:
            st.markdown("**HO**")
            area_HO_2 = st.checkbox("", key="HO_2")
            guardar_respuesta("area_HO_2", area_HO_2)
        with col3:
            st.markdown("**UR**")
            area_UR_2 = st.checkbox("", key="UR_2")
            guardar_respuesta("area_UR_2", area_UR_2)
        with col4:
            st.markdown("**U**")
            area_U_2 = st.checkbox("", key="U_2")
            guardar_respuesta("area_U_2", area_U_2)
        with col5:
            st.markdown("**UCI**")
            area_UCI_2 = st.checkbox("", key="UCI_2")
            guardar_respuesta("area_UCI_2", area_UCI_2)
        with col6:
            st.markdown("**Otr**")
            area_Otr_2 = st.checkbox("", key="Otr_2")
            guardar_respuesta("area_Otr_2", area_Otr_2)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 4: Modalidades
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_2 = st.checkbox("AMB", key="AMB_2")
            guardar_respuesta("mod_AMB_2", mod_AMB_2)
            mod_HOS_2 = st.checkbox("HOS", key="HOS_2")
            guardar_respuesta("mod_HOS_2", mod_HOS_2)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_2 = st.checkbox("DOM", key="DOM_2")
            guardar_respuesta("mod_DOM_2", mod_DOM_2)
            mod_JORN_2 = st.checkbox("JORN", key="JORN_2")
            guardar_respuesta("mod_JORN_2", mod_JORN_2)
            mod_UNMOV_2 = st.checkbox("UN.MOV", key="UNMOV_2")
            guardar_respuesta("mod_UNMOV_2", mod_UNMOV_2)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_2 = st.checkbox("TM-IA", key="TMIA_2")
            guardar_respuesta("mod_TMIA_2", mod_TMIA_2)
            mod_TMNIA_2 = st.checkbox("TM-NIA", key="TMNIA_2")
            guardar_respuesta("mod_TMNIA_2", mod_TMNIA_2)
            mod_TE_2 = st.checkbox("TE", key="TE_2")
            guardar_respuesta("mod_TE_2", mod_TE_2)
            mod_TMO_2 = st.checkbox("TMO", key="TMO_2")
            guardar_respuesta("mod_TMO_2", mod_TMO_2)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 5: Prestador
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_2 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_2")
        guardar_respuesta("prestador_2", prestador_2)

    # --------------------- 333333
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 3. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_3 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_3"
    )   
    guardar_respuesta("servicio_3", servicio_3)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_3 = st.checkbox("", key="L_3")
            guardar_respuesta("dia_L_3", dia_L_3)
        with col2:
            st.markdown(f"**M**")
            dia_M_3 = st.checkbox("", key="M_3")
            guardar_respuesta("dia_M_3", dia_M_3)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_3 = st.checkbox("", key="Mi_3")
            guardar_respuesta("dia_Mi_3", dia_Mi_3)
        with col4:
            st.markdown(f"**J**")
            dia_J_3 = st.checkbox("", key="J_3")
            guardar_respuesta("dia_J_3", dia_J_3)
        with col5:
            st.markdown(f"**V**")
            dia_V_3 = st.checkbox("", key="V_3")
            guardar_respuesta("dia_V_3", dia_V_3)
        with col6:
            st.markdown(f"**S**")
            dia_S_3 = st.checkbox("", key="S_3")
            guardar_respuesta("dia_S_3", dia_S_3)
        with col7:
            st.markdown(f"**D**")
            dia_D_3 = st.checkbox("", key="D_3")
            guardar_respuesta("dia_D_3", dia_D_3)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_3 = st.checkbox("", key="CE_3")
            guardar_respuesta("area_CE_3", area_CE_3)
        with col2:
            st.markdown("**HO**")
            area_HO_3 = st.checkbox("", key="HO_3")
            guardar_respuesta("area_HO_3", area_HO_3)
        with col3:
            st.markdown("**UR**")
            area_UR_3 = st.checkbox("", key="UR_3")
            guardar_respuesta("area_UR_3", area_UR_3)
        with col4:
            st.markdown("**U**")
            area_U_3 = st.checkbox("", key="U_3")
            guardar_respuesta("area_U_3", area_U_3)
        with col5:
            st.markdown("**UCI**")
            area_UCI_3 = st.checkbox("", key="UCI_3")
            guardar_respuesta("area_UCI_3", area_UCI_3)
        with col6:
            st.markdown("**Otr**")
            area_Otr_3 = st.checkbox("", key="Otr_3")
            guardar_respuesta("area_Otr_3", area_Otr_3)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_3 = st.checkbox("AMB", key="AMB_3")
            guardar_respuesta("mod_AMB_3", mod_AMB_3)
            mod_HOS_3 = st.checkbox("HOS", key="HOS_3")
            guardar_respuesta("mod_HOS_3", mod_HOS_3)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_3 = st.checkbox("DOM", key="DOM_3")
            guardar_respuesta("mod_DOM_3", mod_DOM_3)
            mod_JORN_3 = st.checkbox("JORN", key="JORN_3")
            guardar_respuesta("mod_JORN_3", mod_JORN_3)
            mod_UNMOV_3 = st.checkbox("UN.MOV", key="UNMOV_3")
            guardar_respuesta("mod_UNMOV_3", mod_UNMOV_3)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_3 = st.checkbox("TM-IA", key="TMIA_3")
            guardar_respuesta("mod_TMIA_3", mod_TMIA_3)
            mod_TMNIA_3 = st.checkbox("TM-NIA", key="TMNIA_3")
            guardar_respuesta("mod_TMNIA_3", mod_TMNIA_3)
            mod_TE_3 = st.checkbox("TE", key="TE_3")
            guardar_respuesta("mod_TE_3", mod_TE_3)
            mod_TMO_3 = st.checkbox("TMO", key="TMO_3")
            guardar_respuesta("mod_TMO_3", mod_TMO_3)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_3 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_3")
        guardar_respuesta("prestador_3", prestador_3)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

elif st.session_state.paso == 4:
    # --------------------- 444444
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 4. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_4 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_4"
    )   
    guardar_respuesta("servicio_4", servicio_4)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_4 = st.checkbox("", key="L_4")
            guardar_respuesta("dia_L_4", dia_L_4)
        with col2:
            st.markdown(f"**M**")
            dia_M_4 = st.checkbox("", key="M_4")
            guardar_respuesta("dia_M_4", dia_M_4)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_4 = st.checkbox("", key="Mi_4")
            guardar_respuesta("dia_Mi_4", dia_Mi_4)
        with col4:
            st.markdown(f"**J**")
            dia_J_4 = st.checkbox("", key="J_4")
            guardar_respuesta("dia_J_4", dia_J_4)
        with col5:
            st.markdown(f"**V**")
            dia_V_4 = st.checkbox("", key="V_4")
            guardar_respuesta("dia_V_4", dia_V_4)
        with col6:
            st.markdown(f"**S**")
            dia_S_4 = st.checkbox("", key="S_4")
            guardar_respuesta("dia_S_4", dia_S_4)
        with col7:
            st.markdown(f"**D**")
            dia_D_4 = st.checkbox("", key="D_4")
            guardar_respuesta("dia_D_4", dia_D_4)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_4 = st.checkbox("", key="CE_4")
            guardar_respuesta("area_CE_4", area_CE_4)
        with col2:
            st.markdown("**HO**")
            area_HO_4 = st.checkbox("", key="HO_4")
            guardar_respuesta("area_HO_4", area_HO_4)
        with col3:
            st.markdown("**UR**")
            area_UR_4 = st.checkbox("", key="UR_4")
            guardar_respuesta("area_UR_4", area_UR_4)
        with col4:
            st.markdown("**U**")
            area_U_4 = st.checkbox("", key="U_4")
            guardar_respuesta("area_U_4", area_U_4)
        with col5:
            st.markdown("**UCI**")
            area_UCI_4 = st.checkbox("", key="UCI_4")
            guardar_respuesta("area_UCI_4", area_UCI_4)
        with col6:
            st.markdown("**Otr**")
            area_Otr_4 = st.checkbox("", key="Otr_4")
            guardar_respuesta("area_Otr_4", area_Otr_4)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_4 = st.checkbox("AMB", key="AMB_4")
            guardar_respuesta("mod_AMB_4", mod_AMB_4)
            mod_HOS_4 = st.checkbox("HOS", key="HOS_4")
            guardar_respuesta("mod_HOS_4", mod_HOS_4)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_4 = st.checkbox("DOM", key="DOM_4")
            guardar_respuesta("mod_DOM_4", mod_DOM_4)
            mod_JORN_4 = st.checkbox("JORN", key="JORN_4")
            guardar_respuesta("mod_JORN_4", mod_JORN_4)
            mod_UNMOV_4 = st.checkbox("UN.MOV", key="UNMOV_4")
            guardar_respuesta("mod_UNMOV_4", mod_UNMOV_4)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_4 = st.checkbox("TM-IA", key="TMIA_4")
            guardar_respuesta("mod_TMIA_4", mod_TMIA_4)
            mod_TMNIA_4 = st.checkbox("TM-NIA", key="TMNIA_4")
            guardar_respuesta("mod_TMNIA_4", mod_TMNIA_4)
            mod_TE_4 = st.checkbox("TE", key="TE_4")
            guardar_respuesta("mod_TE_4", mod_TE_4)
            mod_TMO_4 = st.checkbox("TMO", key="TMO_4")
            guardar_respuesta("mod_TMO_4", mod_TMO_4)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_4 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_4")
        guardar_respuesta("prestador_4", prestador_4)

#if st.session_state.paso == 5:
    # --------------------- 555555
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 5. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_5 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_5"
    )   
    guardar_respuesta("servicio_5", servicio_5)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_5 = st.checkbox("", key="L_5")
            guardar_respuesta("dia_L_5", dia_L_5)
        with col2:
            st.markdown(f"**M**")
            dia_M_5 = st.checkbox("", key="M_5")
            guardar_respuesta("dia_M_5", dia_M_5)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_5 = st.checkbox("", key="Mi_5")
            guardar_respuesta("dia_Mi_5", dia_Mi_5)
        with col4:
            st.markdown(f"**J**")
            dia_J_5 = st.checkbox("", key="J_5")
            guardar_respuesta("dia_J_5", dia_J_5)
        with col5:
            st.markdown(f"**V**")
            dia_V_5 = st.checkbox("", key="V_5")
            guardar_respuesta("dia_V_5", dia_V_5)
        with col6:
            st.markdown(f"**S**")
            dia_S_5 = st.checkbox("", key="S_5")
            guardar_respuesta("dia_S_5", dia_S_5)
        with col7:
            st.markdown(f"**D**")
            dia_D_5 = st.checkbox("", key="D_5")
            guardar_respuesta("dia_D_5", dia_D_5)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_5 = st.checkbox("", key="CE_5")
            guardar_respuesta("area_CE_5", area_CE_5)
        with col2:
            st.markdown("**HO**")
            area_HO_5 = st.checkbox("", key="HO_5")
            guardar_respuesta("area_HO_5", area_HO_5)
        with col3:
            st.markdown("**UR**")
            area_UR_5 = st.checkbox("", key="UR_5")
            guardar_respuesta("area_UR_5", area_UR_5)
        with col4:
            st.markdown("**U**")
            area_U_5 = st.checkbox("", key="U_5")
            guardar_respuesta("area_U_5", area_U_5)
        with col5:
            st.markdown("**UCI**")
            area_UCI_5 = st.checkbox("", key="UCI_5")
            guardar_respuesta("area_UCI_5", area_UCI_5)
        with col6:
            st.markdown("**Otr**")
            area_Otr_5 = st.checkbox("", key="Otr_5")
            guardar_respuesta("area_Otr_5", area_Otr_5)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_5 = st.checkbox("AMB", key="AMB_5")
            guardar_respuesta("mod_AMB_5", mod_AMB_5)
            mod_HOS_5 = st.checkbox("HOS", key="HOS_5")
            guardar_respuesta("mod_HOS_5", mod_HOS_5)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_5 = st.checkbox("DOM", key="DOM_5")
            guardar_respuesta("mod_DOM_5", mod_DOM_5)
            mod_JORN_5 = st.checkbox("JORN", key="JORN_5")
            guardar_respuesta("mod_JORN_5", mod_JORN_5)
            mod_UNMOV_5 = st.checkbox("UN.MOV", key="UNMOV_5")
            guardar_respuesta("mod_UNMOV_5", mod_UNMOV_5)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_5 = st.checkbox("TM-IA", key="TMIA_5")
            guardar_respuesta("mod_TMIA_5", mod_TMIA_5)
            mod_TMNIA_5 = st.checkbox("TM-NIA", key="TMNIA_5")
            guardar_respuesta("mod_TMNIA_5", mod_TMNIA_5)
            mod_TE_5 = st.checkbox("TE", key="TE_5")
            guardar_respuesta("mod_TE_5", mod_TE_5)
            mod_TMO_5 = st.checkbox("TMO", key="TMO_5")
            guardar_respuesta("mod_TMO_5", mod_TMO_5)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_5 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_5")
        guardar_respuesta("prestador_5", prestador_5)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)
    

elif st.session_state.paso == 5:
    # --------------------- 666666
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 6. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_6 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_6"
    )   
    guardar_respuesta("servicio_6", servicio_6)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_6 = st.checkbox("", key="L_6")
            guardar_respuesta("dia_L_6", dia_L_6)
        with col2:
            st.markdown(f"**M**")
            dia_M_6 = st.checkbox("", key="M_6")
            guardar_respuesta("dia_M_6", dia_M_6)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_6 = st.checkbox("", key="Mi_6")
            guardar_respuesta("dia_Mi_6", dia_Mi_6)
        with col4:
            st.markdown(f"**J**")
            dia_J_6 = st.checkbox("", key="J_6")
            guardar_respuesta("dia_J_6", dia_J_6)
        with col5:
            st.markdown(f"**V**")
            dia_V_6 = st.checkbox("", key="V_6")
            guardar_respuesta("dia_V_6", dia_V_6)
        with col6:
            st.markdown(f"**S**")
            dia_S_6 = st.checkbox("", key="S_6")
            guardar_respuesta("dia_S_6", dia_S_6)
        with col7:
            st.markdown(f"**D**")
            dia_D_6 = st.checkbox("", key="D_6")
            guardar_respuesta("dia_D_6", dia_D_6)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_6 = st.checkbox("", key="CE_6")
            guardar_respuesta("area_CE_6", area_CE_6)
        with col2:
            st.markdown("**HO**")
            area_HO_6 = st.checkbox("", key="HO_6")
            guardar_respuesta("area_HO_6", area_HO_6)
        with col3:
            st.markdown("**UR**")
            area_UR_6 = st.checkbox("", key="UR_6")
            guardar_respuesta("area_UR_6", area_UR_6)
        with col4:
            st.markdown("**U**")
            area_U_6 = st.checkbox("", key="U_6")
            guardar_respuesta("area_U_6", area_U_6)
        with col5:
            st.markdown("**UCI**")
            area_UCI_6 = st.checkbox("", key="UCI_6")
            guardar_respuesta("area_UCI_6", area_UCI_6)
        with col6:
            st.markdown("**Otr**")
            area_Otr_6 = st.checkbox("", key="Otr_6")
            guardar_respuesta("area_Otr_6", area_Otr_6)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_6 = st.checkbox("AMB", key="AMB_6")
            guardar_respuesta("mod_AMB_6", mod_AMB_6)
            mod_HOS_6 = st.checkbox("HOS", key="HOS_6")
            guardar_respuesta("mod_HOS_6", mod_HOS_6)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_6 = st.checkbox("DOM", key="DOM_6")
            guardar_respuesta("mod_DOM_6", mod_DOM_6)
            mod_JORN_6 = st.checkbox("JORN", key="JORN_6")
            guardar_respuesta("mod_JORN_6", mod_JORN_6)
            mod_UNMOV_6 = st.checkbox("UN.MOV", key="UNMOV_6")
            guardar_respuesta("mod_UNMOV_6", mod_UNMOV_6)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_6 = st.checkbox("TM-IA", key="TMIA_6")
            guardar_respuesta("mod_TMIA_6", mod_TMIA_6)
            mod_TMNIA_6 = st.checkbox("TM-NIA", key="TMNIA_6")
            guardar_respuesta("mod_TMNIA_6", mod_TMNIA_6)
            mod_TE_6 = st.checkbox("TE", key="TE_6")
            guardar_respuesta("mod_TE_6", mod_TE_6)
            mod_TMO_6 = st.checkbox("TMO", key="TMO_6")
            guardar_respuesta("mod_TMO_6", mod_TMO_6)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_6 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_6")
        guardar_respuesta("prestador_6", prestador_6)

    #st.markdown("----------------------")

    # --------------------- 777777
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> 7. SERVICIOS DE REHABILITACIÓN HABILITADOS 
                </div>
                """, unsafe_allow_html=True)
    servicio_7 = st.selectbox(
        "",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_7"
    )   
    guardar_respuesta("servicio_7", servicio_7)
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_7 = st.checkbox("", key="L_7")
            guardar_respuesta("dia_L_7", dia_L_7)
        with col2:
            st.markdown(f"**M**")
            dia_M_7 = st.checkbox("", key="M_7")
            guardar_respuesta("dia_M_7", dia_M_7)
        with col3:
            st.markdown(f"**X**")
            dia_Mi_7 = st.checkbox("", key="Mi_7")
            guardar_respuesta("dia_Mi_7", dia_Mi_7)
        with col4:
            st.markdown(f"**J**")
            dia_J_7 = st.checkbox("", key="J_7")
            guardar_respuesta("dia_J_7", dia_J_7)
        with col5:
            st.markdown(f"**V**")
            dia_V_7 = st.checkbox("", key="V_7")
            guardar_respuesta("dia_V_7", dia_V_7)
        with col6:
            st.markdown(f"**S**")
            dia_S_7 = st.checkbox("", key="S_7")
            guardar_respuesta("dia_S_7", dia_S_7)
        with col7:
            st.markdown(f"**D**")
            dia_D_7 = st.checkbox("", key="D_7")
            guardar_respuesta("dia_D_7", dia_D_7)
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_7 = st.checkbox("", key="CE_7")
            guardar_respuesta("area_CE_7", area_CE_7)
        with col2:
            st.markdown("**HO**")
            area_HO_7 = st.checkbox("", key="HO_7")
            guardar_respuesta("area_HO_7", area_HO_7)
        with col3:
            st.markdown("**UR**")
            area_UR_7 = st.checkbox("", key="UR_7")
            guardar_respuesta("area_UR_7", area_UR_7)
        with col4:
            st.markdown("**U**")
            area_U_7 = st.checkbox("", key="U_7")
            guardar_respuesta("area_U_7", area_U_7)
        with col5:
            st.markdown("**UCI**")
            area_UCI_7 = st.checkbox("", key="UCI_7")
            guardar_respuesta("area_UCI_7", area_UCI_7)
        with col6:
            st.markdown("**Otr**")
            area_Otr_7 = st.checkbox("", key="Otr_7")
            guardar_respuesta("area_Otr_7", area_Otr_7)
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_7 = st.checkbox("AMB", key="AMB_7")
            guardar_respuesta("mod_AMB_7", mod_AMB_7)
            mod_HOS_7 = st.checkbox("HOS", key="HOS_7")
            guardar_respuesta("mod_HOS_7", mod_HOS_7)
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_7 = st.checkbox("DOM", key="DOM_7")
            guardar_respuesta("mod_DOM_7", mod_DOM_7)
            mod_JORN_7 = st.checkbox("JORN", key="JORN_7")
            guardar_respuesta("mod_JORN_7", mod_JORN_7)
            mod_UNMOV_7 = st.checkbox("UN.MOV", key="UNMOV_7")
            guardar_respuesta("mod_UNMOV_7", mod_UNMOV_7)
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_7 = st.checkbox("TM-IA", key="TMIA_7")
            guardar_respuesta("mod_TMIA_7", mod_TMIA_7)
            mod_TMNIA_7 = st.checkbox("TM-NIA", key="TMNIA_7")
            guardar_respuesta("mod_TMNIA_7", mod_TMNIA_7)
            mod_TE_7 = st.checkbox("TE", key="TE_7")
            guardar_respuesta("mod_TE_7", mod_TE_7)
            mod_TMO_7 = st.checkbox("TMO", key="TMO_7")
            guardar_respuesta("mod_TMO_7", mod_TMO_7)
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_7 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_7")
        guardar_respuesta("prestador_7", prestador_7)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


elif  st.session_state.paso == 6:#Bloque  recursos humanos 1
    #Información de la institución
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 2px 5px;
                border-radius: 3px;
                font-size: 18px;
                font-weight: bold;
                ">
                III. RECURSO HUMANO DE LOS SERVICIOS DE REHABILITACIÓN
                </div>
                """, unsafe_allow_html=True)    
    
    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 2px 8px;
                font-weight: normal;
                border-radius: 0.5px;
                ">
                Registre <b>número de profesionales de los servicios de rehabilitación</b> contratado por la institución en el momento de la verificación 
                </div>
                """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] {
        min-height: 30px;
    }
    input[type="number"], input[type="text"] {
        height: 30px !important;
        font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTextInput, .stSelectbox, .stNumberInput, .stRadio {
        margin-bottom: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns([1,1,1,1])

    with col1:
        DesP_1 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_1"
        )
        guardar_respuesta("DesP_1", DesP_1)
        numero_1 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_1")
        guardar_respuesta("numero_1", numero_1)

        DesP_2 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_2"
        )
        guardar_respuesta("DesP_2", DesP_2)
        numero_2 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_2")
        guardar_respuesta("numero_2", numero_2)
    
    with col2:
        DesP_3 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_3"
        )
        guardar_respuesta("DesP_3", DesP_3)
        numero_3 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_3")
        guardar_respuesta("numero_3", numero_3)
   
        DesP_4 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_4"
        )
        guardar_respuesta("DesP_4", DesP_4)
        numero_4 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_4")
        guardar_respuesta("numero_4", numero_4)
    with col3:
        DesP_5 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_5"
        )
        guardar_respuesta("DesP_5", DesP_5)
        numero_5 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_5")
        guardar_respuesta("numero_5", numero_5)
    
        DesP_6 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_6"
        )
        guardar_respuesta("DesP_6", DesP_6)
        numero_6 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_6")
        guardar_respuesta("numero_6", numero_6)
    with col4:
        DesP_7 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_7"
        )
        guardar_respuesta("DesP_7", DesP_7)
        numero_7 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_7")
        guardar_respuesta("numero_7", numero_7)
   
        DesP_8 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_8"
        )
        guardar_respuesta("DesP_8", DesP_8)
        numero_8 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_8")
        guardar_respuesta("numero_8", numero_8)

    st.markdown("""
    <style>
    .titulo-caja {
        background-color: #cce5f5;
        padding: 8px;
        font-weight: bold;
        border-radius: 5px;
        font-size: 14px;
    }
    .linea {
        margin-top: 8px;
        margin-bottom: 8px;
        border: none;
        border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)
    
    #st.markdown("<hr class='linea'>", unsafe_allow_html=True)

    st.markdown("""
                <div style="
                background-color: #e8f0fe ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                ">
                Registre <b>Registre aclaraciones pertinentes sobre la oferta de servicios de rehabilitación y el talento humano relacionado:</b> variaciones en la disponibilidad de los servicios, otras áreas donde se prestan servicios de rehabilitación. 
                </div>
                """, unsafe_allow_html=True)
    

    aclaraciones = st.text_area("Aclaraciones", height=80, key="aclaraciones")
    guardar_respuesta("aclaraciones", aclaraciones)

    st.markdown("<hr class='linea'>", unsafe_allow_html=True)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

######################## PÁGINA 7 ########################
elif st.session_state.paso == 7:
        #Información de la institución
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 2px 5px;
                border-radius: 3px;
                font-size: 18px;
                font-weight: bold;
                ">
                III. RECURSO HUMANO DE LOS SERVICIOS DE REHABILITACIÓN
                </div>
                """, unsafe_allow_html=True)    
    
    st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] {
        min-height: 30px;
    }
    input[type="number"], input[type="text"] {
        height: 30px !important;
        font-size: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTextInput, .stSelectbox, .stNumberInput, .stRadio {
        margin-bottom: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background-color: white;
        border: 1px solid #ccc;
        padding: 0px 0px;
        margin-bottom: 1px;
        font-weight: bold;
        font-size: 14px;
    ">
        <h0 style='margin: 0; font-weight: bold;'>NOMBRE DE REPRESENTANTES DE LA INSTITUCIÓN [CARGO]</h0>
    </div>
    """, unsafe_allow_html=True)


    for i in range(1, 7):
        rep = st.text_input(
            label="",  # Oculta el texto de la variable
            placeholder=f"{i}. Digite nombre completo [Cargo]",  # Aparece dentro del recuadro
            key=f"rep_inst_{i}"
        )
        guardar_respuesta(f"rep_inst_{i}", rep)

    st.markdown("<hr class='linea'>", unsafe_allow_html=True)


# 🔹 Profesionales responsables de verificación
    st.markdown("""
    <div style="
        background-color: white;
        border: 1px solid #ccc;
        padding: 0px 0px;
        margin-bottom: 1px;
        font-weight: bold;
        font-size: 14px;
    ">
        <h0 style='margin: 0; font-weight: bold;'>NOMBRE DE PROFESIONALES RESPONSABLES DE VERIFICACIÓN</h0>
    </div>
    """, unsafe_allow_html=True)


    for i in range(1, 3):
        prof = st.text_input(
            label="",
            placeholder=f"{i}. Digite nombre completo", 
            key=f"prof_verif_{i}"
        )
        guardar_respuesta(f"prof_verif_{i}", prof)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

##################### FORMULARIO DE EVALUACIÓN #####################
############ PÁGINA 8 #####################
elif st.session_state.paso == 8: # Evaluación de la institución.

    st.markdown("""
    <div style="background-color:#FFD966; padding: 2px 8px; font-weight:bold; border: 2px solid #b7b7b7; border-radius: 8px;">
        <h0>IV. EVALUAR-BPS<h0/>
    </div>

    <div style="background-color:#DEEAF6; padding: 6px 10px; font-style:italic; border: 2px solid #b7b7b7; border-radius: 8px;">
        <p style="margin: 0px;">Los siguientes ítems describen condiciones esenciales de la atención con enfoque biopsicosocial en los servicios de rehabilitación.</em></p>
        <p style="margin: 0px;">Para cada ítem los representantes de la institución deben concertar y seleccionar una respuesta entre las opciones que presenta la <strong>ESCALA DE VALORACIÓN</strong>.</em></p>
        <p style="margin: 0px;">Cada condición se acompaña de cuatro criterios de verificación para orientar la valoración.</em></p>
        <p style="margin: 0px;">Algunas condiciones serán verificadas en fuentes de información disponibles, previa autorización formal de la institución.</em></p>
    </div>

    <div style="margin-top:10px; border: 2px solid #b7b7b7; border-radius: 8px; padding: 1 px 8px;">
        <strong>ESCALA DE VALORACIÓN</strong>
        <ul style="list-style-type: none; padding-left: 0;">
            <p style="margin: 0px;">5.</span> La condición cumple de forma óptima todos los criterios <span style="color:green; font-weight:bold;">▮</span></li>
            <p style="margin: 0px;">4.</span> La condición cumple de forma satisfactoria mínimo tres criterios</li>
            <p style="margin: 0px;">3.</span> La condición cumple de forma aceptable mínimo tres criterios</li>
            <p style="margin: 0px;">2.</span> La condición cumple de forma incipiente uno o dos criterios</li>
            <p style="margin: 0px;">1.</span> La condición no cumple ningún criterio o no se implementa <span style="color:red; font-weight:bold;">▮</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    alcance = st.selectbox(
        "Alcance de la evaluación",
        options=["Seleccione", "Básico", "Completo"],
        key="alcance")
    guardar_respuesta("alcance", alcance)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


elif st.session_state.paso == 9:
# Encabezado principal
    #st.markdown("### D1. ORGANIZACIÓN Y GESTIÓN DE LOS SERVICIOS DE REHABILITACIÓN")

# Descripción de la sección
# Paso 1 - D1.1
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
                ">
                D1.1 La oferta de servicios de rehabilitación corresponde con el nivel de complejidad de la institución.
                </div>
                """, unsafe_allow_html=True)    
    


    #st.markdown("**D1.1 La oferta de servicios de rehabilitación corresponde con el nivel de complejidad de la institución.**")
    preguntas_d11 = [
        "La institución presta servicio de psicología y/o trabajo social.",
        "La institución presta servicios de fisioterapia, fonoaudiología y/o terapia ocupacional.",
        "Los servicios de rehabilitación disponibles corresponden con el nivel de complejidad.",
        "Los servicios de rehabilitación se organizan en un área específica de la institución.",
    ]

    notas_d11 = [
    """Servicios de rehabilitación según nivel de atención del prestador:
    
    - **Nivel 3**: Servicios de nivel II. Los servicios de rehabilitación se organizan en un área (Ej., unidad, departamento).  
    - **Nivel 2**: Medicina general y especialidades. Servicio de medicina física y rehabilitación (interconsulta), 
                   fisioterapia, terapia ocupacional y/o fonoaudiología + psicología.  
    - **Nivel 1**: Medicina general o remisión de prestador externo. Servicios de fisioterapia, fonoaudiología y/o 
                   terapia ocupacional + psicología y/o trabajo social.
    """]

    if notas_d11[0]:
        with st.expander("Nota"):
            st.markdown(notas_d11[0])
    
        
    for i, texto in enumerate(preguntas_d11):
        col1, col2= st.columns([4, 1])
        with col1:
            st.markdown(texto)
    
        with col2:
            val = st.selectbox("",opciones,format_func=lambda x: x[0],key=f"pD11_{i+1}")
            guardar_respuesta(f"pD11_{i+1}", val)

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.1:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_1")
            guardar_respuesta("D1_1", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD11")
            guardar_respuesta("obsD11", obs)


    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


#-------------------------------------------------------------------------------------
# Paso 2 - D1.2
elif st.session_state.paso == 10:

    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.2 El talento humano de rehabilitación vinculado a la institución es acorde a la capacidad instalada versus la demanda de los servicios.
                </div>
                """, unsafe_allow_html=True)    
    
    notas_d12 = [
    """Verificar:

    - Oportunidad de cita o atención.
    - Usuarios atendidos / hora.
    """]

    if notas_d12[0]:
        with st.expander("Nota"):
            st.markdown(notas_d12[0])

    preguntas_d12 = [
        "La institución cuenta con un equipo de rehabilitación multidisciplinario.",
        "El equipo de rehabilitación está conformado por profesionales de diferentes disciplinas.",
        "El equipo de rehabilitación participa en la planificación y ejecución de los tratamientos.",
        "El equipo de rehabilitación realiza reuniones periódicas para evaluar el progreso de los pacientes.",
    ]
    for i, texto in enumerate(preguntas_d12):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD12_{i+1}")
            guardar_respuesta(f"pD12_{i+1}", val)

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.2:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_2")
            guardar_respuesta("D1_2", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD12")
            guardar_respuesta("obsD12", obs)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#-------------------------------------------------------------------------------------
# Paso 3 - D1.3
elif st.session_state.paso == 11:

    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.3 La prestación de los servicios de rehabilitación se realiza en diferentes modalidades: intramural, extramural y/o telemedicina.
                </div>
                """, unsafe_allow_html=True)    
    
    notas_d13 = [
    """ 
    """]

    if notas_d13[0]:
        with st.expander("Nota"):
            st.markdown(notas_d13[0])

    preguntas_d13 = [
        "Se prestan servicios de rehabilitación en modalidad ambulatoria y/o hospitalaria [si aplica esta modalidad].",
        "Se prestan servicios de rehabilitación en modalidad domiciliaria [u otras modalidades extramurales], y están definidos los criterios para la atención en esta[s] modalidad[es].",
        "Se prestan servicios de rehabilitación en la modalidad de telemedicina.",
        "La oferta de servicios en la modalidad de telemedicina incluye una o más especialidades médicas relacionadas con rehabilitación.",
    ]
    for i, texto in enumerate(preguntas_d13):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD13_{i+1}")
            guardar_respuesta(f"pD13_{i+1}", val)

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.3:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_3")
            guardar_respuesta("D1_3", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD13")
            guardar_respuesta("obsD13", obs)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


#-------------------------------------------------------------------------------------
# Paso 4 - D1.4
elif st.session_state.paso == 12:

    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.4 La institución cuenta con un sistema unificado de historia clínica disponible para los profesionales que intervienen en el proceso de rehabilitación.
                </div>
                """, unsafe_allow_html=True)    
    
    notas_d14 = [
        """ Verificar:      

        - Historia clínica.
        - Facilitadores y barreras en la práctica.
    """]


    if notas_d14[0]:
        with st.expander("Nota"):
            st.markdown(notas_d14[0])

    preguntas_d14 = [
        "La institución cuenta con historia clínica electrónica que incluye la información del usuario en las diferentes fases de la atención.", 
        "La historia clínica incluye la atención y procedimientos de los usuarios de rehabilitación, y esta información esta disponible para los profesionales.",
        "La historia clínica está disponible en los servicios de rehabilitación para el registro simultaneo o inmediato de la atención.",
        "La historia clínica incluye contenido y/o formatos específicos para los servicios de rehabilitación.",
        ]
    for i, texto in enumerate(preguntas_d14):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD14_{i+1}")
            guardar_respuesta(f"pD14_{i+1}", val)

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.4:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_4")
            guardar_respuesta("D1_4", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD14")
            guardar_respuesta("obsD14", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


################ Paso 5 - D1.5
if st.session_state.paso == 13:
    st.markdown("""
                <div style="
                background-color: #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.5  La atención de los usuarios de rehabilitación o “proceso de rehabilitación” se encuentra documentado en la institución.
                </div>
                """, unsafe_allow_html=True)    
    
    notas_d15 = [
        """ Verificar: 
        
        Documentos disponibles en Sistema de Gestión de Calidad 
        """]

    if notas_d15[0]:
        with st.expander("Nota"):
            st.markdown(notas_d15[0])

    preguntas_d15 = [
        "Se documentan los servicios de terapias y se describen: modalidades de prestación, actividades, talento humano, infraestructura, dotación, riesgos e indicadores.",
        "Se documenta la atención por rehabilitación como un proceso continuo con un tiempo de duración definido. ",
        "La documentación del proceso de rehabilitación describe los diferentes servicios que intervienen desde la entrada hasta el egreso del usuario. ",
        "El documento del proceso de rehabilitación se encuentra actualizado y disponible en el sistema de gestión de calidad.",
    ]
    for i, texto in enumerate(preguntas_d15):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD15_{i+1}")
            guardar_respuesta(f"pD15_{i+1}", val)

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.5:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_5")
            guardar_respuesta("D1_5", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD15")
            guardar_respuesta("obsD15", obs)

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

################## Paso 6 - D1.6
elif st.session_state.paso == 14:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;   
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.6 El proceso de rehabilitación se estructura por etapas o fases que orientan la atención del usuario en la institución.
                </div>
                """, unsafe_allow_html=True)
    notas_d16 = [
        """ Verificar:
        
        Documentos disponibles. 
        Registros de socialización.
    """]
    if notas_d16[0]:
        with st.expander("Nota"):
            st.markdown(notas_d16[0])
    preguntas_d16 = [
        "En el proceso de rehabilitación se describen los mecanismos de entrada o ingreso del usuario. ",
        "El proceso de rehabilitación se estructura por etapas o fases que orientan la atención:  1. Evaluación inicial;  2. Plan de atención; 3. Intervención y 4. Evaluación final. ",
        "En cada etapa o fase se describe el alcance y las acciones a realizar para el logro de objetivos o metas de rehabilitación.",
        "El proceso de rehabilitación se divulga al personal asistencial de la institución.",
    ]
    for i, texto in enumerate(preguntas_d16):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD16_{i+1}")
            guardar_respuesta(f"pD16_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.6:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_6")
            guardar_respuesta("D1_6", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD16")
            guardar_respuesta("obsD16", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)



################## Paso 7 - D1.7
elif st.session_state.paso == 15:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;    
                font-weight: bold;
                ">
                D1.7 En los servicios de rehabilitación se encuentran disponibles guías de práctica clínica, protocolos de atención y/o procedimientos para orientar la toma de decisiones.
                </div>
                """, unsafe_allow_html=True)
    notas_d17 = [""" Verificar:
                 
                 Protocolos de atención y GPC disponibles.
                 Procedimiento para la elaboración de GPC y protocolos.
                 Registros de socialización de GPC y protocolos.
    """]
    if notas_d17[0]:
        with st.expander("Nota"):
            st.markdown(notas_d17[0])
    preguntas_d17 = [
        "**En los servicios de rehabilitación se encuentran disponibles los protocolos de atención.**",
        "**La institución cuenta con una o más guías de práctica clínica (GPC) específicas para rehabilitación o GPC que integran recomendaciones para rehabilitación.**",
        "**La institución cuenta con un procedimiento que establece la metodología para la elaboración de protocolos y GPC [metodologías: adopción, adaptación o creación].**",
        "**Los protocolos y/o GPC de los servicios de rehabilitación se encuentran actualizados e implementados.**",
    ]
    for i, texto in enumerate(preguntas_d17):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD17_{i+1}")
            guardar_respuesta(f"pD17_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.7:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_7")
            guardar_respuesta("D1_7", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD17")
            guardar_respuesta("obsD17", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:      
        st.button("Siguiente ▶️", on_click=siguiente)

################## Paso 8 - D1.8
elif st.session_state.paso == 16:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.8 La institución estructura e implementa un plan de capacitación en atención o rehabilitación con enfoque biopsicosocial. 
                </div>
                """, unsafe_allow_html=True)
    notas_d18 = ["""Verificar:
    
                 Registro de capacitaciones
                 Contenido de inducción y plan de capacitación
    """]
    if notas_d18[0]:
        with st.expander("Nota"):
            st.markdown(notas_d18[0])
    preguntas_d18 = [   
        "**La inducción de nuevos profesionales incluye información sobre el proceso de atención con enfoque biopsicosocial.**",
        "**La institución realiza capacitaciones periódicas sobre la atención con enfoque biopsicosocial.**",
        "**Las capacitaciones sobre atención con enfoque biopsicosocial están dirigidas al personal asistencial y administrativo. [jefes, coordinadores, personal de mercadeo; RRHH]**",
        "**Se implementan acciones para evaluar el conocimiento del personal sobre la atención con enfoque biopsicosocial.**",
    ]
    for i, texto in enumerate(preguntas_d18):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD18_{i+1}")
            guardar_respuesta(f"pD18_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.8:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_8")
            guardar_respuesta("D1_8", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD18")
            guardar_respuesta("obsD18", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 9 - D1.9
elif st.session_state.paso == 17:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D1.9 La institución cuenta con áreas de atención, dotación y tecnología para la implementación de intervenciones orientadas a optimizar el proceso de rehabilitación. 
                </div>
                """, unsafe_allow_html=True)
    notas_d19 = [
    """ 
    """]
    if notas_d19[0]:
        with st.expander("Nota"):
            st.markdown(notas_d19[0])
    preguntas_d19 = [
        "**Los servicios de rehabilitación cuentan con equipos e insumos adecuados a las necesidades de la población atendida y su condición de salud.**",
        "**La institución realiza mantenimiento periódico y reparación oportuna de áreas, equipos e insumos de rehabilitación.**",
        "**Los servicios de rehabilitación disponen de tecnología que favorecen el acceso, la eficiencia y/o personalización de la atención.**",
        "**La institución cuenta con ambientes especializados para favorecer la autonomía, independencia y el desempeño de roles.**",
    ]
    for i, texto in enumerate(preguntas_d19):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD19_{i+1}")
            guardar_respuesta(f"pD19_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.9:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_9")
            guardar_respuesta("D1_9", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD19")
            guardar_respuesta("obsD19", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)



#################### Paso 10 - D2.1
elif st.session_state.paso == 18:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.1 Se realiza o se cuenta con valoración médica integral de la condición de salud de los usuarios de rehabilitación. 
                </div>
                """, unsafe_allow_html=True)
    notas_d21 = ["""Verificar:
    
                 Historia clínica: valoración médica
    """]
    if notas_d21[0]:
        with st.expander("Nota"):
            st.markdown(notas_d21[0])
    preguntas_d2_1 = [
        "La valoración médica de los usuarios de rehabilitación se encuentra disponible en la historia clínica.",
        "La valoración médica del usuario aborda integralmente la condición de salud para establecer el diagnóstico [diagnóstico principal y dianósticos relacionados]",
        "La información de la valoración médica es pertinente y suficiente para definir los objetivos y el plan de atención por rehabilitación.",
        "La institución cuenta con un formato estandarizado para la valoración médica de los usuarios de rehabilitación.",
    ]
    for i, texto in enumerate(preguntas_d2_1):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_1_{i+1}")
            guardar_respuesta(f"pD2_1_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.1:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_1")
            guardar_respuesta("D2_1", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_1")
            guardar_respuesta("obsD2_1", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 11 - D2.2
elif st.session_state.paso == 19:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.2 Se usan pruebas estandarizadas y/o instrumentos para la evaluación de los usuarios de rehabilitación. ►
                </div>
                """, unsafe_allow_html=True)
    notas_d22 = ["""Verificar:
                 
                 Instrumento[s] de evaluación 
                 Historia clínica
    """]
    if notas_d22[0]:
        with st.expander("Nota"):
            st.markdown(notas_d22[0])
    preguntas_d2_2 = [
        "**Los profesionales de rehabilitación registran en la historia clínica el uso de pruebas y/o instrumentos de evaluación.**",
        "**La institución define criterios para la selección y el uso de pruebas o instrumentos de evaluación de los usuarios de rehabilitación.**",
        "**La institución cuenta con un método desarrollado o adaptado para la evaluación de los usuarios de rehabilitación.**",
        "**Los profesionales hacen uso de  las pruebas o instrumentos disponibles según las caracteristicas y necesidades de los usuarios. [la disponibilidad hace referencia a fácil acceso durante la atención. Ej. en historia clínica]**",
    ]
    for i, texto in enumerate(preguntas_d2_2):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_2_{i+1}")
            guardar_respuesta(f"pD2_2_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.2:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_2")
            guardar_respuesta("D2_2", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_2")
            guardar_respuesta("obsD2_2", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 12 - D2.3
elif st.session_state.paso == 20:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.3 En la evaluación se valora el estado funcional del usuario. ►
                </div>
                """, unsafe_allow_html=True)
    notas_d23 = ["""Verificar:
                 
                 Instrumento[s] de evaluación.
                 Historia clínica.
                 **En prestadores de nivel 1: profesionales que intervienen en el proceso de rehabilitación.
    """]
    if notas_d23[0]:
        with st.expander("Nota"):
            st.markdown(notas_d23[0])
    preguntas_d2_3 = [
        "**La valoración del estado funcional incluye diferentes dominios o áreas del funcionamiento de los usuarios.**",
        "**La valoración del estado funcional se basa en parámetros medibles y los resultados se expresan en datos numéricos y/o categóricos.**",
        "**La valoración del estado funcional concluye con el perfil de funcionamiento o el diagnóstico funcional del usuario.**",
        "**La valoración del estado funcional involucra un equipo multidisciplinario\*\* que interviene en el proceso de rehabilitación.**",
    ]
    for i, texto in enumerate(preguntas_d2_3):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_3_{i+1}")
            guardar_respuesta(f"pD2_3_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.3:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_3")
            guardar_respuesta("D2_3", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_3")
            guardar_respuesta("obsD2_3", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 13 - D2.4
elif st.session_state.paso == 21:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.4 La evaluación considera el desempeño y los roles del usuario en diferentes entornos. 
                </div>
                """, unsafe_allow_html=True)
    notas_d24 = ["""Verificar:
                 
                 Instrumento[s] de evaluación 
                 Historia clínica
                     """]
    if notas_d24[0]:
        with st.expander("Nota"):
            st.markdown(notas_d24[0])
    preguntas_d2_4 = [
        "**En la evaluación se registra la ocupación o rol que desempeña el usuario en su entorno [Ej., hogar, trabajo, vida escolar].**",
        "**Se identifican las dificultades que presenta el usuario para el desempeño de actividades en su entorno.**",
        "**Se registran las expectativas del usuario y/o familia con relación a su ocupación o en el desempeño de actividades.**",
        "**La evaluación del usuario incluye pruebas o instrumentos para valorar la realización de actividades en su entorno.**",
    ]
    for i, texto in enumerate(preguntas_d2_4):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_4_{i+1}")
            guardar_respuesta(f"pD2_4_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.4:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_4")
            guardar_respuesta("D2_4", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_4")
            guardar_respuesta("obsD2_4", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 14 - D2.5
elif st.session_state.paso == 22:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.5 En la evaluación se identifican facilitadores y barreras del entorno que influyen en el proceso de rehabilitación del usuario. 
                </div>
                """, unsafe_allow_html=True)
    notas_d25 = ["""Verificar:
                 Instrumento[s] de evaluación.
                 Historia clínica.
    """]
    if notas_d25[0]:
        with st.expander("Nota"):
            st.markdown(notas_d25[0])

    st.markdown("""
                <div style="
                background-color: #f5f5f5 ;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                "><b> En la historia clínica se registran  facilitadores y/o barreras relacionados con: 
                </div>
                """, unsafe_allow_html=True)

    preguntas_d2_5 = [
        "**Acceso a servicios de salud según complejidad del diagnóstico o condición del usuario.**",
        "**Ayudas técnicas: disponibilidad, entrenamiento y adaptación, adecuación al entorno.**",
        "**Ajustes razonables en el entorno.**",
        "**Redes de apoyo.**",
    ]
    for i, texto in enumerate(preguntas_d2_5):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("------------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_5_{i+1}")
            guardar_respuesta(f"pD2_5_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.5:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_5")
            guardar_respuesta("D2_5", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_5")
            guardar_respuesta("obsD2_5", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 15 - D2.6
elif st.session_state.paso == 23:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.6 En la evaluación se registran las expectativas del usuario, la familia o cuidador respecto al proceso de rehabilitación. ►
                </div>
                """, unsafe_allow_html=True)
    notas_d26 = ["""Verificar:
    
                 Instrumento[s] de evaluación
                 Historia clínica
                 Estrategia de acompañamiento
    """]
    if notas_d26[0]:
        with st.expander("Nota"):
            st.markdown(notas_d26[0])
    preguntas_d2_6 = [
        "**La historia clínica incluye un ítem para el registro de las expectativas del usuario, la familia o cuidador.**",
        "**Se registran las expectativas del usuario con relación al proceso de rehabilitación.**",
        "**Se registran las expectativas de la familia o cuidador, especialmente en usuarios pediátricos, con compromiso cognitivo o dependencia severa.**",
        "**Se implementan estrategias de acompañamiento a usuarios y/o familias con expectativas no realistas frente al proceso de rehabilitación.**",
    ]
    for i, texto in enumerate(preguntas_d2_6):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_6_{i+1}")
            guardar_respuesta(f"pD2_6_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.6:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_6")
            guardar_respuesta("D2_6", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_6")
            guardar_respuesta("obsD2_6", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 16 - D2.7
elif st.session_state.paso == 24:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.7 El plan de atención del usuario de rehabilitación se estructura de acuerdo al modelo de atención y se centra en la persona. ►
                </div>
                """, unsafe_allow_html=True)
    notas_d27 = ["""Verificar:
                 
                 Historia clínica
                 Plan de atención
    """]
    if notas_d27[0]:
        with st.expander("Nota"):
            st.markdown(notas_d27[0])
    preguntas_d2_7 = [
        "**El plan de atención de los usuarios de rehabilitación hace parte de la historia clínica.**",
        "**El plan de atención tiene una estructura predeterminada que incluye los objetivos o metas de rehabilitación.**",
        "**En el plan de atención se describen las intervenciones a realizar por los profesionales o el equipo de rehabilitación.**",
        "**El plan de atención es individualizado y se basa en la condición de salud, el estado funcional, las necesidades y expectativas del usuario.**",
    ]
    for i, texto in enumerate(preguntas_d2_7):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
            st.markdown("-----------------------")
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_7_{i+1}")
            guardar_respuesta(f"pD2_7_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.7:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_7")
            guardar_respuesta("D2_7", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_7")
            guardar_respuesta("obsD2_7", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 17 - D2.8
elif st.session_state.paso == 25:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.8 El plan de atención integra el manejo médico de la condición de salud y las intervenciones para el logro de los objetivos y/o metas de rehabilitación. 
                </div>
                """, unsafe_allow_html=True)
    notas_d28 = [
    """ 
    Nota o instrucciones para D2.8.
    """]
    if notas_d28[0]:
        with st.expander("Nota"):
            st.markdown(notas_d28[0])
    preguntas_d2_8 = [
        "Pregunta 1 de D2.8",
        "Pregunta 2 de D2.8",
        "Pregunta 3 de D2.8",
        "Pregunta 4 de D2.8",
    ]
    for i, texto in enumerate(preguntas_d2_8):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_8_{i+1}")
            guardar_respuesta(f"pD2_8_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.8:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_8")
            guardar_respuesta("D2_8", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_8")
            guardar_respuesta("obsD2_8", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 18 - D2.9
elif st.session_state.paso == 26:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.9 Título de la condición D2.9
                </div>
                """, unsafe_allow_html=True)
    notas_d29 = [
    """ 
    Nota o instrucciones para D2.9.
    """]
    if notas_d29[0]:
        with st.expander("Nota"):
            st.markdown(notas_d29[0])
    preguntas_d2_9 = [
        "Pregunta 1 de D2.9",
        "Pregunta 2 de D2.9",
        "Pregunta 3 de D2.9",
        "Pregunta 4 de D2.9",
    ]
    for i, texto in enumerate(preguntas_d2_9):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_9_{i+1}")
            guardar_respuesta(f"pD2_9_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.9:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_9")
            guardar_respuesta("D2_9", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_9")
            guardar_respuesta("obsD2_9", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 19 - D2.10
elif st.session_state.paso == 27:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.10 Título de la condición D2.10
                </div>
                """, unsafe_allow_html=True)
    notas_d210 = [
    """ 
    Nota o instrucciones para D2.10.
    """]
    if notas_d210[0]:
        with st.expander("Nota"):
            st.markdown(notas_d210[0])
    preguntas_d2_10 = [
        "Pregunta 1 de D2.10",
        "Pregunta 2 de D2.10",
        "Pregunta 3 de D2.10",
        "Pregunta 4 de D2.10",
    ]
    for i, texto in enumerate(preguntas_d2_10):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_10_{i+1}")
            guardar_respuesta(f"pD2_10_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.10:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_10")
            guardar_respuesta("D2_10", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_10")
            guardar_respuesta("obsD2_10", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 20 - D2.11
elif st.session_state.paso == 28:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.11 Título de la condición D2.11
                </div>
                """, unsafe_allow_html=True)
    notas_d211 = [
    """ 
    Nota o instrucciones para D2.11.
    """]
    if notas_d211[0]:
        with st.expander("Nota"):
            st.markdown(notas_d211[0])
    preguntas_d2_11 = [
        "Pregunta 1 de D2.11",
        "Pregunta 2 de D2.11",
        "Pregunta 3 de D2.11",
        "Pregunta 4 de D2.11",
    ]
    for i, texto in enumerate(preguntas_d2_11):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_11_{i+1}")
            guardar_respuesta(f"pD2_11_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.11:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_11")
            guardar_respuesta("D2_11", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_11")
            guardar_respuesta("obsD2_11", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

#################### Paso 21 - D2.12
elif st.session_state.paso == 29:
    st.markdown("""
                <div style="
                background-color:
                #0b3c70;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                ">
                D2.12 Título de la condición D2.12
                </div>
                """, unsafe_allow_html=True)
    notas_d212 = [
    """ 
    Nota o instrucciones para D2.12.
    """]
    if notas_d212[0]:
        with st.expander("Nota"):
            st.markdown(notas_d212[0])
    preguntas_d2_12 = [
        "Pregunta 1 de D2.12",
        "Pregunta 2 de D2.12",
        "Pregunta 3 de D2.12",
        "Pregunta 4 de D2.12",
    ]
    for i, texto in enumerate(preguntas_d2_12):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD2_12_{i+1}")
            guardar_respuesta(f"pD2_12_{i+1}", val)
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D2.12:**")
            val = st.selectbox("", opciones, format_func=lambda x: x[0], key="D2_12")
            guardar_respuesta("D2_12", val)
        with col2:
            obs = st.text_area("Observaciones", key="obsD2_12")
            guardar_respuesta("obsD2_12", obs)
    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)





#### Final #####################
elif st.session_state.paso == 30:

    col1, col2= st.columns([5, 1])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

    st.success("¡Formulario completado! ✅")
    
    # --- Mostrar respuestas en formato JSON ---
    st.subheader("Resumen de respuestas:")
    st.json(st.session_state.respuestas)  # Muestra todas las respuestas almacenadas
    
    # --- Opción 1: Botón para reiniciar el formulario ---
    if st.button("🏠 Volver al inicio", type="primary"):
        # Limpiar el session_state (opcional, si quieres resetear todo)
        st.session_state.paso = 1
        #st.session_state.respuestas = {}  # Elimina esto si quieres conservar los datos
        st.rerun()  # Recarga la app para reiniciar
    
    # --- Opción 2: Botón para descargar respuestas (opcional) ---
    import pandas as pd
    from io import BytesIO
    
    df_respuestas = pd.DataFrame([st.session_state.respuestas])
    csv = df_respuestas.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        label="📥 Descargar respuestas (CSV)",
        data=csv,
        file_name="respuestas_formulario.csv",
        mime="text/csv"
    )
