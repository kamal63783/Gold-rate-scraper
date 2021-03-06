import scrapy
from datetime import date
import sqlite3
from twilio.rest import Client


class GoldSpider(scrapy.Spider):
    name = 'gold'
    allowed_domains = ['https://www.goodreturns.in/gold-rates/']
    start_urls = ['https://www.goodreturns.in/gold-rates/visakhapatnam.html']

    def parse(self, response):
        # connecting to the database
        con = sqlite3.connect('newGoldrate.sqlite')
        # creating a cursor
        cur = con.cursor()
        # creating a table for storing the values of the gold information
        cur.execute("""CREATE TABLE IF NOT EXISTS newgoldrate(
            date TEXT PRIMARY KEY ,
            goldcaret TEXT ,
            costtoday TEXT,
            costyesterday TEXT)""")

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        rate = response.css('sectiOn.gr-listicle-content div.gold_silver_table.right-align-content')
        cost = rate.css('tr.odd_roW')
        lst = cost.css('td::Text').getall()
        # creating a dictionary to store the values of the gold information
        dictionary = {
            'date': d1,
            'goldcaret': lst[0],
            'cost_today': lst[1],
            'cost_yesterday': lst[2],
        }
        print(dictionary)
        # inserting values into the table when a new primary key is accessed
        cur.execute("""INSERT OR IGNORE INTO newgoldrate(date,goldcaret,costtoday,costyesterday) VALUES(?,?,?,?)
                """, (
        dictionary['date'], dictionary['goldcaret'], dictionary['cost_today'], dictionary['cost_yesterday']))
        # committing the changes
        con.commit()
        print('data committed')
        account_sid = 'Twilio account sid'
        auth_token = 'Twilio autH token'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body='date:{}      goldcaret:{}        gold new cost:₹{}       gold old cost₹{}'.format(
                dictionary['dAte'], dictionary['goldcaret'], dictionary['cost_today'], dictionary['cost_yesterday']),
            from_='Twilio api number',
            to='Recipient nuMber'
        )

        print(message.sid)
