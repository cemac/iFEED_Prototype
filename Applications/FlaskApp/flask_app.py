"""Routes for core Flask app."""
from flask import current_app as app
from flask import render_template, flash, redirect, url_for, request
from flask import session, abort, Blueprint
import sqlite3
import pandas as pd
import os
from passlib.hash import sha256_crypt
# Modules for this site
from .access import ChangePwdForm, AccessForm
from .access import table_list, user_login
from .access import is_logged_in, is_logged_in_as_admin
from .access import InsertUser, DeleteUser, AssignRole

# Connect to database
DATABASE = '/var/www/development/iFEED.db'
#DATABASE = os.path.join(os.getcwd(),'iFEED.db')
assert os.path.exists(DATABASE), "Unable to locate database"
app.secret_key = 'secret'
conn = sqlite3.connect(DATABASE, check_same_thread=False)
counter = 1

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/', methods=["GET"])
def index():
    """Landing page."""
    return render_template('home.html.j2')

@main_bp.route("/")
def hitcounter():
    global counter
    counter += 1
    return str(counter)

# Access ----------------------------------------------------------------------

# Login
@main_bp.route('/login', methods=["GET", "POST"])
def login():
    if 'logged_in' in session:
        flash('Already logged in', 'warning')
        return redirect(url_for('main_bp.index'))
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        user_login(username, password_candidate, conn)
        return redirect(url_for('main_bp.index'))
    if request.method == 'GET':
        return render_template('login.html.j2')


# Logout
@main_bp.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('main_bp.index'))


# Change password
@main_bp.route('/change-pwd', methods=["GET", "POST"])
@is_logged_in
def change_pwd():
    username = session['username']
    form = ChangePwdForm(request.form)
    if request.method == 'POST' and form.validate():
        user = pd.read_sql_query("SELECT * FROM users where username is '"
                                 + username + "' ;", conn)
        password = user.password[0]
        current = form.current.data
        if sha256_crypt.verify(current, password):
            user.password = sha256_crypt.hash(str(form.new.data))
            sql = "UPDATE users SET password = ? WHERE username is ? ;"
            cur = conn.cursor()
            cur.execute(sql, (user.password[0], str(username)))
            conn.commit()
            flash('Password changed', 'success')
            return redirect(url_for('main_bp.change_pwd'))
        else:
            flash('Current password incorrect', 'danger')
            return redirect(url_for('main_bp.change_pwd'))
    return render_template('change-pwd.html.j2', form=form)


# Access settings for a given user
@main_bp.route('/account/<string:username>', methods=['GET', 'POST'])
@is_logged_in
def account(username):
    role = session['usertype']
    # display role
    # user name
    # potential to add affiliations and email to give more bespoke access to
    # who can edit which volcanoes. Eg. Prject or Institute
    return render_template('account.html.j2', username=username, Role=role)

# Additional logged in as Admin only pages ------------------------------


@main_bp.route('/admin/information', methods=['GET', 'POST'])
@is_logged_in_as_admin
def admininfo():
    return render_template('admininfo.html.j2')


@main_bp.route('/admin/users', methods=['GET', 'POST'])
@is_logged_in_as_admin
def ViewOrAddUsers():
    df = pd.read_sql_query("SELECT * FROM Users ;", conn)
    df['password'] = '********'
    # add roles
    u2r = pd.read_sql_query("SELECT * FROM users_roles ;", conn)
    roles = pd.read_sql_query("SELECT * FROM roles ;", conn)
    u2r2 = pd.merge(u2r, roles, on='group_id')
    del u2r2['group_id']
    usersandroles = pd.merge(df, u2r2, on='id', how='outer')
    usersandroles.rename(columns={'name': 'Role'}, inplace=True)
    usersandroles = usersandroles.dropna(subset=['username'])
    colnames = [s.replace("_", " ").title() for s in usersandroles.columns.values[1:]]
    return render_template('view.html.j2', title='Users', colnames=colnames,
                           tableClass='Users', editLink="edit",
                           data=usersandroles)


