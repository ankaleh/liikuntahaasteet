# Tietokantasovellus-harjoitustyö 

Helsingin yliopiston tietojenkäsittelytieteen aineopintojen Tietokantasovellus-kurssilla tehty harjoitustyö ([kurssisivulle](https://hy-tsoha.github.io/materiaali/index))

## Työyhteisön sähköinen liikuntakalenteri -sovellus

* Sovelluksen avulla työnantaja voi järjestää liikuntakampanjoita (esittää haasteen ja palkinnon), ja työntekijät voivat haastaa toisiaan tai itsensä sekä seurata edistymistään eri haasteiden suhteen.

* Pääkäyttäjä voi lisätä haasteen ja nähdä, ketkä ovat täyttäneet haasteen. Pääkäyttäjän sivut ovat polussa /admin. Testipääkäyttäjän kayttäjätunnus on paulapääkäyttajä ja salasana testipääkäyttäjä.

* Sovellus tarjoaa pääkäyttäjän sivujen lisäksi seitsemän sivua:

1. aloitussivu, jolta pääsee rekisteröitymään tai kirjautumaan sovellukseen
2. rekisteröitymissivulla käyttäjä luo itselleen tunnukset ja päättää, millä nimellä haluaa esiintyä sovelluksessa (pelkkä etunimi riittää)
3. kirjautumissivulla käyttäjä kirjautuu sovellukseen
4. kirjautumisen jälkeen käyttäjä ohjataan omalle sivulle, jolla näkyvät
    - liikuntahaasteet, joissa käyttäjä on kirjautumishetkellä osallisena:
        - liikuntahaasteita on kahdenlaisia: 1) käyttäjän itselleen tai jollekulle toiselle käyttäjälle lähettämät haasteet, 2) käyttäjälle lähetetyt haasteet
        - jokaisesta haasteesta näkyy haastaja ja haastettu sekä kummankin kehittyminen ympyrädiagrammin muodossa (montako minuuttia haasteesta suoritettu) sekä Poista haaste -nappi, jonka avulla voi kieltäytyä haasteesta; napin painaminen poistaa haasteen myös haasteen lisääjältä
    - kaikki omat liikuntasuoritukset kootusti joko ympyrädiagrammissa (eri lajien osuudet minuutteina), viivadiagrammissa (kuinka monta minuuttia liikuntaa minäkin päivänä) tai taulukoituina (kaikkien suoritusten laji, ajankohta ja kesto minuutteina)
5. Tilastot-sivulla voi nähdä kaikkien joko ympyrä- tai pylväsdiagrammin muodossa, mitä lajeja työntekijät ovat harrastaneet ja kuinka paljon
6. Lisää suoritus -sivulla voi lisätä liikuntasuorituksen
7. Haasta-sivulla voi lähettää liikuntahaasteen toiselle käyttäjälle

* Kirjautunut käyttäjä pääse navigoimaan kaikilta sivuilta kaikille muille sivuille sekä kirjautumaan ulos.

* Huomattavaa: diagrammit näkyvät oikein Chromessa, mutta eivät välttämättä muissa selaimissa.