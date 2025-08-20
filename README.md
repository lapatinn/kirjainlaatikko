# Kirjainlaatikko

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään sovellukseen elokuva-arvosteluja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään elokuva-arvosteluja.

* Käyttäjä näkee sovellukseen lisätyt arvostelut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät arvostelut.

* Käyttäjä pystyy etsimään arvosteluja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä arvosteluja.

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät arvostelut.

* Käyttäjä pystyy valitsemaan arvostelulle/arvostelemalleen elokuvalle yhden tai useamman luokittelun (genre). Mahdolliset luokat ovat tietokannassa.

* Sovelluksessa on pääasiallisen arvostelun lisäksi kommentteja, käyttäjä voi lisätä kommentteja omiin tai muiden arvosteluihin.

## Sovelluksen käyttöönotto

Asenna `flask` kirjasto:

```
$ pip3 install flask
```

Alusta tietokanta:

```
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:

```
$ flask run
```
