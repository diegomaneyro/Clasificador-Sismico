import streamlit as st
import pandas as pd
import numpy as np
import folium
import requests
from etl import etl
# from streamlit_lottie import st_lottie
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Alerta Sismo",
    page_icon="🌎🌏",
    layout="wide"
)

jp_handler = etl.Extraccion_Url('http://ds.iris.edu/ieb/evtable.phtml?caller=IEB&st=1970-01-01&et=2025-01-01&minmag=6&maxmag=10&orderby=time-desc&src=usgs&limit=5000&maxlat=56.000&minlat=22.000&maxlon=159.000&minlon=127.000&sbl=1&pbl=1&caller=self&name=Japan%20Region&zm=3&mt=ter&rgn=Japan%20Region&title=IEB%20export%3A%20786%20earthquakes%20as%20a%20sortable%20table.&stitle=from%201970-01-01%20to%20the%20latest%20available%2C%20with%20magnitudes%20from%206%20to%2010%2C%20all%20depths%2C%20with%20priority%20for%20most%20recent%2C%20limited%20to%205000%2C%20%20showing%20data%20from%20USGS%2C%20', 'chrome')

ch_handler = etl.Extraccion_Url('http://www.csn.uchile.cl/sismologia/grandes-terremotos-en-chile/', 'chrome')

emoji_dicc = {'alerta1': 'imagenes/st_imgs/relieved-face.png',
              'alerta2': 'imagenes/st_imgs/hushed-face.png',
              'alerta3': 'imagenes/st_imgs/anguished-face.png',
              'alerta4': 'imagenes/st_imgs/face-screaming-in-fear.png'
              }


@st.cache_data
def titulo():
    with st.container():
        titulo = '<p style= "font-family: Helvetica; text-align:center; font-size:100px" >Sistema de Alerta Sismica</p>'
        st.markdown(titulo, unsafe_allow_html=True)
        """---"""


titulo()


inicio, chile, japon, usa = st.tabs(["Inicio", "Chile", "Japon", "USA"])


def intro():
    col_izq, col_der = st.columns(2)
    with col_izq:
        introduccion = '<p style="font-family:Helvetica; color:white; font-size: 30px;">Los sismos son movimientos o vibraciones bruscas que se producen en la Tierra debido a la liberación de energía acumulada en el interior de la corteza terrestre. Esta liberación de energía se produce cuando las placas tectónicas que forman la corteza terrestre se desplazan o se deslizan entre sí, causando una ruptura en la roca que libera una gran cantidad de energía en forma de ondas sísmicas.</p>'
        st.markdown(introduccion, unsafe_allow_html=True)

    with col_der:
        img = "<img src=https://img.freepik.com/vector-gratis/concepto-interacciones-placas-tectonicas_1308-123308.jpg?w=1380&t=st=1683247619~exp=1683248219~hmac=79999464085c5f247da09a8db28d14aeb266483a9608a759ab22b83393f4364f width='100%' style='border-radius: 10px; align-self: center;'>"
        st.markdown(img, unsafe_allow_html=True)


def alerta_jp():
    """Esta funcion permite renderizar el contenido referente a
    a la seccion de Japon"""

    datos_japon = jp_handler.df

    izq, der = st.columns(2)
    with izq:
        st.write('soy japon')

    with der:
        # se instancia el mapa
        mapa1 = folium.Map(location=[datos_japon.Lat.mean(),
                                     datos_japon.Lon.mean()],
                           zoom_start=3,
                           control_scale=True)

        # Se extrae el evento sismico mas reciente
        evento = datos_japon.head(1)

        # contenido del popup
        magnitud_txt = f'Magnitud: {str(evento.Mag.values)}\n'
        region_txt = f'Region: {str(evento.Region.values)}'
        iframe = folium.IFrame(magnitud_txt + region_txt)
        # se instancia el popup
        pop_up = folium.Popup(iframe, min_width=300, max_width=300)
        # poner marcador
        folium.Marker(location=[evento.Lat, evento.Lon],
                      popup=pop_up).add_to(mapa1)

        # renderizar mapa1
        folium_static(mapa1, width=500)

        # # se recorre el df en busca de la informacion
        # for i,row in datos_japon.iterrows():
        #     # Contenido del popup
        #     iframe = folium.IFrame('Magnitud: ' + str(row['Mag']))
        #     # se instancia el popup
        #     pop_up = folium.Popup(iframe, min_width=300, max_width=300)
        #     # se agrega el marcador al mapa
        #     folium.Marker(location=[row['Lat'], row['Lon']],
        #                   popup=pop_up
        #                   ).add_to(mapa)
        # folium_static(mapa, width=700)
        # df = pd.DataFrame(
        #     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        #     columns=['lat', 'lon'])
        # st.map(df)


def alerta_ch():
    """Esta funcion permite renderizar el contenido referente a
    a la seccion de chile"""

    datos_chile = ch_handler.df

    izq, der = st.columns(2)
    with izq:
        st.write('soy chile')

    with der:
        # se instancia el mapa
        mapa2 = folium.Map(location=[datos_chile.Latitud.astype('float').mean(),
                                     datos_chile.Longitud.astype('float').mean()],
                           zoom_start=3,
                           control_scale=True)

        # Se extrae el evento sismico mas reciente
        evento = datos_chile.head(1)

        # contenido del popup
        magnitud_txt = f'Magnitud: {str(evento["Magnitud Ms"].values)}\n'
        # region_txt = f'Region: {str(evento.Region.values)}'
        iframe = folium.IFrame(magnitud_txt)
        # se instancia el popup
        pop_up = folium.Popup(iframe, min_width=300, max_width=300)
        # poner marcador
        folium.Marker(location=[evento.Latitud.float, evento.Longitud.float],
                      popup=pop_up).add_to(mapa2)

        # renderizar mapa2
        folium_static(mapa2, width=500)

        # # se recorre el df en busca de la informacion
        # for i,row in datos_chile.iterrows():
        #     # Contenido del popup
        #     iframe = folium.IFrame('Magnitud: ' + str(row['Mag']))
        #     # se instancia el popup
        #     pop_up = folium.Popup(iframe, min_width=300, max_width=300)
        #     # se agrega el marcador al mapa
        #     folium.Marker(location=[row['Lat'], row['Lon']],
        #                   popup=pop_up
        #                   ).add_to(mapa)
        # folium_static(mapa, width=700)
        # df = pd.DataFrame(
        #     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        #     columns=['lat', 'lon'])
        # st.map(df)

with inicio:
    intro()

with japon:
    alerta_jp()

with chile:
    alerta_ch()

# with st.sidebar:
#     emoji_cont = st.container()
#     with emoji_cont:
#         emoji = Image.open(emoji_dicc['alerta2'])
#         st.image(emoji, use_column_width='always')
#         st.divider()

#     with st.container():
#         inicio = st.button('Inicio',
#                            use_container_width=True)

#         sismos = st.button('Sismos',
#                            use_container_width=True)

#         if inicio:
#             intro()
#         if sismos:
#             alerta()
#         else:
#             intro()
