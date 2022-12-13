import pandas as pd
import streamlit as st
import yagmail 
import numpy as np




st.title(":gift: Hediye Çekiliş Uygulaması") 

st.markdown("## Nasıl çalışır?")
st.markdown("- Hediye çekilişine katılmak isteyen tüm adayların ismini ve mail adresini kaydedin.")
st.markdown("- `Çekilişi Yap!` butonuna bastığınızda uygulama her bir kişi ile kendisinden hariç birisini rastgele olarak eşleştirip kim ile eşleştiğini bildiren bir e-posta atacaktır.")
st.markdown("- İsim listesini yenilemek için f5 tuşuna basıp sayfayı yenileyebilirsiniz")

st.markdown("")

# "st.session_state object:", st.session_state

if "df_result" not in st.session_state:
    st.session_state['df_result'] = pd.DataFrame(columns=['isim','eposta'])


if "df_result_gift" not in st.session_state:
    st.session_state['df_result_gift'] = pd.DataFrame(columns=['isim','eposta'])


# st.write(st.session_state)

name = st.text_input('Adaylardan birinin adını yazın')
email = st.text_input('Adayın mail adresini yazın')


def onAddRow():
    data = {
            'isim':name,
            'eposta':email  
        }
    st.session_state['df_result'] = st.session_state['df_result'].append(data, ignore_index=True)
    st.session_state['df_result_gift'] = st.session_state['df_result_gift'].append(data, ignore_index=True)


st.button("Aday ekle", on_click = onAddRow)



st.dataframe(st.session_state.df_result)


def sendMail():
    if len(pd.unique(st.session_state.df_result['isim'])) != len(st.session_state.df_result):
        st.warning('Her bir isim farklı olmalıdır')
        st.stop()
    
    if len(pd.unique(st.session_state.df_result['eposta'])) != len(st.session_state.df_result):
        st.warning('Her bir e-posta farklı olmalıdır')
        st.stop()
        
    yag = yagmail.SMTP(st.secrets("EMAIL"), st.secrets("PASSWORD"))
    start = 0
    end = len(st.session_state.df_result_gift)
    st.session_state.df_result_gift["gift_isim"] = np.nan
    st.session_state.df_result_gift["gift_eposta"] = np.nan
    index_list = np.array(list(range(start,end)))
    for i in index_list:
        draw_pick = np.random.choice(index_list)
        while(i == draw_pick):
            draw_pick = np.random.choice(index_list)
        index_list = index_list[(index_list != draw_pick)]
        gift_isim = st.session_state.df_result_gift["isim"][draw_pick] 
        gift_eposta = st.session_state.df_result_gift["eposta"][draw_pick] 
        contents = [
        "Merhaba " + st.session_state.df_result_gift["isim"][i] , ",","\n",
        "<b>Hediye alacağın kişi: </b>" +   gift_isim
        ]
        target = gift_eposta
        yag.send(target, 'Çekiliş Sonuçları', contents)
  
    st.success("Her bir mail adresine kendisine çıkan çekiliş sonucu gönderilmiştir.")
    st.balloons()
    
    
    
    
    
st.button("Çekilişi Yap!", on_click = sendMail)


