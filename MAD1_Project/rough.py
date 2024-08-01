'''import sqlite3
#Database Creation
connection = sqlite3.connect('database.db')
cursor = connection.cursor()'''
'''
#Database Tables
cursor.execute("""CREATE TABLE IF NOT EXISTS users_influencer (
               username TEXT PRIMARY KEY,
               password TEXT
               )""")
connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS users_sponsor (
               username TEXT PRIMARY KEY,
               password TEXT
               )""")
connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS campaigns (
               sponsor TEXT,
               campaignName TEXT,
               influencer TEXT,
               stipend TEXT,
               public TEXT
               )""")
connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS ad_requests (
               sponsor TEXT,
               influencer TEXT,
               campaignName TEXT,
               stipend TEXT
               )""")
connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS negotiations (
               negotiator TEXT,
               negotiatee TEXT,
               ad TEXT,
               stipend TEXT,
               negotiated_amount TEXT,
               user_type TEXT
               )""")

#Database functions
#Insert
def insert_user_influencer(username, password):
    with cursor:
        cursor.execute("INSERT INTO users_influencer (username, password) VALUES (?, ?)", (username, password))
def insert_user_sponsor(username, password):
    with cursor:
        cursor.execute("INSERT INTO users_sponsor (username, password) VALUES (?, ?)", (username, password))
def insert_campaign(sponsor, campaignName, influencer, stipend, public):
    with cursor:
        cursor.execute("INSERT INTO campaigns (sponsor, campaignName, influencer, stipend, public) VALUES (?, ?, ?, ?, ?)", (sponsor, campaignName, influencer, stipend, public))
def insert_ad_request(sponsor, influencer, campaignName, stipend):
    with cursor:
        cursor.execute("INSERT INTO ad_requests (sponsor, influencer, campaignName, stipend) VALUES (?, ?, ?, ?)", (sponsor, influencer, campaignName, stipend))
def insert_negotiation(negotiator, negotiatee, ad, stipend, negotiated_amount, user_type):
    with cursor:
        cursor.execute("INSERT INTO negotiations (negotiator, negotiatee, ad, stipend, negotiated_amount, user_type) VALUES (?, ?, ?, ?, ?, ?)", (negotiator, negotiatee, ad, stipend, negotiated_amount, user_type))
#Update
def update_campaign(sponsor, campaignName, influencer, stipend, public):
    with cursor:
        cursor.execute("UPDATE campaigns SET influencer = ?, stipend = ?, public = ? WHERE sponsor = ? AND campaignName = ?", (influencer, stipend, public, sponsor, campaignName))
def update_ad_request(sponsor, influencer, campaignName, stipend):
    with cursor:
        cursor.execute("UPDATE ad_requests SET stipend = ? WHERE sponsor = ? AND influencer = ? AND campaignName = ?", (stipend, sponsor, influencer, campaignName))
#Delete
def delete_campaign(sponsor, campaignName, influencer):
    with cursor:
        cursor.execute("DELETE FROM campaigns WHERE sponsor = ? AND campaignName = ? AND influencer = ?", (sponsor, campaignName, influencer))
def delete_ad_request(sponsor, influencer, campaignName):
    with cursor:
        cursor.execute("DELETE FROM ad_requests WHERE sponsor = ? AND influencer = ? AND campaignName = ?", (sponsor, influencer, campaignName))
def delete_influencer(username):
    with cursor:
        cursor.execute("DELETE FROM users_influencer WHERE username = ?", (username,))
def delete_sponsor(username):
    with cursor:
        cursor.execute("DELETE FROM users_sponsor WHERE username = ?", (username,))
#Select
def select_user_influencer(username):
    with cursor:
        cursor.execute("SELECT * FROM users_influencer WHERE username = ?", (username,))
        return cursor.fetchall()
def select_user_sponsor(username):
    with cursor:
        cursor.execute("SELECT * FROM users_sponsor WHERE username = ?", (username,))
        return cursor.fetchall()
def select_campaign_sponsor(sponsor):
    with cursor:
        cursor.execute("SELECT * FROM campaigns WHERE sponsor = ?", (sponsor, ))
        return cursor.fetchall()
def select_campaign_influencer(influencer):
    with cursor:
        cursor.execute("SELECT * FROM campaigns WHERE influencer = ?", (influencer, ))
        return cursor.fetchall()
def select_ad_request_sponsor(sponsor):
    with cursor:
        cursor.execute("SELECT * FROM ad_requests WHERE sponsor = ?", (sponsor, ))
        return cursor.fetchall()
def select_ad_request_influencer(influencer):
    with cursor:
        cursor.execute("SELECT * FROM ad_requests WHERE influencer = ?", (influencer, ))
        return cursor.fetchall()
def select_negotiation(negotiator, negotiatee):
    with cursor:
        cursor.execute("SELECT * FROM negotiations WHERE negotiator = ? AND negotiatee = ?", (negotiator, negotiatee))
        return cursor.fetchall()
def select_campaign(sponsor, campaignName):
    with cursor:
        cursor.execute("SELECT * FROM campaigns WHERE sponsor = ? AND campaignName = ?", (sponsor, campaignName))
        return cursor.fetchall()
def select_ad_request(sponsor, influencer, campaignName):
    with cursor:
        cursor.execute("SELECT * FROM ad_requests WHERE sponsor = ? AND influencer = ? AND campaignName = ?", (sponsor, influencer, campaignName))
        return cursor.fetchall()
'''
# cursor.execute("DROP TABLE negotiations")
'''cursor.execute("""CREATE TABLE IF NOT EXISTS negotiations (
               negotiator TEXT,
               negotiatee TEXT,
               ad TEXT,
               negotiated_amount TEXT,
               user_type TEXT
               )""")
connection.commit()'''
'''cursor.execute("SELECT * FROM users_influencer")
print(cursor.fetchall())
connection.commit()'''
'''cursor.execute("""delete   from ongoing_ad
where    rowid not in
         (
         select  min(rowid)
         from    ongoing_ad
         )""")
connection.commit()'''
'''cursor.execute("""
DELETE FROM negotiations
               """)
connection.commit()'''
'''from datetime import datetime
print(str(datetime.now()))'''

def prefixes_div_by_5(codes):
    result = []
    current_value = 0
    
    for bit in codes:
        current_value = (current_value * 2 + bit) % 5
        result.append(current_value == 0)
    
    return result

# Example usage:
codes = [1,0,1]
print(prefixes_div_by_5(codes))  # Output: [True, False, False, False, True, False]