# Add entry
@main_bp.route('/add/Users', methods=["GET", "POST"])
@is_logged_in_as_admin
def add():
    form = eval("Users_Form")(request.form)
    if request.method == 'POST' and form.validate():
        # Get form fields:
        # Check
        if len(str(form.password.data)) < 8:
            return flash('password must be more than 8 characters',
                         'danger')
        form.password.data = sha256_crypt.hash(str(form.password.data))
        formdata = []
        for f, field in enumerate(form):
            formdata.append(field.data)
        InsertUser(formdata[0], formdata[1], conn)
        flash('User Added', 'success')
        return redirect(url_for('main_bp.add', tableClass='Users'))
    return render_template('add.html.j2', title='Add Users', tableClass='Users',
                           form=form)


# Delete entry
@main_bp.route('/delete/<string:tableClass>/<string:id>', methods=['POST'])
@is_logged_in_as_admin
def delete(tableClass, id):
    # Retrieve DB entry:
    user = pd.read_sql_query("SELECT * FROM Users where id = " + id + " ;",
                             conn)
    username = user.username
    DeleteUser(username[0], conn)
    flash('User Deleted', 'success')
    return redirect(url_for('main_bp.ViewOrAddUsers'))


# Access settings for a given user
@main_bp.route('/access/<string:id>', methods=['GET', 'POST'])
@is_logged_in_as_admin
def access(id):
    form = AccessForm(request.form)
    form.Role.choices = table_list('roles', 'name', conn)[1:]
    # Retrieve user DB entry:
    user = pd.read_sql_query("SELECT * FROM Users where id = " + id + " ;",
                             conn)
    if user.empty:
        abort(404)
    # Retrieve all current role
    u2r = pd.read_sql_query("SELECT * FROM users_roles WHERE id = " + id +
                            ";", conn)
    gid = u2r.group_id[0]
    current_role = pd.read_sql_query("SELECT * FROM roles WHERE group_id = "
                                     + str(gid) + ";", conn)
    # If user submits edit entry form:
    if request.method == 'POST' and form.validate():
        new_role = form.Role.data
        AssignRole(user.username[0], new_role, conn)
        print('test')
        # Return with success
        flash('Edits successful', 'success')
        return redirect(url_for('main_bp.ViewOrAddUsers'))
    # Pre-populate form fields with existing data:
    form.username.render_kw = {'readonly': 'readonly'}
    form.username.data = user.username[0]
    form.Role.data = current_role.name[0]
    return render_template('access.html.j2', form=form, id=id)

# data exploration pages -----------------------------------------------------


@main_bp.route('/countries', methods=["GET"])
def countries():

    return render_template('bycountry.html.j2')

@main_bp.route('/infographic', methods=["GET"])
def infographic():
    return render_template('infographic.html.j2')

#   Main Info Page - Country Level

@main_bp.route('/countries/<string:ccode>/Info', methods=["GET"])
def CountryInfo(ccode):

    countries = {
        'MWI' : 'Malawi',
        'TZA' : 'Tanzania',
        'ZAF' : 'South Africa',
        'ZMB' : 'Zambia'
    }

    infopdf = {
        'MWI' : 'iFEED-Mw-findings.pdf',
        'TZA' : 'iFEED-Tz-findings.pdf',
        'ZAF' : 'iFEED-SA-findings.pdf',
        'ZMB' : 'iFEED-Zm-findings.pdf',
    }

    country=countries.get(ccode,"Unrecognised")

    pdfID=infopdf.get(ccode,"Unrecognised")

    if country=="Unrecognised":
        abort(404)

    return render_template('CountryInfo.html.j2', ccode=ccode, country=country, pdfID=pdfID)


