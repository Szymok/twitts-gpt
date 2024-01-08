# Generowanie tweetów GPT
Wersja na żywo tej aplikacji pod adresem tweets.streamlit.app

## Opis
Ta mini-aplikacja Streamlit generuje teksty Tweetów przy użyciu GPT OpenAI dla tekstów i DALL-E dla obrazów.

Formularz tworzenia monitu tekstowego akceptuje temat, a także opcjonalny parametr nastroju i konto na Twitterze do "transferu stylu" (aktualizacja: ze względu na nowe ograniczenia API Twittera transfer stylu prawdopodobnie już nie działa). Następnie aplikacja generuje monit z instrukcją napisania odpowiedniego tweeta i wysyła go do interfejsu API OpenAI, który - korzystając z jednego z ich modeli GPT, które zostały przeszkolone na wielu publicznie dostępnych treściach tekstowych - przewiduje następne prawdopodobnie używane tokeny (słowa), a tym samym generuje treść tweeta. Ponadto aplikacja może zażądać i wyświetlić obraz z modelu DALL-E OpenAI, używając wcześniej wygenerowanego tekstu Tweeta jako podpowiedzi.

