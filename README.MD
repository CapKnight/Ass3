# Wine Sales Platform

A Django-based web application for selling wines online, featuring user authentication, product browsing, order management, and admin analytics.

## Features

- **User Authentication**: Register, login, and logout functionality for users. Admin users can access the Django admin panel.
- **Product Listing**: Browse wines with filtering (by country, region, winery), searching, sorting (by price), and pagination.
- **Product Comparison**: Compare up to 4 products side by side.
- **Order Management**:
  - Create orders for products.
  - Pay for individual orders or multiple selected orders.
  - Cancel pending or paid orders (inventory updates accordingly).
  - Simulated payment process with a modal popup for confirmation.
- **Admin Dashboard**: View order statistics (total orders, revenue, status breakdown) and a line chart of orders over the last 7 days using Chart.js. Administrator can see all the orders and edit or cancel them.
- **Responsive Design**: The application is mobile-friendly with a responsive navigation bar and layout.

### Account
You can create your own user account or admin account. Or you can use our account for testing.
for regular user:
- username: test
- password: 123

for admin:
- username: admin
- password: admin123

### Steps
You can chekck my cloud urls: https://capknight.pythonanywhere.com/products/

If you are using my codio, simply start the server by using terminal: python3 manage.py runserver 0.0.0.0:8000. Then open your browser and navigate to `https://futurefield-initialstuart-8000.codio-box.uk/` to access the application.


1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CapKnight/Ass3.git
   cd Ass3
   ```

2.**install Django**
   ```bash
   pip install django==5.2
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a Superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```
   Open your browser and navigate to `https://futurefield-initialstuart-8000.codio-box.uk/` to access the application.

## Requirements

The following dependencies are listed in `requirements.txt`:

- Django==5.2
- Chart.js (loaded via CDN for admin dashboard charts)

To generate the `requirements.txt` file, you can use:
```bash
pip freeze > requirements.txt
```

## Testing

The project includes unit tests to ensure functionality. To run the tests:

```bash
python manage.py test
```

This will execute all test cases (16 tests in total) and provide a summary of the results.

### Data

Wine's data from open source: https://www.kaggle.com/datasets/budnyak/wine-rating-and-price