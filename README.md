# Logs Analysis
_______________________
## The Application
This python command line app is used to reproduce some metrics about a log table of a website. Those metrics beign
- Most clicked articles
- Most famous authors
- The days that more than 1% of requests led to an error.

## Tech/framework used

<b>Built with</b>
- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [PostgreSQL](https://www.postgresql.org//)

## How to use?
Download the SQL data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
Run the following comand in the directory of the db:
  -"psql -d news -f newsdata.sql".
Execute the code.


### Adicional Info
When reproducing the last metric I created two views with the respective comands:

create or replace view number_of_clicks_good as
SELECT Date(log.time), COUNT (log.time) AS numbers_good
FROM log
GROUP BY Date(log.time);

create or replace view number_of_clicks_bad as
SELECT Date(log.time),
COUNT (log.time) AS numbers_bad
FROM log
WHERE log.status <> '200 OK'
GROUP BY Date(log.time);

Being the first view the overall requests and the other the requests that led to an error
