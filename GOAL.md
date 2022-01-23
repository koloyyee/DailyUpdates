# Goal of this project

This goal of this project is to have a desktop notification when something happened.

For example, at 6:45 am the python programme will fetch the news headlines and notify me, or I have something from the google calendar.

The goal is to create a notifier for fun.

## packages

pynotifier, urllib3, beautifulsoup4, python-crontab

- urllib3 and beautifulsoup4 are for scraping news
- pynotifier for desktop notification
- python-crontab for cron job, a daily update on the news

TODO list

- [x] showing list of news on the frontend.
- [x] deploy to heroku or linode.
- [x] setup an auto scrape cron job.
- [x] scrape and directly insert into sqlite3 db
- [x] populate agency data
- [ ] need pagination
- [ ] add custom domain
- [ ] add ssl
- [ ] write test
- [ ] In the agency form, include which category does the user want to fetch if there are any.
- [ ] add register button
- [ ] clean last "/" before inserting into db
- [ ] Add text editor or markdown editor
- [ ] Add login system
