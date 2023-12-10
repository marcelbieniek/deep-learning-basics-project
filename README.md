# Music artist classification

An university project for Deep Learning Basics classes at 2nd semester of Informatics on Gdansk University of Technology.

## Project purpose

Project's target is to create deep learning model for classifying rock and metal bands using music samples.

List of currently supported bands:

* AC/DC
* Ensiferum
* Judas Priest
* Korn
* Korpiklaani
* Metallica
* Rammstein
* Slayer
* Slipknot
* System of a Down

## Dataset creation

To create dataset, they have been taken 5 random albums from each bands from list above.
File tree looks like this:

```txt
data/
- ACDC/
-- [1976] High Voltage/
--- 01. ACDC - It’s a Long Way to the Top (If You Wanna Rock ‘n’ Roll).mp3
--- 01. ACDC - Rock ‘n’ Roll Singer.mp3
--- ...
-- [1977] Let There Be Rock/
--- 01. ACDC - Go Down.mp3
--- 02. ACDC - Dog Eat Dog.mp3
--- ...
-- ...
- Ensiferum/
-- [2007] Victory Songs/
--- 01. Ensiferum - Ad Victoriam.mp3
--- 01. Ensiferum - Blood is the Price of Glory.mp3
--- ...
-- ...
- ...
```

Every metal band, album and song names have been converted to a snake_case but artist and song name are separated by dash.
