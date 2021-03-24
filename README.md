# zeraignment
Zerodha assignment

## Demo link - https://marketinfo-bse.herokuapp.com/bhavcopy
### Features
-  Displays the data related to stock based on stock name provided by user.
-  If the current data is not available it fetches the previous day's data and displays according to the user query.
-  User can download their search result as a csv file by click on the download link provided.
-  If both current and previous data is not available or if the stock name is not present in DB no records are displayed.
-  The App tries to fetch the current day data from https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx endpoit at 18:00 IST everyday.

## Running locally - 
- Clone this repo and cd into zeraignment/
- Run `pip install -r requirements.txt`
- Then run `python manage.py migrate`
- `python manage.py collectstatic`
- Set `marketinfo/settings.py` set `DOCKER = False`
- Then finally `python manage.py runserver localhost:8000`, then type http://localhost:8000/bhavcopy/ in your browser to view this app.

## Running using docker-compose -
- If you want to run this app using docker-compose create a folder called marketinfo and move bhavcopyapp, db.sqlite3, manage.py, marketinfo, media
inside the create directory. In `marketinfo/settings.p`y set `DOCKER = True`
- Then run `sudo docker-compose up --build`, then type http://localhost:8000/bhavcopy/ in your browser to view this app.
