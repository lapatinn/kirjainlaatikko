# Kirjainlaatikko
Elokuva-arvostelu web sovellus projekti, inspiraationa letterboxd (siksi myös nimi). 

Suorita ennen käyttöä:

sqlite3 database.db < schema.sql

Tavoitteet:

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään sovellukseen elokuva-arvosteluja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään elokuva-arvosteluja.

* Käyttäjä näkee sovellukseen lisätyt arvostelut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät arvostelut.

* Käyttäjä pystyy etsimään arvosteluja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä            arvosteluja.

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät arvostelut.

* Käyttäjä pystyy valitsemaan arvostelulle/arvostelemalleen elokuvalle yhden tai useamman luokittelun (Elokuvan genre, julkaisuvuosi, arvosana). Mahdolliset luokat ovat tietokannassa.

* Sovelluksessa on pääasiallisen arvostelun lisäksi kommentteja, käyttäjä voi lisätä kommentteja omiin tai muiden arvosteluihin. 

Sovelluksen lopullinen tila (02.05):

Sovellus ilmeisesti toimii. Käyttäjä voi luoda tunnuksen, kirjautua ja arvostella elokuvia. Arvosteluja voi katsella omalta sivulta ja samoin myös käyttäjiä. Klikkaamalla käyttäjää pääsee käyttäjän henkilökohtaiselle sivulle, joka näyttää hänen luomat arvostelut ja niiden määrän. Käyttäjä voi muokata ja poistaa arvostelujaan. Arvosteluihin voi myös jättää kommentteja, joita voi poistaa. Arvosteluja voi myös hakea arvostellun elokuvan nimen perusteella. 
Sovellus tarkistaa käyttäjän syötteitä ja oikeuksia sekä html-pohjissa, että pääohjelmassa. Virheviesteihin on varauduttu ja suurin osa niistä ilmestyy mukavasti flash-ilmoituksena. Suurimpaan osaan virhetilanteista (tietääkseni) on varauduttu.
Yleisesti ottaen sovellus on aika yksinkertainen ja varsin tylsä, mutta mielestäni toteutus onnistui aika hyvin ja kaikki vaikuttaisi toimivan oikein. Css-tyyli on hyvin yksinkertainen, mutta ihan miellyttävä. 

Log:

12.03:

Added necessary components for basic functionality of the website, such as templates folder, static folder and corresponding functions to app.py. 


20.03:

Added ability to create movie reviews, along with the required database table. User id is now stored in session. Rearranged some elements on the front page. 

21.03:

Added dedicated page for movie reviews. Each review will redirect to a page according to review id. This page will store the actual contents of the review. Rearranged some elements on various pages and added return links to various pages. 

24.03:

Added ability to edit and remove reviews. 

25.03:

Added ability to search movie reviews by movie title. Made minor changes to arrangement. Added function for when a movie is not found the page will prompt to add a review. 

04.04:

Added genres, directors and year of release (can also be edited). Separate table in database. Cleared and repopulated databse. Added Users page, where the reviews of a certain user can be accessed along with review count. Made everything look a little less shit by rearranging some template elements and introducing some if/else statements where information may not always be available. 

05.04:

Added ability to leave comments on reviews. Users can also delete their own comments. Comments will show up as a list under a review. Cleaned up the front page and made minor rearrangements. Removed old unused functions (numbers, form/result) from app.py and corresponding templates. 

17.04:

Fixed edit_review page. The previously selected information about the review will now show as default value. Outsourced register and login functions to users.py: Perhaps a bit cleaner? Made canges to how error messages show, now a separate template with return links according to where the error came from (Error from register page will have a "retry" link pointing back to register page). Added return link to register page lol. 

18.04:

Hardened the users rights management, added error messages to undefined pages with integer id's and added a function which checks login (returns error page if no login) for certain functions. Undefined pages won't break the app now and users can only edit/remove their own content. 

26.04:

Apparently I managed to break removing reviews, nice. Fixed that. Added input regulation to templates and app.py so all user inputs (I think) will be double checked. 

28.04:

Added css styles. Modified frontpage. Made changes to arrangement and return links on various pages. 

01.05:

Moved most error messages from a separate page to a flash()-call. This applies to errors that would appear on a specific page, since flash() needs a redirect in order to update the page and show the message. Errors that occur when a user epicly trolls me by typing in an address that is not defined (or otherwise inaccessible due to whatever), will still redirect to a separate page. 
Had to make a separate function for checking the integrity of movie reviews: the if-and statement chain was taking up a stupid amount of horizontal space, much cleaner. In the process realized that editing a review has no restrictions whatsoever, fixed that. 
Added an alt-thingy to the image on the frontpage and "cleaned up" the code a little and uhh yeah. 

02.05:

Very minor cleanup.