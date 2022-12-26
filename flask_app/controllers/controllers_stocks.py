from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.models_user import User
from flask_app.models.models_stock import Stock
from flask_app.config.mysqlconnection import connectToMySQL

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    all = Stock.all_stocks()
    return render_template('dashboard.html', user = user, all = all)


#New Stock route
@app.route('/add_stock')
def add_stock():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('new_stock.html', user = user)


# Create Stock entry and adds to DB
@app.route('/create_stock', methods=['POST'])
def create_stock():
    data = {
        'symbol' : request.form['symbol'],
        'company_name' : request.form['company_name'],
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    Stock.create_stock(data)
    return redirect('/dashboard')


# Display One Stock
@app.route('/show_stock/<int:stock_id>')
def show_stock(stock_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : stock_id
    }
    user_data = {
        'id' : session['user_id']
    }
    stock = Stock.get_one(data)
    user = User.get_one(user_data)
    return render_template('show_stock.html', stock = stock, user = user)


# Update One Stock
@app.route('/update_stock/<int:stock_id>', methods=['POST'])
def update_stock(stock_id):
    Stock.update_stock(request.form, stock_id)
    return redirect('/dashboard')


# Edit One Stock Tab
@app.route('/edit_stock/<int:stock_id>')
def edit_stock(stock_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : stock_id
    }
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    stock = Stock.get_one(data)
    return render_template('edit_stock.html', stock = stock, user = user)


# Delete One Stock
@app.route('/delete/<int:stock_id>')
def delete_stock(stock_id):
    data = {
        'id' : stock_id
    }
    Stock.delete_stock(data)
    return redirect('/dashboard')
