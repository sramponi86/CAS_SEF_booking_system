from flask import Flask, render_template, request, flash, session, redirect, url_for
from rental import controller
from rental.company import Company
from rental.exceptions import RentalException
import traceback
import pickle
from os.path import exists
from datetime import date
from pathlib import Path
import logging

app = Flask(__name__)

app.secret_key = "super secret key"
company: Company = None
request_number = 1


log = logging.getLogger('werkzeug')
log.setLevel(logging.WARN)

@app.context_processor
def inject_data():
    return dict(company = company, today = controller.today)

def persist_company():
  Path('./persistence').mkdir(parents=True, exist_ok=True)
  file = open('./persistence/state.data','wb')
  pickle.dump([company, controller.current_id] , file)
  file.close()

def load_persisted_company():
  global company
  if not exists('./persistence/state.data'):
    print('No persisted company data.')
    return False
  file = open('./persistence/state.data','rb')
  try:
    company, id = pickle.load(file)
    controller.setId(id)
    print('Persistent company data loaded successfully.')
    return True
  except:
    pass
  finally:
    file.close()
  print('Schema missmatch. Persistent company data will not be loaded.')
  return False
  
# Hacky - should be wrapped in proper Startup, can only be done after we put everything in modules.
# https://flask.palletsprojects.com/en/3.0.x/tutorial/factory/
load_persisted_company()

# HACK: Such a message is reported by flask upon startup and handy since clickable in VS Code, but 
# we currently suppress the output by setting log granularity to WARN. Moreover, host and port are
# hardcoded here. I tried to find a better way, but failed (in reasonable time).
print(" * Running on http://127.0.0.1:5000")

def handle_request():
  global request_number
  
  handle = False
  rq = request.args.get('rq')
  if not rq:
    return False
  try:
    handle = int(request.args.get('rq')) == session['rq']
    if not handle:
      print('Request got replayed, Ignoring.') 
  except:
    print('Exception during replay-checking. Ignoring.') 
  return handle

def update_request_number():
  global request_number
  request_number += 1
  session['rq'] = request_number

@app.route('/')
def index():
  if company == None:
    return redirect(url_for('admin'))
  return render_template('index.html')

@app.route('/customer')
def customer():
  if company == None:
    return redirect(url_for('admin'))
  if handle_request():
    try:
      customer_id = session.get('customer_id')
      id = request.args.get('id')
      if (customer_id):
        action = request.args.get('action')
        if action == "add_car_booking":
          period_start = date.fromisoformat(request.args.get('period_start'))
          period_end = date.fromisoformat(request.args.get('period_end'))
          company.bookings.add(int(customer_id),period_start, period_end, int(id))
        if action == "delete_booking":
          company.bookings.delete(int(id))
        if action == "add_rental":
          company.rentals.add(int(id))
        if action == "delete_rental":
          rental = company.rentals.find_by_booking_id(int(id))
          company.rentals.delete(rental.id)
        persist_company()
    except RentalException as re:
      flash(re, 'warning')
    except Exception:
      flash(traceback.format_exc(), 'danger')
  update_request_number()
  if session.get('customer_id'):
    return render_template('customer.html')
  else:
    return redirect(url_for('login'))

@app.route('/book')
def book():
  return render_template('book.html')

@app.route('/rent')
def rent():
  return render_template('rent.html')

@app.route('/logout')
def logout():
  session.pop('customer_id', None)
  return redirect(url_for('login'))

@app.route('/login')
def login():
  if handle_request():
    set_customer = request.args.get('set_customer')
    if set_customer:
      session['customer_id'] = int(set_customer)
      session['customer_name'] = company.customers.find_by_id(int(set_customer)).getLabel()
  update_request_number()
  if session.get('customer_id'):
    return redirect(url_for('customer'))
  return render_template('login.html')

@app.route('/set_date')
def setDate():
  next = "/"
  if handle_request():
    controller.setToday(date.fromisoformat(request.args.get('today')))
    next = request.args.get('next')
  update_request_number()
  return redirect(next)
  
  
@app.route('/reset')
def reset():
  global company
  if handle_request():    
    try:
      company_name = request.args.get('company_name')
      if company_name:
        session.pop('customer_id', None)
        company = Company(company_name)
        persist_company()
    except Exception:
      flash(traceback.format_exc(), 'danger')
  update_request_number()
  return redirect(url_for('admin'))

@app.route('/admin')
def admin():
  if company == None:
    session.pop('customer_id', None)
  if handle_request():
    try:
      action = request.args.get('action')
      id = request.args.get('id')
      name = request.args.get('name')
      color = request.args.get('color')
      if action == "add_customer":
        if not company.customers.contains(name):
          company.customers.add(name)
        else:
          flash(f'A customer with name "{name}" exists already', 'warning')
      if action == "delete_customer":
        company.customers.delete(int(id))
      if action == "add_car":
        company.cars.add(name, color)
      if action == "delete_car":
        company.cars.delete(int(id))
      persist_company()
      
    except RentalException as re:
      flash(re, 'warning')
    except Exception:
      flash(traceback.format_exc(), 'danger')
  update_request_number()
  return render_template('admin.html')
