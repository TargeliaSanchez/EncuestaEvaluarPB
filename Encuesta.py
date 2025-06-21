import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import datetime
import uuid  # Para generar IDs únicos
#import openpyxl
from datetime import date


st.markdown("""
<style>
.vertical-divider {
    border-left: 1px solid #ccc;
    padding-left: 12px;
}
</style>
""", unsafe_allow_html=True)




st.markdown("""
    <style>
        .main .block-container {
            max-width: 95%;
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
    .no-cumple { background-color: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
    .incipiente { background-color: #fff8e1; color: #f57f17; border: 1px solid #ffcc80; }
    .aceptable { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
    .satisfactorio { background-color: #e3f2fd; color: #1565c0; border: 1px solid #90caf9; }
    .optimo { background-color: #f1f8e9; color: #33691e; border: 1px solid #c5e1a5; }
    .dimension-rating {
        background-color: #e3f2fd;
        padding: 1.5rem 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
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


# Inicializa el estado si no está definido
if "paso" not in st.session_state:
    st.session_state.paso = 1

def siguiente():
    st.session_state.paso += 1

def anterior():
    st.session_state.paso -= 1


opciones = [
    ("Seleccione una opción", 0),
    ("1 - No cumple", 1),
    ("2 - Incipiente", 2),
    ("3 - Aceptable", 3),
    ("4 - Satisfecho", 4),
    ("5 - Óptimo", 5)
]


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
        st.markdown("Diligencias previo a la visita y validar posteriormente con los delegados de la institución.")
    with col2:
    # Alineación vertical + espaciado elegante
        st.markdown('<div style="padding-top: 0.6rem; text-align:right;"><strong>FECHA</strong></div>', unsafe_allow_html=True)
    with col3:
    # Selector de fecha sin etiqueta visible
        fecha = st.date_input("", value=date.today(), label_visibility="collapsed")
    
    col1, col2 = st.columns([4,4])
    with col1:
        st.markdown("**DEPARTAMENTO**")
        DEPARTAMENTO = st.text_input("DEPARTAMENTO", value="",  label_visibility="collapsed")
    with col2:
        st.markdown("**MUNICIPIO**")
        MUNICIPIO = st.text_input("MUNICIPIO", value="",label_visibility="collapsed")
    
    col1,col2 = st.columns([4, 2])
    with col1:
        st.markdown("**INSTITUCIÓN PRESTADORA DE SERVIVIOS DE SALUD**")
        INSTITUCION = st.text_input("INSTITUCIÓN", value="",placeholder="Digite nombre completo del prestador", label_visibility="collapsed")
    with col2:
        st.markdown("**NIT**")
        NOMBRE_RESPONSABLE = st.text_input("NIT", value="", placeholder="Digite número-DV", label_visibility="collapsed")
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.markdown("**NATURALEZA JURÍDICA**")
        NATURALEZA_JURIDICA = st.selectbox("",[("Seleccione una opción...",0),("Pública",1),("Privada",2),("Mixta",3)], format_func=lambda x: x[0], key="naturaleza_juridica")
    with col2:
        st.markdown("**EMPRESA SOCIAL DE ESTADO**")
        EMPRESA_SOCIAL_ESTADO = st.selectbox("",[("Seleccione una opción...",0),("Si",1),("No",2)], format_func=lambda x: x[0], key="empresa_social_estado")
    with col3:
        st.markdown("**NIVEL DE ATENCIÓN DEL PRESTADOR**")
        NIVEL_ATENCION_PRESTADOR = st.selectbox("",[("Seleccione una opción...",0),("1",1),("2",2),("3",3)], format_func=lambda x: x[0], key="nivel_atencion_prestador")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.button("Siguiente ▶️", on_click=siguiente)

if st.session_state.paso == 2:

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
                background-color: #ADD8E6;
                color: black;
                padding: 4px 10px;
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
    servicio_1 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 1",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_1"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
# Columna 2: Días de atención
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_1 = st.checkbox("", key="L_1")
        with col2:
            st.markdown(f"**M**")
            dia_M_1 = st.checkbox("", key="M_1")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_1 = st.checkbox("", key="Mi_1")
        with col4:
            st.markdown(f"**J**")
            dia_J_1 = st.checkbox("", key="J_1")
        with col5:
            st.markdown(f"**V**")
            dia_V_1 = st.checkbox("", key="V_1")
        with col6:
            st.markdown(f"**S**")
            dia_S_1 = st.checkbox("", key="S_1")
        with col7:
            st.markdown(f"**D**")
            dia_D_1 = st.checkbox("", key="D_1")
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
        with col2:
            st.markdown("**HO**")
            area_HO_1 = st.checkbox("", key="HO_1")
        with col3:
            st.markdown("**UR**")
            area_UR_1 = st.checkbox("", key="UR_1")
        with col4:
            st.markdown("**U**")
            area_U_1 = st.checkbox("", key="U_1")
        with col5:
            st.markdown("**UCI**")
            area_UCI_1 = st.checkbox("", key="UCI_1")
        with col6:
            st.markdown("**Otr**")
            area_Otr_1 = st.checkbox("", key="Otr_1")
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
            mod_HOS_1 = st.checkbox("HOS", key="HOS_1")

        with col2:
            st.markdown("**Extramural**")
            mod_DOM_1 = st.checkbox("DOM", key="DOM_1")
            mod_JORN_1 = st.checkbox("JORN", key="JORN_1")
            mod_UNMOV_1 = st.checkbox("UN.MOV", key="UNMOV_1")

        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_1 = st.checkbox("TM-IA", key="TMIA_1")
            mod_TMNIA_1 = st.checkbox("TM-NIA", key="TMNIA_1")
            mod_TE_1 = st.checkbox("TE", key="TE_1")
            mod_TMO_1 = st.checkbox("TMO", key="TMO_1")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
# Columna 5: Prestador
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_1 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_1")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

if st.session_state.paso == 3:
    # --------------------- 222222
    servicio_2 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 2",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_2"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    # Columna 2: Días de atención
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_2 = st.checkbox("", key="L_2")
        with col2:
            st.markdown(f"**M**")
            dia_M_2 = st.checkbox("", key="M_2")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_2 = st.checkbox("", key="Mi_2")
        with col4:
            st.markdown(f"**J**")
            dia_J_2 = st.checkbox("", key="J_2")
        with col5:
            st.markdown(f"**V**")
            dia_V_2 = st.checkbox("", key="V_2")
        with col6:
            st.markdown(f"**S**")
            dia_S_2 = st.checkbox("", key="S_2")
        with col7:
            st.markdown(f"**D**")
            dia_D_2 = st.checkbox("", key="D_2")
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
        with col2:
            st.markdown("**HO**")
            area_HO_2 = st.checkbox("", key="HO_2")
        with col3:
            st.markdown("**UR**")
            area_UR_2 = st.checkbox("", key="UR_2")
        with col4:
            st.markdown("**U**")
            area_U_2 = st.checkbox("", key="U_2")
        with col5:
            st.markdown("**UCI**")
            area_UCI_2 = st.checkbox("", key="UCI_2")
        with col6:
            st.markdown("**Otr**")
            area_Otr_2 = st.checkbox("", key="Otr_2")
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
            mod_HOS_2 = st.checkbox("HOS", key="HOS_2")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_2 = st.checkbox("DOM", key="DOM_2")
            mod_JORN_2 = st.checkbox("JORN", key="JORN_2")
            mod_UNMOV_2 = st.checkbox("UN.MOV", key="UNMOV_2")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_2 = st.checkbox("TM-IA", key="TMIA_2")
            mod_TMNIA_2 = st.checkbox("TM-NIA", key="TMNIA_2")
            mod_TE_2 = st.checkbox("TE", key="TE_2")
            mod_TMO_2 = st.checkbox("TMO", key="TMO_2")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    # Columna 5: Prestador
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_2 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_2")

    # --------------------- 333333
    servicio_3 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 3",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_3"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_3 = st.checkbox("", key="L_3")
        with col2:
            st.markdown(f"**M**")
            dia_M_3 = st.checkbox("", key="M_3")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_3 = st.checkbox("", key="Mi_3")
        with col4:
            st.markdown(f"**J**")
            dia_J_3 = st.checkbox("", key="J_3")
        with col5:
            st.markdown(f"**V**")
            dia_V_3 = st.checkbox("", key="V_3")
        with col6:
            st.markdown(f"**S**")
            dia_S_3 = st.checkbox("", key="S_3")
        with col7:
            st.markdown(f"**D**")
            dia_D_3 = st.checkbox("", key="D_3")
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_3 = st.checkbox("", key="CE_3")
        with col2:
            st.markdown("**HO**")
            area_HO_3 = st.checkbox("", key="HO_3")
        with col3:
            st.markdown("**UR**")
            area_UR_3 = st.checkbox("", key="UR_3")
        with col4:
            st.markdown("**U**")
            area_U_3 = st.checkbox("", key="U_3")
        with col5:
            st.markdown("**UCI**")
            area_UCI_3 = st.checkbox("", key="UCI_3")
        with col6:
            st.markdown("**Otr**")
            area_Otr_3 = st.checkbox("", key="Otr_3")
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_3 = st.checkbox("AMB", key="AMB_3")
            mod_HOS_3 = st.checkbox("HOS", key="HOS_3")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_3 = st.checkbox("DOM", key="DOM_3")
            mod_JORN_3 = st.checkbox("JORN", key="JORN_3")
            mod_UNMOV_3 = st.checkbox("UN.MOV", key="UNMOV_3")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_3 = st.checkbox("TM-IA", key="TMIA_3")
            mod_TMNIA_3 = st.checkbox("TM-NIA", key="TMNIA_3")
            mod_TE_3 = st.checkbox("TE", key="TE_3")
            mod_TMO_3 = st.checkbox("TMO", key="TMO_3")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_3 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_3")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

if st.session_state.paso == 4:
    # --------------------- 444444
    servicio_4 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 4",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_4"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_4 = st.checkbox("", key="L_4")
        with col2:
            st.markdown(f"**M**")
            dia_M_4 = st.checkbox("", key="M_4")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_4 = st.checkbox("", key="Mi_4")
        with col4:
            st.markdown(f"**J**")
            dia_J_4 = st.checkbox("", key="J_4")
        with col5:
            st.markdown(f"**V**")
            dia_V_4 = st.checkbox("", key="V_4")
        with col6:
            st.markdown(f"**S**")
            dia_S_4 = st.checkbox("", key="S_4")
        with col7:
            st.markdown(f"**D**")
            dia_D_4 = st.checkbox("", key="D_4")
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_4 = st.checkbox("", key="CE_4")
        with col2:
            st.markdown("**HO**")
            area_HO_4 = st.checkbox("", key="HO_4")
        with col3:
            st.markdown("**UR**")
            area_UR_4 = st.checkbox("", key="UR_4")
        with col4:
            st.markdown("**U**")
            area_U_4 = st.checkbox("", key="U_4")
        with col5:
            st.markdown("**UCI**")
            area_UCI_4 = st.checkbox("", key="UCI_4")
        with col6:
            st.markdown("**Otr**")
            area_Otr_4 = st.checkbox("", key="Otr_4")
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_4 = st.checkbox("AMB", key="AMB_4")
            mod_HOS_4 = st.checkbox("HOS", key="HOS_4")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_4 = st.checkbox("DOM", key="DOM_4")
            mod_JORN_4 = st.checkbox("JORN", key="JORN_4")
            mod_UNMOV_4 = st.checkbox("UN.MOV", key="UNMOV_4")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_4 = st.checkbox("TM-IA", key="TMIA_4")
            mod_TMNIA_4 = st.checkbox("TM-NIA", key="TMNIA_4")
            mod_TE_4 = st.checkbox("TE", key="TE_4")
            mod_TMO_4 = st.checkbox("TMO", key="TMO_4")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_4 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_4")


#if st.session_state.paso == 5:
    # --------------------- 555555
    servicio_5 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 5",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_5"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_5 = st.checkbox("", key="L_5")
        with col2:
            st.markdown(f"**M**")
            dia_M_5 = st.checkbox("", key="M_5")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_5 = st.checkbox("", key="Mi_5")
        with col4:
            st.markdown(f"**J**")
            dia_J_5 = st.checkbox("", key="J_5")
        with col5:
            st.markdown(f"**V**")
            dia_V_5 = st.checkbox("", key="V_5")
        with col6:
            st.markdown(f"**S**")
            dia_S_5 = st.checkbox("", key="S_5")
        with col7:
            st.markdown(f"**D**")
            dia_D_5 = st.checkbox("", key="D_5")
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_5 = st.checkbox("", key="CE_5")
        with col2:
            st.markdown("**HO**")
            area_HO_5 = st.checkbox("", key="HO_5")
        with col3:
            st.markdown("**UR**")
            area_UR_5 = st.checkbox("", key="UR_5")
        with col4:
            st.markdown("**U**")
            area_U_5 = st.checkbox("", key="U_5")
        with col5:
            st.markdown("**UCI**")
            area_UCI_5 = st.checkbox("", key="UCI_5")
        with col6:
            st.markdown("**Otr**")
            area_Otr_5 = st.checkbox("", key="Otr_5")
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_5 = st.checkbox("AMB", key="AMB_5")
            mod_HOS_5 = st.checkbox("HOS", key="HOS_5")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_5 = st.checkbox("DOM", key="DOM_5")
            mod_JORN_5 = st.checkbox("JORN", key="JORN_5")
            mod_UNMOV_5 = st.checkbox("UN.MOV", key="UNMOV_5")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_5 = st.checkbox("TM-IA", key="TMIA_5")
            mod_TMNIA_5 = st.checkbox("TM-NIA", key="TMNIA_5")
            mod_TE_5 = st.checkbox("TE", key="TE_5")
            mod_TMO_5 = st.checkbox("TMO", key="TMO_5")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_5 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_5")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

if st.session_state.paso == 5:
    # --------------------- 666666
    servicio_6 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 6",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_6"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_6 = st.checkbox("", key="L_6")
        with col2:
            st.markdown(f"**M**")
            dia_M_6 = st.checkbox("", key="M_6")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_6 = st.checkbox("", key="Mi_6")
        with col4:
            st.markdown(f"**J**")
            dia_J_6 = st.checkbox("", key="J_6")
        with col5:
            st.markdown(f"**V**")
            dia_V_6 = st.checkbox("", key="V_6")
        with col6:
            st.markdown(f"**S**")
            dia_S_6 = st.checkbox("", key="S_6")
        with col7:
            st.markdown(f"**D**")
            dia_D_6 = st.checkbox("", key="D_6")
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_6 = st.checkbox("", key="CE_6")
        with col2:
            st.markdown("**HO**")
            area_HO_6 = st.checkbox("", key="HO_6")
        with col3:
            st.markdown("**UR**")
            area_UR_6 = st.checkbox("", key="UR_6")
        with col4:
            st.markdown("**U**")
            area_U_6 = st.checkbox("", key="U_6")
        with col5:
            st.markdown("**UCI**")
            area_UCI_6 = st.checkbox("", key="UCI_6")
        with col6:
            st.markdown("**Otr**")
            area_Otr_6 = st.checkbox("", key="Otr_6")
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_6 = st.checkbox("AMB", key="AMB_6")
            mod_HOS_6 = st.checkbox("HOS", key="HOS_6")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_6 = st.checkbox("DOM", key="DOM_6")
            mod_JORN_6 = st.checkbox("JORN", key="JORN_6")
            mod_UNMOV_6 = st.checkbox("UN.MOV", key="UNMOV_6")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_6 = st.checkbox("TM-IA", key="TMIA_6")
            mod_TMNIA_6 = st.checkbox("TM-NIA", key="TMNIA_6")
            mod_TE_6 = st.checkbox("TE", key="TE_6")
            mod_TMO_6 = st.checkbox("TMO", key="TMO_6")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_6 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_6")


    # --------------------- 777777
    servicio_7 = st.selectbox(
        "SERVICIOS DE REHABILITACIÓN HABILITADOS 7",
        options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
        key="servicio_7"
    )   
    col_dias,sep1,col_areas, sep2,col_modalidades,sep3, col_prestador = st.columns([1,0.1,1.1,0.1,1.5,0.1,1.5])
    with col_dias:
        st.markdown("<div style='text-align: center;'><b>Días de atención</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X los días de atención")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            st.markdown(f"**L**")
            dia_L_7 = st.checkbox("", key="L_7")
        with col2:
            st.markdown(f"**M**")
            dia_M_7 = st.checkbox("", key="M_7")
        with col3:
            st.markdown(f"**X**")
            dia_Mi_7 = st.checkbox("", key="Mi_7")
        with col4:
            st.markdown(f"**J**")
            dia_J_7 = st.checkbox("", key="J_7")
        with col5:
            st.markdown(f"**V**")
            dia_V_7 = st.checkbox("", key="V_7")
        with col6:
            st.markdown(f"**S**")
            dia_S_7 = st.checkbox("", key="S_7")
        with col7:
            st.markdown(f"**D**")
            dia_D_7 = st.checkbox("", key="D_7")
    with sep1:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_areas:
        st.markdown("<div style='text-align: center;'><b>Áreas asistenciales</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X las áreas donde se prestan servicios de rehabilitación")
        col1, col2, col3,col4,col5,col6 = st.columns(6)
        with col1:
            st.markdown("**CE**")
            area_CE_7 = st.checkbox("", key="CE_7")
        with col2:
            st.markdown("**HO**")
            area_HO_7 = st.checkbox("", key="HO_7")
        with col3:
            st.markdown("**UR**")
            area_UR_7 = st.checkbox("", key="UR_7")
        with col4:
            st.markdown("**U**")
            area_U_7 = st.checkbox("", key="U_7")
        with col5:
            st.markdown("**UCI**")
            area_UCI_7 = st.checkbox("", key="UCI_7")
        with col6:
            st.markdown("**Otr**")
            area_Otr_7 = st.checkbox("", key="Otr_7")
    with sep2:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_modalidades:
        st.markdown("<div style='text-align: center;'><b>Modalidades de prestación</b></div>", unsafe_allow_html=True)
        st.markdown("Marque con X  las modalidades habilitadas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Intramural**")
            mod_AMB_7 = st.checkbox("AMB", key="AMB_7")
            mod_HOS_7 = st.checkbox("HOS", key="HOS_7")
        with col2:
            st.markdown("**Extramural**")
            mod_DOM_7 = st.checkbox("DOM", key="DOM_7")
            mod_JORN_7 = st.checkbox("JORN", key="JORN_7")
            mod_UNMOV_7 = st.checkbox("UN.MOV", key="UNMOV_7")
        with col3:
            st.markdown("**Telemedicina**")
            mod_TMIA_7 = st.checkbox("TM-IA", key="TMIA_7")
            mod_TMNIA_7 = st.checkbox("TM-NIA", key="TMNIA_7")
            mod_TE_7 = st.checkbox("TE", key="TE_7")
            mod_TMO_7 = st.checkbox("TMO", key="TMO_7")
    with sep3:
        st.markdown("<div class='vertical-divider'></div>", unsafe_allow_html=True)
    with col_prestador:
        st.markdown("<div style='text-align: center;'><b>Prestador telemedicina</b></div>", unsafe_allow_html=True)
        st.markdown("marque con una X el tipo de prestador")
        prestador_7 = st.radio("Tipo", ["P.REM", "P.REF"], key="prestador_7")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


if  st.session_state.paso == 6:#Bloque  recursos humanos 1
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
                background-color: #ADD8E6;
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
        
        numero_1 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_1")

        DesP_2 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_2"
        )
        
        numero_2 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_2")
    
    with col2:
        DesP_3 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_3"
        )
        
        numero_3 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_3")
   
        DesP_4 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_4"
        )
        
        numero_4 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_4")
    with col3:
        DesP_5 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_5"
        )
        
        numero_5 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_5")
    
        DesP_6 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_6"
        )
        
        numero_6 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_6")
    with col4:
        DesP_7 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_7"
        )
        
        numero_7 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_7")
   
        DesP_8 = st.selectbox(
            "",
            options=["Seleccione", "Fisioterapia", "Fonoaudiología", "Terapia ocupacional", "Terapia Respiratoria","Esp. medicina Física y Fehabilitación", "Psicología", "Trabajo Social", "Nutrición"],
            key="DesP_8"
        )
        
        numero_8 = st.number_input("", min_value=0, max_value=100, value=0, step=1,key="numero_8")


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
                background-color: #ADD8E6;
                color: black;
                padding: 4px 10px;
                font-weight: normal;
                border-radius: 0.5px;
                ">
                Registre <b>Registre aclaraciones pertinentes sobre la oferta de servicios de rehabilitación y el talento humano relacionado:</b> variaciones en la disponibilidad de los servicios, otras áreas donde se prestan servicios de rehabilitación. 
                </div>
                """, unsafe_allow_html=True)
    

    st.text_area("Aclaraciones", height=80, key="aclaraciones")

    st.markdown("<hr class='linea'>", unsafe_allow_html=True)


    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)


