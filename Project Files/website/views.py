from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users, product 
from . import models, db
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

@views.route('/adminhome')
@login_required
def adminhome():
    return render_template("admin home.html")

@views.route('/adminhome/userManagement/createuser', methods=['GET', 'POST'])
@login_required
def UMcreateuser():
    if request.method == 'POST':
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password1 = request.form.get('password1')
        accesslevel = request.form.get('accesslevel')
        #input validation tests
        if len(name) < 2:
            flash('Name must be valid', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 6:
            flash('Passwords must be atleast 6 characters', category='error')
        else:
            new_user = Users(name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')     
    return render_template("admin user create.html")

#STOCKS AND STOCK CONTROL
@views.route('/stocks')
@login_required
def stocks():
    return render_template('stocks.html', title='Stocks')

@views.route('/stocks/add', methods=['GET', 'POST'])
def addstock():
    if request.method== 'POST':
        ProductName= request.form.get('ProductName')
        stocklevel= request.form.get('stocklevel')
        barcode= request.form.get('barcode')
        Pricing= request.form.get('Pricing')

        if len(barcode)>='14':
            flash("Invalid barcode, try again!", category='error')
        elif isinstance(stocklevel, (str,bool, float, complex)) == True:
            flash("Invalid entry for stock level, try again!",category='error')

        elif isinstance(Pricing, (float, int))==False:
            flash("Invalid entry for pricing, try again!",category='error')
        else: 
            new_product = product(ProductName=ProductName, stocklevel=stocklevel, barcode=barcode, Pricing=Pricing)
            db.session.add(new_product)
            db.session.commit()
            flash('Stock successfully added!', category='success')

@views.route('/stocks/edit')
def editstock():
    if request.method== 'POST':
        ProductID= request.form.get('ProductID')
        nProductName= request.form.get('ProductName')
        nstocklevel= request.form.get('stocklevel')
        nbarcode= request.form.get('barcode')
        nPricing= request.form.get('Pricing')

        #product.query.filter_by(ProductID=ProductID).first_or_404(description='ProductID is not valid'.format(ProductID))

        productbeingeditted = product.query.filter_by(ProductID=ProductID).first_or_404(description='ProductID is not valid'.format(ProductID))

        try:
            if ProductName != "":
                productbeingeditted.ProductName=nProductName
            if stocklevel !="":
                productbeingeditted.stocklevel=nstocklevel
            if barcode != "":
                productbeingeditted.barcode=nbarcode
            if Pricing != "":
                productbeingeditted.Pricing=nPricing
        except:
            flash("There was an error",category='error')
        finally:
            flash("Operation has been completed", category='success')
    
        
    



@views.route('/stocks/delete', methods=['GET', 'POST'])
def deletestock():
    if request.method== 'POST':
        ProductID= request.form.get('ProductID')
        stock_to_delete = product.query.get_or_404(ProductID)
        
        try: 
            db.session.delete(stock_to_delete)
            db.session.commit()
            flash("Stock ", ProductID," deleted successfully!", category='success')
            return redirect(url_for('views.stocks'))#
        except:
            flash("Error deleting stock, try again!", category='error')
            

        
#START CODING HERE ^^^ ABOVE THIS MESSAGE





@views.route('/api/data')
def data():
    query = product.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            product.ProductName.like(f'%{search}%'),
            product.barcode.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['ProductName', 'barcode', 'ProductID']:
            col_name = 'ProductName'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(product, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [user.to_dict() for user in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': product.query.count(),
        'draw': request.args.get('draw', type=int),
    }
