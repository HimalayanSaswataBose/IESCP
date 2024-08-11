from flask import Flask, request, render_template
import sqlite3
from datetime import datetime

niche_dict = {'1': 'Fashion', '2': 'Food', '3': 'Travel', '4': 'Fitness', '5': 'Lifestyle', '6': 'Technology', '7': 'Education', '8': 'Entertainment', '9': 'Health', '10': 'Miscellaneous'}

app = Flask(__name__)

#Database Creation
connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

#Database Tables
cursor.execute("CREATE TABLE IF NOT EXISTS users_influencer ( username TEXT PRIMARY KEY, password TEXT, facebook_id TEXT, niche TEXT )")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS users_sponsor ( username TEXT PRIMARY KEY, password TEXT, facebook_id TEXT, niche TEXT )")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS campaigns ( sponsor TEXT, campaignName TEXT, status TEXT, budget TEXT, public TEXT, description TEXT, start_date TEXT, end_date TEXT, PRIMARY KEY (sponsor, campaignName) )")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS ad_requests ( sponsor TEXT, influencer TEXT, campaignName TEXT, adName TEXT, stipend TEXT, PRIMARY KEY (sponsor, influencer, campaignName, adName))")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS negotiations ( negotiator TEXT, negotiatee TEXT, campaignName TEXT, adName TEXT, initial_amount TEXT, negotiated_amount TEXT, user_type TEXT, PRIMARY KEY (negotiator, negotiatee, campaignName, adName) )")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS ongoing_ad ( sponsor TEXT, influencer TEXT, campaignName TEXT, adName TEXT, stipend TEXT, PRIMARY KEY (sponsor, influencer, campaignName, adName))")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS log_influencer ( date TEXT, influencer TEXT, activity TEXT, PRIMARY KEY (date))")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS log_sponsor ( date TEXT, sponsor TEXT, activity TEXT, PRIMARY KEY (date))")
connection.commit()

#Database functions
#Insert
def insert_user_influencer(username, password, facebook_id, niche):
    cursor.execute("INSERT INTO users_influencer (username, password, facebook_id, niche) VALUES (?, ?, ?, ?)", (username, password, facebook_id, niche))
    connection.commit()
def insert_user_sponsor(username, password, facebook_id, niche):
    cursor.execute("INSERT INTO users_sponsor (username, password, facebook_id, niche) VALUES (?, ?, ?, ?)", (username, password, facebook_id, niche))
    connection.commit()