if st.session_state.paso == 7:
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
        st.text_input(
            label="",  # Oculta el texto de la variable
            placeholder=f"{i}. Digite nombre completo [Cargo]",  # Aparece dentro del recuadro
            key=f"rep_inst_{i}"
        )

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
        st.text_input(label="",
                      placeholder=f"{i}. Digite nombre completo", 
                      key=f"prof_verif_{i}")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)

##################### FORMULARIO DE EVALUACIÓN #####################

if st.session_state.paso == 8: # Evaluación de la institución.

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


if st.session_state.paso == 9:
# Encabezado principal
    #st.markdown("### D1. ORGANIZACIÓN Y GESTIÓN DE LOS SERVICIOS DE REHABILITACIÓN")

# Descripción de la sección
# Paso 1 - D1.1


    st.markdown("**D1.1 La oferta de servicios de rehabilitación corresponde con el nivel de complejidad de la institución.**")
    preguntas = [
        "La institución presta servicio de psicología y/o trabajo social.",
        "La institución presta servicios de fisioterapia, fonoaudiología y/o terapia ocupacional.",
        "Los servicios de rehabilitación disponibles corresponden con el nivel de complejidad.",
        "Los servicios de rehabilitación se organizan en un área específica de la institución.",
    ]
    for i, texto in enumerate(preguntas):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(texto)
        with col2:
            st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD11_{i+1}")

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.1:**")
            st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_1")
        with col2:
            st.text_area("Observaciones", key="obsD11")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)
#-------------------------------------------------------------------------------------
# Paso 2 - D1.2
elif st.session_state.paso == 9:
    st.markdown("**D1.2 El talento humano de rehabilitación vinculado a la institución es acorde a la capacidad instalada versus la demanda de los servicios.**")
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
            st.selectbox("", opciones, format_func=lambda x: x[0], key=f"pD12_{i+1}")

    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("**Calificación D1.2:**")
            st.selectbox("", opciones, format_func=lambda x: x[0], key="D1_2")
        with col2:
            st.text_area("Observaciones", key="obsD12")

    col1, col2= st.columns([1, 4])
    with col1:
        st.button("◀️ Anterior", on_click=anterior)
    with col2:
        st.button("Siguiente ▶️", on_click=siguiente)



