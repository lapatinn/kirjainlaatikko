# Kirjainlaatikko
Elokuva-arvostelu web sovellus projekti, inspiraationa letterboxd (siksi myös nimi). 

Tavoitteet:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään sovellukseen elokuva-arvosteluja. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään elokuva-arvosteluja.

* Käyttäjä näkee sovellukseen lisätyt arvostelut. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät arvostelut.

* Käyttäjä pystyy etsimään arvosteluja hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä            arvosteluja.

* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät arvostelut.

* Käyttäjä pystyy valitsemaan arvostelulle/arvostelemalleen elokuvalle yhden tai useamman luokittelun (Elokuvan genre, julkaisuvuosi, arvosana). Mahdolliset luokat ovat tietokannassa.

* Sovelluksessa on pääasiallisen arvostelun lisäksi kommentteja, käyttäjä voi lisätä kommentteja omiin tai muiden arvosteluihin. 

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