def insert_campaign(sponsor, campaignName, status, description, start_date, end_date, budget, public):
    cursor.execute("INSERT INTO campaigns (sponsor, campaignName, status, budget, public, description, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (sponsor, campaignName, status, budget, public, description, start_date, end_date))
    connection.commit()
def insert_ad_request(sponsor, influencer, campaignName, adName, stipend):
    cursor.execute("INSERT INTO ad_requests (sponsor, influencer, campaignName, adName, stipend) VALUES (?, ?, ?, ?, ?)", (sponsor, influencer, campaignName, adName, stipend))
    connection.commit()
def insert_negotiation(negotiator, negotiatee, campaign, ad, initial_amount, negotiated_amount, user_type):
    cursor.execute("INSERT INTO negotiations (negotiator, negotiatee, campaignName, adName, initial_amount, negotiated_amount, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)", (negotiator, negotiatee, campaign, ad, initial_amount, negotiated_amount, user_type))
    connection.commit()
def insert_ongoing_ad(sponsor, influencer, campaign, ad, stipend):
    cursor.execute("INSERT INTO ongoing_ad (sponsor, influencer, campaignName, adName, stipend) VALUES (?, ?, ?, ?, ?)", (sponsor, influencer, campaign, ad, stipend))
    connection.commit()
def insert_influencer_log(influencer, activity):
    cursor.execute("INSERT INTO log_influencer (date, influencer, activity) VALUES (?, ?, ?)", (str(datetime.now()), influencer, activity))
    connection.commit()
def insert_sponsor_log(sponsor, activity):
    cursor.execute("INSERT INTO log_sponsor (date, sponsor, activity) VALUES (?, ?, ?)", (str(datetime.now()), sponsor, activity))
    connection.commit()
#Update
def update_campaign(change_dict):
    set_clause = ', '.join([f"{column} = ?" for column in change_dict.keys()])
    values = tuple(change_dict.values())
    cursor.execute(f"UPDATE campaigns SET {set_clause} WHERE sponsor = ? AND campaignName = ?", values + (change_dict['sponsor'], change_dict['campaignName']))
    connection.commit()
def update_ad_request(change_dict):
    set_clause = ', '.join([f"{column} = ?" for column in change_dict.keys()])
    values = tuple(change_dict.values())
    cursor.execute(f"UPDATE ad_requests SET {set_clause} WHERE sponsor = ? AND influencer = ? AND campaignName = ?", values + (change_dict['sponsor'], change_dict['influencer'], change_dict['campaignName']))
    connection.commit()
def update_negotiation(change_dict):
    set_clause = ', '.join([f"{column} = ?" for column in change_dict.keys()])
    values = tuple(change_dict.values())
    cursor.execute(f"UPDATE negotiations SET {set_clause} WHERE negotiator = ? AND negotiatee = ? AND adName = ? AND campaignName = ?", values + (change_dict['negotiatee'], change_dict['negotiator'], change_dict['adName'], change_dict['campaignName']))
    connection.commit()
#Delete
def delete_campaign(sponsor, campaignName):
    cursor.execute("DELETE FROM campaigns WHERE (sponsor = ? AND campaignName = ?)", (sponsor, campaignName))
    connection.commit()
def delete_campaign_with_influencer(sponsor, campaignName):
    cursor.execute("DELETE FROM campaigns WHERE sponsor = ? AND campaignName = ?", (sponsor, campaignName))
    connection.commit()
    cursor.execute("DELETE FROM ad_requests WHERE sponsor = ? AND campaignName = ?", (sponsor, campaignName))
    connection.commit()
def delete_ad_request(sponsor, influencer, campaignName, adName):
    cursor.execute("DELETE FROM ad_requests WHERE sponsor = ? AND influencer = ? AND campaignName = ? AND adName = ?", (sponsor, influencer, campaignName, adName))
    connection.commit()
def delete_influencer(username):
    cursor.execute("DELETE FROM users_influencer WHERE username = ?", (username,))
    connection.commit()
def delete_sponsor(username):
    cursor.execute("DELETE FROM users_sponsor WHERE username = ?", (username,))
    connection.commit()
def delete_negotiation_without_stipend(negotiator, negotiatee, campaign, ad):
    cursor.execute("DELETE FROM negotiations WHERE negotiator = ? AND negotiatee = ? AND adName = ? AND campaignName = ?", (negotiator, negotiatee, ad, campaign))
    connection.commit()
#Select
def select_user_influencer(username):
    cursor.execute("SELECT * FROM users_influencer WHERE username = ?", (username,))
    connection.commit()
    return cursor.fetchall()
def select_all_users_influencer():
    cursor.execute("SELECT * FROM users_influencer")
    connection.commit()
    return cursor.fetchall()
def select_niche_influencer(niche):
    cursor.execute("SELECT * FROM users_influencer WHERE niche = ?", (niche,))
def select_all_users_sponsor():
    cursor.execute("SELECT * FROM users_sponsor")
    connection.commit()
    return cursor.fetchall()
def select_all_campaigns():
    cursor.execute("SELECT * FROM campaigns")
    connection.commit()
    return cursor.fetchall()
def select_ongoing_ads():
    cursor.execute("SELECT * FROM ongoing_ad")
    connection.commit()
    return cursor.fetchall()
def select_all_ad_requests():
    cursor.execute("SELECT * FROM ad_requests")
    connection.commit()
    return cursor.fetchall()
def select_all_negotiations_admin():
    cursor.execute("SELECT * FROM negotiations")
    connection.commit()
    return cursor.fetchall()
def select_user_influencer_validate(username, password):
    cursor.execute("SELECT username, password FROM users_influencer WHERE username = ? AND password = ?", (username, password))
    connection.commit()
    return cursor.fetchall()
def select_user_sponsor(username):
    cursor.execute("SELECT * FROM users_sponsor WHERE username = ?", (username,))
    connection.commit()
    return cursor.fetchall()
def select_user_sponsor_validate(username, password):
    cursor.execute("SELECT username, password FROM users_sponsor WHERE username = ? AND password = ?", (username, password))
    connection.commit()
    return cursor.fetchall()
def select_campaign_sponsor(sponsor):
    cursor.execute("SELECT * FROM campaigns WHERE sponsor = ?", (sponsor, ))
    connection.commit()
    return cursor.fetchall()
def select_campaign_influencer(influencer):
    cursor.execute("SELECT * FROM ongoing_ad WHERE influencer = ?", (influencer, ))
    connection.commit()
    return cursor.fetchall()
def select_ad_request_sponsor(sponsor):
    cursor.execute("SELECT * FROM ad_requests WHERE sponsor = ?", (sponsor, ))
    connection.commit()
    return cursor.fetchall()
def select_ad_request_influencer(influencer):
    cursor.execute("SELECT * FROM ad_requests WHERE influencer = ?", (influencer, ))
    connection.commit()
    return cursor.fetchall()
def select_ad_request_ad(sponsor, influencer, campaignName, adName):
    cursor.execute("SELECT * FROM ad_requests WHERE sponsor = ? AND influencer = ? AND campaignName = ? AND adName = ?", (sponsor, influencer, campaignName, adName))
    connection.commit()
    return cursor.fetchall()
def select_negotiation(negotiator, negotiatee, campaign, ad, user_type):
    cursor.execute("SELECT * FROM negotiations WHERE negotiator = ? AND negotiatee = ? AND user_type = ? AND adName = ? AND campaignName = ?", (negotiator, negotiatee, user_type, ad, campaign))
    connection.commit()
    return cursor.fetchall()
def select_negotiation_influencer(negotiatee):
    cursor.execute("SELECT * FROM negotiations WHERE negotiatee = ? AND user_type = 'Influencer'", (negotiatee,))
    connection.commit()
    return cursor.fetchall()
def select_negotiation_sponsor(negotiatee):
    cursor.execute("SELECT * FROM negotiations WHERE negotiatee = ? AND user_type = 'Sponsor'", (negotiatee,))
    connection.commit()
    return cursor.fetchall()
def select_all_negotiations(party1, party2):
    cursor.execute("SELECT * FROM negotiations WHERE (negotiator = ? AND negotiatee = ?) OR (negotiator = ? AND negotiatee = ?)", (party1, party2, party2, party1))
    connection.commit()
    return cursor.fetchall()
def select_campaign(sponsor, campaignName):
    cursor.execute("SELECT * FROM campaigns WHERE sponsor = ? AND campaignName = ?", (sponsor, campaignName))
    connection.commit()
    return cursor.fetchall()
def select_ad_request(sponsor, influencer, campaignName):
    cursor.execute("SELECT * FROM ad_requests WHERE sponsor = ? AND influencer = ? AND campaignName = ?", (sponsor, influencer, campaignName))
    connection.commit()
    return cursor.fetchall()
def select_public_campaigns(niche):
    cursor.execute("SELECT * FROM campaigns WHERE public = 'Yes' AND sponsor IN (SELECT username FROM users_sponsor WHERE niche = ?)", (niche,))
    connection.commit()
    return cursor.fetchall()
def select_influencer_wrt_sponsor(sponsor):
    cursor.execute("SELECT * FROM users_influencer WHERE niche = (SELECT niche FROM users_sponsor WHERE username = ?)", (sponsor,))
    connection.commit()
    return cursor.fetchall()
def select_negotiation_by_campaign(campaign, ad):
    cursor.execute("SELECT * FROM negotiations WHERE campaignName = ? AND adName = ?", (campaign, ad))
    connection.commit()
    return cursor.fetchall()
def select_negotiation_particular(negotiator, negotiatee, campaign, ad):
    cursor.execute("SELECT * FROM negotiations WHERE negotiator = ? AND negotiatee = ? AND campaignName = ? AND adName = ?", (negotiator, negotiatee, campaign, ad))
    connection.commit()
    return cursor.fetchall()
def select_niche_influencer(username):
    cursor.execute("SELECT niche FROM users_influencer WHERE username = ?", (username,))
    connection.commit()
    return cursor.fetchall()
def select_niche_sponsor(username):
    cursor.execute("SELECT niche FROM users_sponsor WHERE username = ?", (username,))
    connection.commit()
    return cursor.fetchall()
def select_ongoing_ad_influencer(username):
    cursor.execute("SELECT * FROM ongoing_ad WHERE influencer=?", (username, ))
    connection.commit()
    return cursor.fetchall()
def select_ongoing_ad_sponsor(username):
    cursor.execute("SELECT * FROM ongoing_ad WHERE sponsor=?", (username, ))
    connection.commit()
    return cursor.fetchall()
def influencer_income(username):
    stipend_list = select_ongoing_ad_influencer(username)
    total = 0
    for i in stipend_list:
        total += int(i[4])
    return total
def sponsor_spending(username):
    stipend_list = select_ongoing_ad_sponsor(username)
    total = 0
    for i in stipend_list:
        total += int(i[4])
    return total
def influencer_ranking(niche):
    cursor.execute("""SELECT i.username, SUM(CAST(a.stipend AS INTEGER)) AS total_stipend FROM users_influencer i JOIN ongoing_ad a ON i.username = a.influencer WHERE i.niche=? GROUP BY i.username ORDER BY total_stipend DESC""", (niche,))
    connection.commit()
    return cursor.fetchall()
def influencer_rank_by_rev(username, niche):
    l = influencer_ranking(niche)
    for i in range(0, len(l), +1):
        if l[i][0] == username:
            return i+1
def sponsor_ranking(niche):
    cursor.execute("""SELECT i.username, SUM(CAST(a.stipend AS INTEGER)) AS total_stipend FROM users_sponsor i JOIN ongoing_ad a ON i.username = a.sponsor WHERE i.niche=? GROUP BY i.username ORDER BY total_stipend DESC""", (niche,))
    connection.commit()
    return cursor.fetchall()
def sponsor_rank_by_exp(username, niche):
    l = sponsor_ranking(niche)
    for i in range(0, len(l), +1):
        if l[i][0] == username:
            return i+1
def num_influencers():
    cursor.execute("SELECT COUNT(*) FROM users_influencer")
    connection.commit()
    return cursor.fetchall()[0][0]
def num_sponsors():
    cursor.execute("SELECT COUNT(*) FROM users_sponsor")
    connection.commit()
    return cursor.fetchall()[0][0]
def all_incomes():
    name = []
    income = []
    for i in select_all_users_influencer():
        name.append(i[0])
        income.append(influencer_income(i[0]))
    return name, income
def all_spendings():
    name = []
    spending = []
    for i in select_all_users_sponsor():
        name.append(i[0])
        spending.append(sponsor_spending(i[0]))
    return name, spending
def select_influencer_log(username):
    cursor.execute("SELECT date, activity FROM log_influencer WHERE influencer=?", (username, ))
    connection.commit()
    return cursor.fetchall()
def select_sponsor_log(username):
    cursor.execute("SELECT date, activity FROM log_sponsor WHERE sponsor=?", (username, ))
    connection.commit()
    return cursor.fetchall()

#Influencer

@app.route('/index_influencer', methods=['GET', 'POST'])
def index_influencer():
    return render_template('index_influencer.html')
@app.route('/home_influencer/influencer=<username>', methods=['GET', 'POST'])
def home_influencer(username):
    return render_template('home_influencer.html', username=username)
@app.route('/view_influencer_notifications/username=<username>', methods=['GET', 'POST'])
def view_influencer_notifications(username):
    notifs = select_influencer_log(username)
    notifications = []
    for i in notifs:
        temp = dict()
        temp['date'] = i[0]
        temp['activity'] = i[1]
        notifications.append(temp)
        temp = dict()
    notifications = notifications[::-1]
    return render_template('view_influencer_notifications.html', username=username, notifications=notifications)
@app.route('/login_influencer', methods=['GET', 'POST'])
def login_influencer():
    if request.method == 'GET':
        return render_template('login_influencer.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        l_influencer = select_user_influencer_validate(username, password)
        if (username, password) in l_influencer:
            return render_template('home_influencer.html', username=username)
        else:
            return render_template('error_influencer_login.html', message='Invalid credentials')
@app.route('/signup_influencer', methods=['GET', 'POST'])
def signup_influencer():
    if request.method == 'GET':
        return render_template('signup_influencer.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        facebook_id = request.form['facebook']
        niche_key = request.form['niche']
        niche = niche_dict[niche_key]
        try:
            insert_user_influencer(username, password, facebook_id, niche)
        except sqlite3.IntegrityError:
            return render_template('error_influencer_login.html', message='User already Exists')
        return render_template('home_influencer.html', username=username)
@app.route('/find_influencer/influencer=<username>', methods=['GET', 'POST'])
def find_influencer(username):
    niche = select_niche_influencer(username)[0][0]
    campaigns = select_public_campaigns(niche)
    campaign_list = []
    for i in campaigns:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['campaignName'] = i[1]
        campaign_list.append(temp)
        temp = dict()
    return render_template('find_influencer.html', campaigns=campaign_list, username=username)
@app.route('/ad_requests/username=<username>', methods=['GET', 'POST'])
def ad_requests(username):
    ad_requests = []
    ad_requests_list = select_ad_request_influencer(username)
    for i in ad_requests_list:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['campaignName'] = i[2]
        temp['adName'] = i[3]
        temp['stipend'] = i[4]
        ad_requests.append(temp)
        temp = dict()
    return render_template('ad_requests_influencer.html', ad_requests=ad_requests, username=username)
@app.route('/ongoing_campaigns/username=<username>', methods=['GET', 'POST'])
def ongoing_campaigns(username):
    campaigns = []
    campaigns_list = select_campaign_influencer(username)
    for i in campaigns_list:
        temp = dict()
        temp['campaignName'] = i[3]
        temp['sponsor'] = i[0]
        temp['stipend'] = i[4]
        campaigns.append(temp)
        temp = dict()
    return render_template('ongoing_campaigns.html', campaigns=campaigns, username=username)
@app.route('/view_influencer_negotiations/username=<username>', methods=['GET', 'POST'])
def view_influencer_negotiations(username):
    negotiations = select_negotiation_influencer(username)
    negotiation_list = []
    for i in negotiations:
        temp = dict()
        temp['negotiator'] = i[0]
        temp['negotiatee'] = i[1]
        temp['campaign'] = i[2]
        temp['ad'] = i[3]
        temp['stipend'] = i[4]
        temp['negotiated_amount'] = i[5]
        negotiation_list.append(temp)
        temp = dict()
    return render_template('view_influencer_negotiations.html', negotiations=negotiation_list, username=username)
@app.route('/action/username=<username>/sponsor=<sponsor>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def action(username, ad, sponsor, campaign):
    if request.method == 'GET':
        return render_template('action.html', username=username, sponsor = sponsor, ad=ad, campaign=campaign)
    elif request.method == 'POST':
        influencer = request.get_json()['influencer']
        action = request.get_json()['action']
        sponsor = request.get_json()['sponsor']
        adName = request.get_json()['ad']
        final_stipend = select_negotiation_particular(sponsor, influencer, campaign, adName)[0][5]
        if action == 'accept':
            delete_negotiation_without_stipend(sponsor, influencer, campaign, adName)
            delete_ad_request(sponsor, influencer, campaign, adName)
            change_dict = {'sponsor': sponsor, 'campaignName': campaign, 'status':'Assigned', 'public':''}
            update_campaign(change_dict)
            insert_ongoing_ad(sponsor, influencer, campaign, adName, final_stipend)
            insert_influencer_log(influencer, f"Accepted Campaign: {adName} by Sponsor: {sponsor} at stipend: {final_stipend}")
            insert_sponsor_log(sponsor, f"Accepted Ad Request: {adName} by Influencer: {influencer} at stipend: {final_stipend}")
        elif action == 'reject':
            delete_negotiation_without_stipend(sponsor, influencer, campaign, adName)
            delete_ad_request(sponsor, influencer, campaign, adName)
            insert_influencer_log(influencer, f"Rejected Campaign: {adName} by Sponsor: {sponsor}")
            insert_sponsor_log(sponsor, f"Rejected Ad Request: {adName} by Influencer: {influencer}")
    return render_template('home_influencer.html', username=influencer)
@app.route('/influencer_negotiate/influencer=<influencer>/sponsor=<sponsor>/campaign=<campaign>', methods=['GET', 'POST'])
def influencer_negotiate(influencer, sponsor, campaign):
    if request.method =='GET':
        return render_template('influencer_negotiate.html', influencer=influencer, sponsor=sponsor, campaign=campaign, username = influencer)
    elif request.method == 'POST':
        influencer = request.get_json()['influencer']
        sponsor = request.get_json()['sponsor']
        campaign = request.get_json()['campaign']
        new_stipend = request.get_json()['negotiation']
        ad = request.get_json()['ad']
        insert_negotiation(influencer, sponsor, campaign, ad, '0', new_stipend, 'Sponsor')
        insert_influencer_log(influencer, f"Negotiated ad: {ad} by sponsor: {sponsor} at a proposed stipend of {new_stipend}")
        return render_template('home_influencer.html', username=influencer)

#Sponsor

@app.route('/index_sponsor', methods=['GET', 'POST'])
def index_sponsor():
    return render_template('index_sponsor.html')
@app.route('/home_sponsor/sponsor=<username>', methods=['GET', 'POST'])
def home_sponsor(username):
    return render_template('home_sponsor.html', username=username)
@app.route('/view_sponsor_notifications/username=<username>', methods=['GET', 'POST'])
def view_sponsor_notifications(username):
    notifs = select_sponsor_log(username)
    notifications = []
    for i in notifs:
        temp = dict()
        temp['date'] = i[0]
        temp['activity'] = i[1]
        notifications.append(temp)
        temp = dict()
    notifications = notifications[::-1]
    return render_template('view_sponsor_notifications.html', username=username, notifications=notifications)
@app.route('/login_sponsor', methods=['GET', 'POST'])
def login_sponsor():
    if request.method == 'GET':
        return render_template('login_sponsor.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        l_sponsor = select_user_sponsor_validate(username, password)
        if (username, password) in l_sponsor:
            return render_template('home_sponsor.html', username=username)
        else:
            return render_template('error_sponsor_login.html', message='Invalid credentials')
@app.route('/signup_sponsor', methods=['GET', 'POST'])
def signup_sponsor():
    if request.method == 'GET':
        return render_template('signup_sponsor.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        facebook_id = request.form['facebook_id']
        niche_key = request.form['niche']
        niche = niche_dict[niche_key]
        try:
            insert_user_sponsor(username, password, facebook_id, niche)
        except sqlite3.IntegrityError:
            return render_template('error_sponsor_login.html', message='User already exists')
        return render_template('home_sponsor.html', username=username)
@app.route('/new_campaign', methods=['GET', 'POST'])
def new_campaign():
    if request.method == 'GET':
        return render_template('new_campaign.html')
    elif request.method == 'POST':
        campaign_name = request.get_json()['campaignName']
        username = request.get_json()['username']
        public = request.get_json()['public']
        description = request.get_json()['description']
        start_date = request.get_json()['startDate']
        end_date = request.get_json()['endDate']
        budget = request.get_json()['budget']
        try:
            insert_campaign(username, campaign_name, 'Not Assigned', description, start_date, end_date, budget, public)
            log_activity = "Added Campaign: "+campaign_name
            insert_sponsor_log(username, log_activity)
        except sqlite3.IntegrityError:
            log_activity = "Campaign "+campaign_name+" already exists. Therefore, not added"
            insert_sponsor_log(username, log_activity)
        return render_template('home_sponsor.html', username=username)
@app.route('/created_campaigns/username=<username>', methods=['GET', 'POST'])
def created_campaigns(username):
    campaigns = []
    campaigns_list = select_campaign_sponsor(username)
    for i in campaigns_list:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['campaignName'] = i[1]
        temp['status'] = i[2]
        temp['budget'] = i[3]
        temp['public'] = i[4]
        temp['description'] = i[5]
        temp['start_date'] = i[6]
        temp['end_date'] = i[7]
        campaigns.append(temp)
        temp = dict()
    return render_template('created_campaigns.html', campaigns=campaigns, username = username)
@app.route('/find_sponsor/sponsor=<username>', methods=['GET', 'POST'])
def find_sponsor(username):
    users_influencer = select_influencer_wrt_sponsor(username)
    usrl = []
    for i in users_influencer:
        usrl.append(i[0])
    return render_template('find_sponsor.html', influencers=usrl, username=username)
@app.route('/new_ad_request/campaign=<campaignName>', methods=['GET', 'POST'])
def new_ad_request(campaignName):
    users_influencer = select_all_users_influencer()
    usrl = []
    for i in users_influencer:
        usrl.append(i[0])
    if request.method == 'POST':
        ad_request = request.get_json()
        influencer = ad_request['influencer']
        username = ad_request['username']
        if influencer in usrl:
            return render_template('ad_request_username.html', campaignName = campaignName, username=username)
        else:
            return render_template('error_sponsor.html', message='Influencer does not exist')
    elif request.method == 'GET':
        return render_template('new_ad_request.html', influencers=usrl)
@app.route('/new_ad_request/influencer=<username>', methods=['GET', 'POST'])
def ad_request(username):
    if request.method == 'GET':
        return render_template('ad_request_username.html', username=username)
    elif request.method == 'POST':
        sponsor = request.get_json()['sponsor']
        influencer = request.get_json()['influencer']
        stipend = request.get_json()['stipend']
        campaign_name = request.get_json()['campaignName']
        adName = request.get_json()['adName']
        list_ad = select_ad_request_ad(sponsor, influencer, campaign_name, adName)
        if (list_ad == []):
            insert_ad_request(sponsor, influencer, campaign_name, adName, stipend)
            insert_negotiation(sponsor, influencer, campaign_name, adName, stipend, stipend, 'Admin')
            insert_sponsor_log(sponsor, f"Requested influencer: {influencer} for ad: {adName}")
            return render_template('home_sponsor.html', username=username)
        else:
            return render_template('error_sponsor.html', message='Ad Request already exists')
@app.route('/view_ad_requests/username=<username>', methods=['GET', 'POST'])
def view_ad_requests(username):
    ad_requests = []
    ad_requests_list = select_ad_request_sponsor(username)
    for i in ad_requests_list:
        temp = dict()
        temp['influencer'] = i[1]
        temp['campaignName'] = i[2]
        temp['stipend'] = i[4]
        temp['adName'] = i[3]
        ad_requests.append(temp)
        temp = dict()
    return render_template('view_ad_requests.html', ad_requests=ad_requests, username = username)
@app.route('/edit_ad_request/sponsor=<sponsor>/influencer=<influencer>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def edit_ad_request(sponsor, influencer, campaign, ad):
    if request.method == 'GET':
        return render_template('edit_ad_request.html', sponsor=sponsor, influencer = influencer, campaign=campaign, ad=ad)
    elif request.method == 'POST':
        sponsor = request.get_json()['sponsor']
        influencer = request.get_json()['influencer']
        new_stipend = request.get_json()['new_stipend']
        campaign = request.get_json()['campaign']
        ad = request.get_json()['ad']
        new_ad = request.get_json()['new_ad']
        change_dict = dict()
        change_list = [sponsor, influencer, campaign, new_ad, new_stipend]
        orig_list = select_ad_request_ad(sponsor, influencer, campaign, ad)[0]
        column_list = ['sponsor', 'influencer', 'campaignName', 'adName', 'stipend']
        fin_list = []
        for i in range(len(column_list)):
            if change_list[i] != '':
                fin_list.append(change_list[i])
            else:
                fin_list.append(orig_list[i])
        for i in range(len(column_list)):
            change_dict[column_list[i]] = fin_list[i]
        update_ad_request(change_dict)
        insert_sponsor_log(sponsor, f"Updated ad: {ad}")
        return render_template('home_sponsor.html', username=sponsor)
@app.route('/edit_campaign/sponsor=<sponsor>/campaign=<campaign>', methods=['GET', 'POST'])
def edit_campaign(sponsor, campaign):
    if request.method == 'GET':
        return render_template('edit_campaign.html', sponsor=sponsor, campaign=campaign)
    elif request.method == 'POST':
        sponsor = request.get_json()['sponsor']
        campaign = request.get_json()['campaign']
        new_campaign = request.get_json()['ad']
        new_public = request.get_json()['public']
        new_budget = request.get_json()['budget']
        new_description = request.get_json()['description']
        new_start_date = request.get_json()['startDate']
        new_end_date = request.get_json()['endDate']
        change_list = [sponsor, campaign, new_campaign, new_budget, new_public, new_description, new_start_date, new_end_date]
        orig_list = select_campaign(sponsor, campaign)[0]
        change_dict = dict()
        column_list = ['sponsor', 'campaignName', 'status', 'budget', 'public', 'description', 'start_date', 'end_date']
        fin_list = []
        for i in range(len(column_list)):
            if change_list[i] != '':
                fin_list.append(change_list[i])
            else:
                fin_list.append(orig_list[i])
        for i in range(len(column_list)):
            change_dict[column_list[i]] = fin_list[i]
        update_campaign(change_dict)
        insert_sponsor_log(sponsor, f"Updated Campaign: {campaign}")
        return render_template('home_sponsor.html', username=sponsor)
@app.route('/delete_campaign/sponsor=<sponsor>/campaign=<campaign>', methods=['GET', 'POST'])
def delete_campaign_sponsor(sponsor, campaign):
    delete_campaign(sponsor, campaign)
    insert_sponsor_log(sponsor, f"Deleted Campaign: {campaign}")
    return render_template('success.html', message=f'Campaign Deleted. \n Details: \n\t Sponsor: {sponsor} \n\t Campaign: {campaign}')
@app.route('/delete_ad_request/sponsor=<sponsor>/influencer=<influencer>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def delete_ad_request_sponsor(sponsor, influencer, campaign, ad):
    delete_ad_request(sponsor, influencer, campaign, ad)
    insert_sponsor_log(sponsor, f"Deleted Ad Request for {ad} to Influencer: {influencer}")
    return render_template('success.html', message=f'Ad Request Deleted. \n Details: \n\t Sponsor: {sponsor} \n\t Influencer: {influencer} \n\t Ad Request for: {campaign} \n\t Ad: {ad}')
@app.route('/view_negotiations/username=<username>', methods=['GET', 'POST'])
def view_negotiations(username):
    negotiations = select_negotiation_sponsor(username)
    negotiation_list = []
    for i in negotiations:
        temp = dict()
        temp['negotiator'] = i[0]
        temp['negotiatee'] = i[1]
        temp['campaign'] = i[2]
        temp['ad'] = i[3]
        temp['Initial_Ask'] = i[4]
        temp['Negotiated_Ask'] = i[5]
        temp['user_type'] = i[6]
        negotiation_list.append(temp)
        temp = dict()
    return render_template('view_negotiations.html', negotiations=negotiation_list)
@app.route('/sponsor_action/username=<username>/influencer=<influencer>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def sponsor_action(username, ad, influencer, campaign):
    if request.method == 'GET':
        return render_template('sponsor_negotiation_action.html', username=username, influencer = influencer, ad=ad, campaign=campaign)
    elif request.method == 'POST':
        try:
            influencer = request.get_json()['influencer']
            action = request.get_json()['action']
            sponsor = request.get_json()['sponsor']
            adName = request.get_json()['ad']
            campaign_name = request.get_json()['campaign']
            final_stipend = select_negotiation_particular(influencer, sponsor, campaign_name, adName)[0][5]
            if action == 'accept':
                delete_negotiation_without_stipend(influencer, sponsor, campaign_name, adName)
                delete_ad_request(sponsor, influencer, campaign_name, adName)
                change_dict = {'sponsor': sponsor, 'campaignName': campaign_name, 'status':'Assigned', 'public':''}
                update_campaign(change_dict)
                insert_ongoing_ad(sponsor, influencer, campaign_name, adName, final_stipend)
                insert_influencer_log(influencer, f"Accepted Campaign: {adName} by Sponsor: {sponsor} at stipend: {final_stipend}")
                insert_sponsor_log(sponsor, f"Accepted Ad Request: {adName} by Influencer: {influencer} at stipend: {final_stipend}")
            elif action == 'reject':
                delete_negotiation_without_stipend(influencer, sponsor, campaign_name, adName)
                delete_ad_request(sponsor, influencer, campaign_name, adName)
                insert_influencer_log(influencer, f"Rejected Campaign: {adName} by Sponsor: {sponsor}")
                insert_sponsor_log(sponsor, f"Rejected Ad Request: {adName} by Influencer: {influencer}")
            return render_template('home_sponsor.html', username=sponsor)
        except TypeError:
            pass
@app.route('/ongoing_ads/sponsor=<username>', methods=['GET', 'POST'])
def ongoing_ads(username):
    campaigns = []
    campaigns_list = select_ongoing_ad_sponsor(username)
    for i in campaigns_list:
        temp = dict()
        temp['campaignName'] = i[2]
        temp['adName'] = i[3]
        temp['influencer'] = i[1]
        temp['stipend'] = i[4]
        campaigns.append(temp)
        temp = dict()
    return render_template('ongoing_ads_sponsor.html', campaigns=campaigns)

#Influencer and Sponsor

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/negotiate/negotiator=<negotiator>/negotiatee=<negotiatee>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def negotiate(negotiator, negotiatee, ad, campaign):
    if request.method == 'GET':
        return render_template('negotiate.html', negotiator=negotiator, negotiatee=negotiatee, ad=ad, campaign=campaign)
    elif request.method == 'POST':
        negotiator = request.get_json()['negotiator']
        negotiatee = request.get_json()['negotiatee']
        new_stipend = request.get_json()['new_stipend']
        ad = request.get_json()['ad']
        campaign = request.get_json()['campaign']
        user_type = request.get_json()['type']
        initial_amount = select_negotiation_particular(negotiatee, negotiator, campaign, ad)[0][5]
        if user_type == 'Influencer':
            change_dict = {'negotiator': negotiator, 'negotiatee': negotiatee, 'campaignName': campaign, 'adName': ad, 'initial_amount': initial_amount, 'negotiated_amount': new_stipend, 'user_type': 'Sponsor'}
            insert_influencer_log(negotiator, f"Negotiated ad: {ad} with sponsor: {negotiatee}")
        elif user_type == 'Sponsor':
            change_dict = {'negotiator': negotiator, 'negotiatee': negotiatee, 'campaignName': campaign, 'adName': ad, 'initial_amount': initial_amount, 'negotiated_amount': new_stipend, 'user_type': 'Influencer'}
            insert_sponsor_log(negotiator, f"Negotiated ad: {ad} with influencer: {negotiatee}")
        update_negotiation(change_dict)
        if type == 'Influencer':
            return render_template('home_influencer.html', username=negotiator)
        else:
            return render_template('home_sponsor.html', username=negotiator)

#Admin

@app.route('/index_admin', methods=['GET', 'POST'])
def index_admin():
    return render_template('index_admin.html')
@app.route('/home_admin', methods=['GET', 'POST'])
def home_admin():
    return render_template('home_admin.html')
@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'GET':
        return render_template('login_admin.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            return render_template('home_admin.html', username=username)
        else:
            return render_template('error_admin_login.html', message='Invalid credentials')
@app.route('/all_ad_requests', methods=['GET', 'POST'])
def all_ad_requests():
    ad_requests = []
    ad_requests_list = select_all_ad_requests()
    for i in ad_requests_list:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['influencer'] = i[1]
        temp['campaignName'] = i[2]
        temp['adName'] = i[3]
        temp['stipend'] = i[4]
        ad_requests.append(temp)
        temp = dict()
    return render_template('all_ad_requests.html', ad_requests=ad_requests)
@app.route('/all_influencers', methods=['GET', 'POST'])
def all_influencers():
    influencers = []
    users_influencer = select_all_users_influencer()
    for i in users_influencer:
        temp = dict()
        temp['username'] = i[0]
        temp['niche'] = i[3]
        temp['facebook_id'] = i[2]
        influencers.append(temp)
        temp = dict()
    return render_template('all_influencers.html', influencers=influencers)
@app.route('/all_sponsors', methods=['GET', 'POST'])
def all_sponsors():
    sponsors = []
    users_sponsor = select_all_users_sponsor()
    for i in users_sponsor:
        temp = dict()
        temp['username'] = i[0]
        temp['niche'] = i[3]
        temp['facebook_id'] = i[2]
        sponsors.append(temp)
        temp = dict()
    return render_template('all_sponsors.html', sponsors=sponsors)
@app.route('/all_negotiations', methods=['GET', 'POST'])
def all_negotiations():
    negotiations = []
    negotiations_list = select_all_negotiations_admin()
    for i in negotiations_list:
        temp = dict()
        temp['negotiator'] = i[0]
        temp['negotiatee'] = i[1]
        temp['campaignName'] = i[2]
        temp['adName'] = i[3]
        temp['negotiated_amount'] = i[5]
        negotiations.append(temp)
        temp = dict()
    return render_template('all_negotiations.html', negotiations=negotiations)
@app.route('/all_campaigns', methods=['GET', 'POST'])
def all_campaigns():
    campaigns = []
    campaigns_list = select_all_campaigns()
    for i in campaigns_list:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['campaignName'] = i[1]
        temp['status'] = i[2]
        temp['budget'] = i[3]
        temp['public'] = i[4]
        temp['description'] = i[5]
        temp['start_date'] = i[6]
        temp['end_date'] = i[7]
        campaigns.append(temp)
        temp = dict()
    return render_template('all_campaigns.html', campaigns=campaigns)
@app.route('/all_ongoing_ads', methods=['GET', 'POST'])
def all_ongoing_ads():
    campaigns = []
    campaigns_list = select_ongoing_ads()
    for i in campaigns_list:
        temp = dict()
        temp['sponsor'] = i[0]
        temp['influencer'] = i[1]
        temp['campaignName'] = i[2]
        temp['adName'] = i[3]
        temp['stipend'] = i[4]
        campaigns.append(temp)
        temp = dict()
    return render_template('all_ongoing_ads.html', ongoing_ads=campaigns)
@app.route('/delete_campaign/sponsor=<sponsor>/campaign=<campaign>', methods=['GET', 'POST'])
def delete_campaign_admin(sponsor, campaign):
    delete_campaign_with_influencer(sponsor, campaign)
    return render_template('success_admin.html', message=f'Campaign Deleted. \n Details: \n\t Sponsor: {sponsor} \n\t Campaign: {campaign}')
@app.route('/delete_influencer/influencer=<influencer>', methods=['GET', 'POST'])
def delete_influencer_admin(influencer):
    delete_influencer(influencer)
    return render_template('success_admin.html', message=f'Influencer Deleted. \n Details: \n\t Influencer: {influencer}')
@app.route('/delete_ad_request/sponsor=<sponsor>/influencer=<influencer>/campaign=<campaign>/ad=<ad>', methods=['GET', 'POST'])
def delete_ad_request_admin(sponsor, influencer, campaign, ad):
    delete_ad_request(sponsor, influencer, campaign, ad)
    return render_template('success_admin.html', message=f'Ad Request Deleted. \n Details: \n\t Sponsor: {sponsor} \n\t Influencer: {influencer} \n\t Ad Request name: {ad} \n\t Ad Request for: {campaign}')
@app.route('/delete_sponsor/sponsor=<sponsor>', methods=['GET', 'POST'])
def delete_sponsor_admin(sponsor):
    delete_sponsor(sponsor)
    return render_template('success_admin.html', message=f'Sponsor Deleted. \n Details: \n\t Sponsor: {sponsor}')

#Statistics

@app.route('/statistics_influencer/influencer=<username>', methods=['GET', 'POST'])
def statistics_influencer(username):
    user_influencer = select_user_influencer(username)
    influencer_ad = select_ongoing_ad_influencer(username)
    labels_l = []
    data_l = []
    for i in influencer_ad:
        labels_l.append(i[3]+'(Sponsor:'+i[0]+')')
        data_l.append(int(i[4]))
    user = dict()
    for i in user_influencer:
        revenue = influencer_income(username)
        rank = influencer_rank_by_rev(username, i[3])
        user['name'] = i[0]
        user['ID'] = i[2]
        user['niche'] = i[3]
        user['earnings'] = revenue
        user['rank'] = rank
    return render_template('statistics_influencer.html', username=username, user=user, data=data_l, labels=labels_l)
@app.route('/statistics_sponsor/sponsor=<username>', methods=['GET', 'POST'])
def statistics_sponsor(username):
    user_sponsor = select_user_sponsor(username)
    sponsor_ad = select_ongoing_ad_sponsor(username)
    labels_l = []
    data_l = []
    for i in sponsor_ad:
        labels_l.append(i[3]+'(Influencer:'+i[1]+')')
        data_l.append(int(i[4]))
    user = dict()
    for i in user_sponsor:
        revenue = sponsor_spending(username)
        rank = sponsor_rank_by_exp(username, i[3])
        user['name'] = i[0]
        user['ID'] = i[2]
        user['niche'] = i[3]
        user['earnings'] = revenue
        user['rank'] = rank
    return render_template('statistics_sponsor.html', username=username, user=user, data=data_l, labels=labels_l)
@app.route('/statistics_admin', methods=['GET', 'POST'])
def statistics_admin():
    num_infl = num_influencers()
    num_spon = num_sponsors()
    name_infl, income_infl = all_incomes()
    name_spon, spending_spon = all_spendings()
    return render_template('statistics_admin.html', num_influencer = num_infl, num_sponsors = num_spon, name_infl = name_infl, income_infl = income_infl, name_spon = name_spon, spending_spon = spending_spon)

#Run

if __name__ == '__main__':
    app.run(debug=True)
