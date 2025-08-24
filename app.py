import os
import pandas as pd
import html
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ============================================================
# --- Flask Application Setup ---
# ============================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# ============================================================
# --- Database Model ---
# ============================================================
class Phone(db.Model):
    """
    Represents a refurbished phone in the inventory.
    Stores details such as stock, base price, B2B reservations,
    platform listing status, and calculated platform prices.
    """
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    reserved_for_b2b = db.Column(db.Integer, default=0)
    condition = db.Column(db.String(50), nullable=False)
    specifications = db.Column(db.String(200), nullable=True)

    # Platform listing flags
    is_listed_on_x = db.Column(db.Boolean, default=False)
    is_listed_on_y = db.Column(db.Boolean, default=False)
    is_listed_on_z = db.Column(db.Boolean, default=False)

    # Platform specific prices
    price_on_x = db.Column(db.Float, default=0.0)
    price_on_y = db.Column(db.Float, default=0.0)
    price_on_z = db.Column(db.Float, default=0.0)

    tags = db.Column(db.String(100), nullable=True)

    @property
    def available_stock(self):
        """Returns the stock available for listing after B2B reservations."""
        return max(0, self.stock_quantity - self.reserved_for_b2b)

# ============================================================
# --- Helper Functions ---
# ============================================================
def calculate_platform_prices(base_price):
    """
    Calculate platform-specific selling prices based on their fee structure.
    X: 10% fee
    Y: 8% fee + $2 fixed
    Z: 12% fee
    """
    return {
        'x': round(base_price / (1 - 0.10), 2),
        'y': round((base_price + 2) / (1 - 0.08), 2),
        'z': round(base_price / (1 - 0.12), 2)
    }

def map_condition_to_platform(internal_condition, platform):
    """Map the internal phone condition to platform-specific categories."""
    mapping = {
        'X': {'New': 'New', 'Good': 'Good', 'Scrap': 'Scrap'},
        'Y': {'New': '3 stars (Excellent)', 'Good': '2 stars (Good)', 'Usable': '1 star (Usable)'},
        'Z': {'New': 'New', 'Excellent': 'As New', 'Good': 'Good'}
    }
    return mapping.get(platform, {}).get(internal_condition)

def check_profitability(base_price, platform):
    """Ensure that the phone yields at least $5 profit after fees."""
    MIN_PROFIT = 5.0
    final_price = calculate_platform_prices(base_price)[platform.lower()]
    profit = final_price - base_price
    return profit >= MIN_PROFIT

