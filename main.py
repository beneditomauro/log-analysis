#!/usr/bin/env python3
import psycopg2 as pg2
import datetime


try:
    conn = pg2.connect("dbname=news")
    cur = conn.cursor()
except pg2.Error as e:
    print(e)


def report():
    cur.execute("SELECT articles.title,"
                " COUNT(*) FROM articles "
                "INNER JOIN log ON '/article/' "
                "|| articles.slug = log.path "
                "GROUP"
                " BY articles.title "
                "ORDER BY COUNT DESC LIMIT 3 ")

    print("Top 3 most clicked article")
    for record in cur:
        print(" \""+str(record[0]) + " \"— "+str(record[1])+" views")

    print()

    cur.execute("SELECT authors.name, "
                "COUNT(*) FROM authors"
                " INNER JOIN articles"
                " ON articles.author = authors.id"
                " INNER JOIN log ON '/article/' || articles.slug = log.path"
                " GROUP BY authors.name"
                " ORDER BY COUNT DESC LIMIT 3")

    print("Top 3 most clicked authors")
    for record in cur:
        print("-"+str(record[0]) + "- " + str(record[1]) + " views")

    print()
    cur.execute("create or replace view number_of_clicks_good as "
                "SELECT Date(log.time), "
                "COUNT (log.time) AS numbers_good "
                "FROM log " 
                "GROUP BY Date(log.time); "
                "create or replace view number_of_clicks_bad as " 
                "SELECT Date(log.time), "
                "COUNT (log.time) AS numbers_bad "
                "FROM log "
                "WHERE log.status <> \'200 OK\' "
                "GROUP BY Date(log.time); "
                "SELECT number_of_clicks_good.date, "
                "((number_of_clicks_bad.numbers_bad::DECIMAL /number_of_clicks_good.numbers_good::DECIMAL) * 100) "
                "as errors "
                "FROM number_of_clicks_good "
                "FULL OUTER JOIN number_of_clicks_bad ON number_of_clicks_good.date=number_of_clicks_bad.date "
                "WHERE ((number_of_clicks_bad.numbers_bad::DECIMAL /number_of_clicks_good.numbers_good::DECIMAL) * 100)"
                " > 1.0 ")
    print("In which days more than 1% of the requests resulted in an error: ")
    for record in cur:
        monthinteger = int(str(record[0]).split("-")[1])  # extracting the month from the date string

        month = datetime.date(1900, monthinteger, 1).strftime('%B')  # using the date funciton to get the month from its representative integer
        print(" "+month + " " + str(record[0]).split("-")[2] + "- " + str(round(record[1], 2))+"%")


report()
