# importar pacotes
import streamlit as st
from PIL import Image

from filters import Filters


def main():
    st.title("Aplicação de Filtros em Imagens")
    st.sidebar.title("Escolha o filtro")

    # menu com opções de páginas
    menu_options = ["Filtros", "Sobre"]
    page = st.sidebar.selectbox("Escolha uma página", menu_options)

    if page == 'Filtros':
        # carregar e exibir imagem
        # cv2.imread não funciona com o streamlit, por isso utilizamos o PIL
        image_file = st.file_uploader("Carregue uma foto e aplique um filtro no menu lateral", type=['jpg', 'jpeg', 'png'])
        if image_file:
            user_image = Image.open(image_file)
            st.sidebar.text("Imagem Original")
            st.sidebar.image(user_image, width=150)
        else:
            user_image = Image.open('empty.jpg')

        filter = Filters(st, user_image)
        filter()

    elif page == 'Sobre':
        st.subheader("Esse projeto faz parte da Masterclass de Visão Computacional da Escola de Data Science (Sigmoidal)")
        st.markdown("""
            Neste projeto criamos uma aplicação web utilizando o Streamlit para exemplificar a manipulação de imagens
            utilizando OpenCV e Python.
            
            Nessa aplicação, é possível enviar uma imagem e aplicar um dos seguintes filtros: 
             - Escala de cinza (Grayscale)
             - Efeito de Desenho 
             - Sépia
             - Blur (embaçado)
             - Canny (destacar bordas)
             - Contraste
             - Brilho
        """)


if __name__ == '__main__':
    main()