def allowed_file(filename):
    """Check if uploaded file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================================
# --- Mock Authentication ---
# ============================================================
MOCK_USERS = {"admin": "password123"}

@app.before_request
def require_login():
    """Redirect to login page if user not authenticated."""
    allowed_routes = ['login']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

# ============================================================
# --- Routes ---
# ============================================================

# --- Authentication ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with mock credentials."""
    if request.method == 'POST':
        if MOCK_USERS.get(request.form['username']) == request.form['password']:
            session['username'] = request.form['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user and clear session."""
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Inventory Views ---
@app.route('/')
def index():
    """Main inventory page with search and filter options."""
    query = Phone.query

    # Search filter
    search_term = request.args.get('search')
    if search_term:
        query = query.filter(
            Phone.model_name.ilike(f'%{search_term}%') |
            Phone.brand.ilike(f'%{search_term}%')
        )

    # Condition filter
    condition_filter = request.args.get('condition')
    if condition_filter:
        query = query.filter(Phone.condition == condition_filter)

    # Platform filter
    platform_filter = request.args.get('platform')
    if platform_filter == 'X':
        query = query.filter(Phone.is_listed_on_x == True)
    elif platform_filter == 'Y':
        query = query.filter(Phone.is_listed_on_y == True)
    elif platform_filter == 'Z':
        query = query.filter(Phone.is_listed_on_z == True)

    phones = query.all()
    return render_template('index.html', phones=phones)

# --- Add Phone ---
@app.route('/add', methods=['GET', 'POST'])
def add_phone():
    """Add a new phone into the inventory."""
    if request.method == 'POST':
        model_name = html.escape(request.form['model_name'])
        brand = html.escape(request.form['brand'])
        specifications = html.escape(request.form['specifications'])
        condition = request.form['condition']

        try:
            base_price = float(request.form['base_price'])
            stock_quantity = int(request.form['stock_quantity'])
            reserved_for_b2b = int(request.form.get('reserved_for_b2b', 0))
            if base_price < 0 or stock_quantity < 0 or reserved_for_b2b < 0:
                flash('Price, stock, or B2B reservation cannot be negative.', 'danger')
                return redirect(url_for('add_phone'))
            if reserved_for_b2b > stock_quantity:
                flash('B2B reservation cannot exceed stock quantity.', 'danger')
                return redirect(url_for('add_phone'))
        except ValueError:
            flash('Invalid number for price, stock, or B2B.', 'danger')
            return redirect(url_for('add_phone'))

        prices = calculate_platform_prices(base_price)
        new_phone = Phone(
            model_name=model_name,
            brand=brand,
            base_price=base_price,
            stock_quantity=stock_quantity,
            reserved_for_b2b=reserved_for_b2b,
            condition=condition,
            specifications=specifications,
            price_on_x=prices['x'],
            price_on_y=prices['y'],
            price_on_z=prices['z'],
            tags="Out of Stock" if stock_quantity == 0 else ""
        )
        db.session.add(new_phone)
        db.session.commit()
        flash(f'Phone "{model_name}" added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_phone.html')

# --- Edit Phone ---
@app.route('/edit/<int:phone_id>', methods=['GET', 'POST'])
def edit_phone(phone_id):
    """Edit an existing phone in the inventory."""
    phone = Phone.query.get_or_404(phone_id)
    if request.method == 'POST':
        phone.model_name = html.escape(request.form['model_name'])
        phone.brand = html.escape(request.form['brand'])
        phone.specifications = html.escape(request.form['specifications'])
        phone.condition = request.form['condition']
        try:
            phone.base_price = float(request.form['base_price'])
            phone.stock_quantity = int(request.form['stock_quantity'])
            phone.reserved_for_b2b = int(request.form.get('reserved_for_b2b', 0))
            phone.price_on_x = float(request.form['price_on_x'])
            phone.price_on_y = float(request.form['price_on_y'])
            phone.price_on_z = float(request.form['price_on_z'])
            if phone.reserved_for_b2b > phone.stock_quantity:
                flash('B2B reservation cannot exceed stock quantity.', 'danger')
                return render_template('edit_phone.html', phone=phone)
        except ValueError:
            flash('Invalid number input.', 'danger')
            return render_template('edit_phone.html', phone=phone)

        phone.tags = "Out of Stock" if phone.available_stock == 0 else ""
        db.session.commit()
        flash(f'Phone "{phone.model_name}" updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_phone.html', phone=phone)

# --- Delete Phone ---
@app.route('/delete/<int:phone_id>', methods=['POST'])
def delete_phone(phone_id):
    """Delete a phone from the inventory."""
    phone = Phone.query.get_or_404(phone_id)
    db.session.delete(phone)
    db.session.commit()
    flash(f'Phone "{phone.model_name}" deleted.', 'info')
    return redirect(url_for('index'))

# --- List on Platform ---
@app.route('/list_on_platform/<int:phone_id>/<platform>', methods=['POST'])
def list_on_platform(phone_id, platform):
    """Simulate listing a phone on a given platform."""
    phone = Phone.query.get_or_404(phone_id)
    platform_name = platform.upper()

    if phone.available_stock <= 0:
        flash(f'Cannot list on {platform_name}: Out of stock or reserved for B2B.', 'danger')
        return redirect(url_for('index'))

    platform_condition = map_condition_to_platform(phone.condition, platform_name)
    if not platform_condition:
        flash(f'Cannot list on {platform_name}: Unsupported condition \"{phone.condition}\".', 'warning')
        return redirect(url_for('index'))

    if not check_profitability(phone.base_price, platform_name):
        flash(f'Cannot list on {platform_name}: Not profitable.', 'warning')
        return redirect(url_for('index'))

    if platform_name == 'X':
        phone.is_listed_on_x = True
    elif platform_name == 'Y':
        phone.is_listed_on_y = True
    elif platform_name == 'Z':
        phone.is_listed_on_z = True

    db.session.commit()
    flash(f'Successfully listed \"{phone.model_name}\" on {platform_name} as \"{platform_condition}\".', 'success')
    return redirect(url_for('index'))

# --- Bulk Upload ---
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Handle CSV/Excel bulk upload of phones."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded.', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            flash('Invalid file type.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath) if filename.endswith('.csv') else pd.read_excel(filepath)
            for _, row in df.iterrows():
                try:
                    base_price = float(row['base_price'])
                    stock_quantity = int(row['stock_quantity'])
                    reserved_for_b2b = int(row.get('reserved_for_b2b', 0))
                    if reserved_for_b2b > stock_quantity:
                        reserved_for_b2b = 0  # fallback if bad data
                    prices = calculate_platform_prices(base_price)
                    new_phone = Phone(
                        model_name=row['model_name'],
                        brand=row['brand'],
                        base_price=base_price,
                        stock_quantity=stock_quantity,
                        reserved_for_b2b=reserved_for_b2b,
                        condition=row['condition'],
                        specifications=row['specifications'] if 'specifications' in row else "",
                        price_on_x=prices['x'],
                        price_on_y=prices['y'],
                        price_on_z=prices['z'],
                        tags="Out of Stock" if (stock_quantity - reserved_for_b2b) <= 0 else ""
                    )
                    db.session.add(new_phone)
                except Exception as inner_e:
                    flash(f'Skipped a row due to error: {inner_e}', 'warning')
            db.session.commit()
            flash('File processed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Upload failed: {e}', 'danger')
        return redirect(url_for('index'))
    return render_template('upload.html')

# ============================================================
# --- Main Entrypoint ---
# ============================================================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