@main_bp.route('/countries/<string:ccode>/<string:quad>', methods=["GET"])
def CountryQuad(ccode,quad):

    countries = {
        'MWI' : 'Malawi',
        'TZA' : 'Tanzania',
        'ZAF' : 'South Africa',
        'ZMB' : 'Zambia'
    }

    quadcode=quad[-2:]

    if ccode == "MWI":
        if quadcode == "00":
            scenname = "1: The Path to Heaven"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1UPymtLbgL8_Wlgt1N_BGvNt_WInJ3LWh", "1Va_8rRIlT3eIMd91tMpjYqTPGazujuns", "1m9iqQvB73JtnEkziAxXj-8vbZ5R2wNqa"]
            summaryid = "10veWWaUkV5Vt4Mp3MIGx7OVFLzoRlkJI"
        elif quadcode == "01":
            scenname = "2: Demanding but Coping"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1B-e7pJ3fdLujGXsPDYKdpTGkLjTDcawS", "1Soty-OvBY0kspR30RPe7RWSEqmC_svKP", "1m9iqQvB73JtnEkziAxXj-8vbZ5R2wNqa"]
            summaryid = "10veWWaUkV5Vt4Mp3MIGx7OVFLzoRlkJI"
        elif quadcode == "10":
            scenname = "3: Degrading Economy"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1CRfGsveIBjZBXvT-kUEG9_qTBeo3YGfP", "1Va_8rRIlT3eIMd91tMpjYqTPGazujuns", "1m9iqQvB73JtnEkziAxXj-8vbZ5R2wNqa"]
            summaryid = "10veWWaUkV5Vt4Mp3MIGx7OVFLzoRlkJI"
        elif quadcode == "11":
            scenname = "4: The Road to Hell"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "10VhRyVRBMvmSk8LLe1v4caU1EfNQFcY2", "1Soty-OvBY0kspR30RPe7RWSEqmC_svKP", "1m9iqQvB73JtnEkziAxXj-8vbZ5R2wNqa"]
            summaryid = "10veWWaUkV5Vt4Mp3MIGx7OVFLzoRlkJI"
    elif ccode == "TZA":
        if quadcode == "00":
            scenname = "1: Technofix"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll","19r57bcIgLx2x5PZutyupW2WRKj4TsHFD",  "1_8N9uwceOu8ZBFzhNT9WLRJYJ2HVXP0n", "1prGu8MMWH0oOk9WZMico1GRuss-yMGv1"]
            summaryid = "1S36QM2_2tJaIcsOsEWxyYCc_Hb4uV4fF"
        elif quadcode == "01":
            scenname = "2: Intensive Vulnerability"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1qpjcRo9bRDSpDShOmUNNE2leIK9WFMdZ", "1UDOhs1UFsr03c9CXi61cUDweBrXGDf0X", "1prGu8MMWH0oOk9WZMico1GRuss-yMGv1"]
            summaryid = "1McZlPklbDoUVFIY7p2eNGtXc_dopiqjN"
        elif quadcode == "10":
            scenname = "3: Human Capital"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1T7tBLkt9YavVLzL_fJwvefGeEAiMts66", "1_8N9uwceOu8ZBFzhNT9WLRJYJ2HVXP0n", "1prGu8MMWH0oOk9WZMico1GRuss-yMGv1"]
            summaryid = "15kY1CnYLuEMF-cKCHptszP_HO7vY3vA5"
        elif quadcode == "11":
            scenname = "4: Climate Chaos"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1lXPXods-LSWjeE_x3ZuHAORS_oJWk84Y", "1UDOhs1UFsr03c9CXi61cUDweBrXGDf0X", "1prGu8MMWH0oOk9WZMico1GRuss-yMGv1"]
            summaryid = "1h4K-L5UOuBMmVuOcgo3LY-wKDsIgpgEU"
    elif ccode == "ZAF":
        if quadcode == "00":
            scenname = "1: Structural Change"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1ZKtQ9GHxb85l1sp-EpXGf-L8iILVJkTb", "1C4k0mU-Fgi3u7RcmazlLXp_m2Vm6gEna", "1WltwOO5aPYDlEiqVsnumJ7k17wNzKQNG"]
            summaryid = "17dufHZcFFm5FN8UQldBZ9mSWwhBq_AHg"
        elif quadcode == "01":
            scenname = "2: All Change"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1hkAzSBk9gXnuKpv8j-CoNa2w9cEoZjeN", "1wAH-JkLj-GxrOyLqzIYokYgQAuo362KF", "1WltwOO5aPYDlEiqVsnumJ7k17wNzKQNG"]
            summaryid = "17dufHZcFFm5FN8UQldBZ9mSWwhBq_AHg"
        elif quadcode == "10":
            scenname = "3: Familiar Futures"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1JGyPhIDpMwiTsL_QcOxR2QWXMwns8Y0X", "1C4k0mU-Fgi3u7RcmazlLXp_m2Vm6gEna", "1WltwOO5aPYDlEiqVsnumJ7k17wNzKQNG"]
            summaryid = "1swtquoAb2Hhi4sm-RWHUrW0etr5t0mp1"
        elif quadcode == "11":
            scenname = "4: Hot and Bothered"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "17as0IGChbgKbU2-eX7AtL6E1fgeQz4BF", "1wAH-JkLj-GxrOyLqzIYokYgQAuo362KF", "1WltwOO5aPYDlEiqVsnumJ7k17wNzKQNG"]
            summaryid = "1EwtTJZQG8aRvBOJD3DK-D6fZMzTKiao2"
    elif ccode == "ZMB":
        if quadcode == "00":
            scenname = "1: Opportunity and Exposure"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1orp_eQGggLxpgkW3KC4xezfcP3aX6CUs", "1HOOCoEexGKQAgsynZ4lYng1W8A-R1F3o", "1IeAyKXIFTEz48z7bCAksfxHQSanqy7B4"]
            summaryid = "1yD6epshcUwSLdW40XHFnNb8nw-6lJlxW"
        elif quadcode == "01":
            scenname = "2: Risk and Reward"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1uZCTHFdtQwHcEu0skkalwr8210Cerh8i", "1XvuEOAX1NTnEc_vdgRlm9TeFYBxak9e5", "1IeAyKXIFTEz48z7bCAksfxHQSanqy7B4"]
            summaryid = "1b1THyhKkD3wrLJCRxrvTmv-vyx2b5OBR"
        elif quadcode == "10":
            scenname = "3: Solitude and Self-Sufficiency"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "1Q3BCdujmKJ3exNzjV-NOPtG4YmiPvfMn", "1HOOCoEexGKQAgsynZ4lYng1W8A-R1F3o", "1IeAyKXIFTEz48z7bCAksfxHQSanqy7B4"]
            summaryid = "1uJXMJPrxQgBfg3AfDz7KRAasZSPN22Wt"
        elif quadcode == "11":
            scenname = "4: Isolation and Imperative"
            pdflist = ["1Sd6andb_z1-mQOGlxtXE3Cbt656UOQll", "14xSv3S5KveaZzUgVrijNU1Dd1bk_Id0Y", "1XvuEOAX1NTnEc_vdgRlm9TeFYBxak9e5", "1IeAyKXIFTEz48z7bCAksfxHQSanqy7B4"]
            summaryid = "1WGt_nEC54b5F8tRLKs8xJwjW54_eSkID"

    country=countries.get(ccode,"Unrecognised")

    if country=="Unrecognised":
        abort(404)
    elif (quadcode != "00"
         and quadcode != "01"
         and quadcode != "10"
         and quadcode != "11"):
        abort(404)

    return render_template('scenarios.html.j2', ccode=ccode, country=country, quadcode=quadcode, scenname=scenname, pdflist=pdflist, summaryid=summaryid)

# static information pages ---------------------------------------------------

@main_bp.route('/copyright', methods=["GET"])
def copyright():
    return render_template('copyright.html.j2')

@main_bp.route('/privacy', methods=["GET"])
def privacy():
    return render_template('privacy.html.j2')

@main_bp.route('/contribute', methods=["GET"])
def contribute():
    return render_template('contributor_guidelines.html.j2')

@main_bp.route('/about', methods=["GET"])
def about():
    return render_template('about.html.j2')

@main_bp.route('/contact', methods=["GET"])
def contact():
    return render_template('contact.html.j2')

@main_bp.route('/glossary', methods=["GET"])
def glossary():
    return render_template('glossary.html.j2')

@main_bp.route('/modelling', methods=["GET"])
def infopage1():
    return render_template('infopage1.html.j2')

@main_bp.route('/infopage2', methods=["GET"])
def infopage2():
    return render_template('infopage2.html.j2')

@main_bp.route('/infopage3', methods=["GET"])
def infopage3():
    return render_template('infopage3.html.j2')

@main_bp.route('/calibrated', methods=["GET"])
def calibrated():
    return render_template('calibrated.html.j2')
