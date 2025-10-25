from app import app, db
from flask import render_template, flash, redirect, url_for, request, current_app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from datetime import datetime, timezone
from DataAcq.Standings import DriverStandings
from DataAcq.Races import Races
from DataAcq.LastSession import LastSession
from DataAcq.Drivers import drivers
from DataAcq.Circuits import Circuits
from util import time_conversion as tc
from util import circuit_map, race_mapping, colors, constructor_mapping, track_dominance
from DataAcq.Telemetry import telem
import plotly.express as px
import json
import pandas as pd
import plotly.graph_objects as go
import os
import plotly.io as pio

@login_required
@app.route('/index')
@app.route('/')
def index():
    session = LastSession.get_last_session()
    session_name = session[0]['session_name']
    year = session[0]['year']
    circuit_name = session[0]['circuit_short_name']
    session_result = LastSession.get_last_session_results()
    session_key = session_result[0]['session_key']
    session_drivers = drivers.get_drivers_by_session(session_key)
    driver_dict = {driver['driver_number']: f"{driver['first_name']} {driver['last_name']}" for driver in session_drivers}
    for result in session_result:
        if 'race' in session_name.lower():
            if result['duration'] is not None:
                result['time'] = tc.convert_time(result['duration']).lstrip("0")
            else:
                result['time'] = 'lapped'
            if '+' not in str(result['gap_to_leader']) and result['gap_to_leader'] != 0:
                result['gap_to_leader'] = '+' + str(tc.convert_time(result['gap_to_leader']).lstrip("0"))
            result['points'] = int(result['points'])
        elif 'race' not in session_name.lower() and 'qualifying' not in session_name.lower():
            result['time'] = tc.convert_time(result['duration']).lstrip("0")
        else:
            if result['duration'][2] is not None:
                result['time'] = tc.convert_time(result['duration'][2]).lstrip("0")
                result['gap_to_leader'] = result['gap_to_leader'][2]
            elif result['duration'][1] is not None:
                result['time'] = tc.convert_time(result['duration'][1]).lstrip("0")
                result['gap_to_leader'] = result['gap_to_leader'][1]
            elif result['duration'][0] is not None:
                result['time'] = tc.convert_time(result['duration'][0]).lstrip("0")
                result['gap_to_leader'] = result['gap_to_leader'][0]
            else:
                result['position'] = '-'
                for i in ['dnf', 'dns', 'dsq']:
                    if result[i] == True:
                        result['time'] = i.upper()
                        result['gap_to_leader'] = '-'
                        break
                    else:
                        result['time'] = '-'
                        result['gap_to_leader'] = '-'
        if result['gap_to_leader'] == 0:
                result['gap_to_leader'] = '-'
        result['driver_name'] = driver_dict[result['driver_number']]

    if 'race' not in session_name.lower():
        circuit = Circuits.getNextCircuit()
    else:
        circuit = Circuits.getLastCircuit()
    circuit = circuit['MRData']['CircuitTable']['Circuits'][0]
    loc = circuit['Location']
    location = [float(loc['lat']), float(loc['long']), circuit_name]
    #circuit_map.generate_circuit_map(location[0], location[1], location[2])
    
    return render_template('index.html', session_result=session_result, session_name=session_name, year=year, circuit_name=circuit_name, circuit=circuit)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', register_form=RegistrationForm(), login_form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('login.html', title='Register', register_form=form, login_form=LoginForm())

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username)
        )
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are now following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username)
        )
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself.')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are no longer following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/driver_standings', methods=['GET', 'POST'])
@login_required
def driver_standings():
    year = datetime.now().year
    standings = DriverStandings.getDriverStandingsCurrent(year)
    standings = standings['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    return render_template('driverstandings.html', title=f"Driver Standings {year}", standings=standings, year=year)

@app.route('/race', methods=['GET','POST'])
@login_required
def race_result():
    value = request.args.get('race')
    value = value.replace('%20', ' ')
    circuit = race_mapping.map_race_name(value, 'circuitId')
    year = datetime.now().year
    results, circuit = Races.getRaceResultByYearCircuit(year, circuit)
    return render_template('race_result.html', title=f"{year} {value} Race Result", results=results, year=year, value=value, circuit=circuit)

@app.route('/drivers/<driverId>', methods=['GET', 'POST'])
@login_required
def driver_info(driverId: str):
    results = drivers.get_driver_current_season_results(driverId)['MRData']['RaceTable']['Races']
    standing = DriverStandings.getCurrentYearSingleDriverStandings(driverId)['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][0]
    info = {}

    info['wins'] = standing['wins']
    info['points'] = standing['points']
    info['position'] = standing['position']
    info['races'] = len(results)
    info['podiums'] = sum(1 for race in results if int(race['Results'][0]['position']) <= 3)
    info['points_finishes'] = sum(1 for race in results if int(race['Results'][0]['position']) <= 10)
    info['poles'] = sum(1 for race in results if int(race['Results'][0]['grid']) == 1)
    info['year'] = results[0]['season']
    info['number'] = results[0]['Results'][0]['Driver']['permanentNumber']
    info['givenName'] = results[0]['Results'][0]['Driver']['givenName']
    info['familyName'] = results[0]['Results'][0]['Driver']['familyName']
    info['code'] = results[0]['Results'][0]['Driver']['code']
    info['nationality'] = results[0]['Results'][0]['Driver']['nationality']
    info['dateOfBirth'] = datetime.strptime(results[0]['Results'][0]['Driver']['dateOfBirth'], "%Y-%m-%d").strftime("%B %-d, %Y")
    info['constructor'] = results[len(results)-1]['Results'][0]['Constructor']['constructorId']
    print(info)
    return render_template('driver.html', info=info, driverId=driverId)

@app.route('/telemetry', methods=['GET', 'POST'])
@login_required
def telemetry():
    return render_template('telemetry_select.html')

@app.route('/load_drivers', methods=['GET', 'POST'])
@login_required
def load_drivers():
    print('loading drivers')
    race_name = request.args.get('raceId').replace('%20', ' ')
    raceId = race_mapping.RACE_MAP[race_name]['circuitId']
    print('raceId:', raceId)
    driver_list = drivers.get_drivers_by_season_circuit(2025, raceId)
    driver_ids = [driver for driver in driver_list['MRData']['DriverTable']['Drivers']]
    return driver_ids


@app.route('/get_telemetry', methods=['GET', 'POST'])
@login_required
def get_telemetry():
    
    raceId = race_mapping.RACE_MAP[request.args.get('raceId').replace('%20', ' ')]['circuit_short_name']
    circuit_short_name = race_mapping.RACE_MAP[request.args.get('raceId').replace('%20', ' ')]['circuit_short_name']
    print(raceId, circuit_short_name)
    country = race_mapping.RACE_MAP[request.args.get('raceId').replace('%20', ' ')]['country_name']
    driver1 = request.args.get('driver1')
    driver2 = request.args.get('driver2')
    df1, df2 = telem.get_telemetry(raceId, driver1, driver2)


    print(circuit_short_name)
    raceId = next((v['circuitId'] for v in race_mapping.RACE_MAP.values() if v['circuit_short_name'] == raceId), None)
    race = Races.getSessionByYearCircuit(raceId)
    d1 = next(
       driver
       for driver in race['MRData']['RaceTable']['Races'][0]['Results']
       if driver['Driver']['code'] == driver1
     )
    d2 = next(
       driver
       for driver in race['MRData']['RaceTable']['Races'][0]['Results']
       if driver['Driver']['code'] == driver2
     )

    driver1_id = d1['Driver']['driverId']
    driver2_id = d2['Driver']['driverId']
    
    driver1_name = d1['Driver']['familyName']
    driver2_name = d2['Driver']['familyName']

    con1 = d1['Constructor']['constructorId']
    con2 = d2['Constructor']['constructorId']
    driver1_color = '#' + next((x['color'] for x in constructor_mapping.CONSTRUCTOR_MAP.values() if x['id'] == con1), 'FFFFFF')
    driver2_color = '#' + next((x['color'] for x in constructor_mapping.CONSTRUCTOR_MAP.values() if x['id'] == con2), 'FFFFFF')

    if driver1_color == driver2_color:
        driver2_color = colors.shift_hue(driver2_color, 0.15)


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df1['Time'],
        y=df1['Speed'],
        mode='lines',
        name=driver1_name,
        line=dict(color=driver1_color),
        hovertemplate='%{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df2['Time'],
        y=df2['Speed'],
        mode='lines',
        name=driver2_name,
        line=dict(color=driver2_color),
        hovertemplate='%{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        # title=f"{request.args.get('raceId').replace('%20', ' ')} Qualifying: {driver1_name} vs {driver2_name}",
        xaxis_title='Time',
        yaxis_title='Speed (km/h)',
        template='plotly_dark',
        hovermode='x'
    )

    
    graph = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    path = os.path.join(current_app.root_path, 'static', 'media', 'telemetry', 'speed_comparison.html')
    fig.write_html(path)

    track_dominance.track_dominance(driver1, driver2, raceId, driver1_color, driver2_color)


    racename = request.args.get('raceId').replace('%20', ' ')
    return render_template('telemetry.html', 
                           graph=graph, 
                           raceId=raceId, 
                           racename=racename, 
                           driver1_name=driver1_name, 
                           driver2_name=driver2_name,
                           driver1_id=driver1_id,
                           driver2_id=driver2_id,
                           con1=con1,
                           con2=con2)

