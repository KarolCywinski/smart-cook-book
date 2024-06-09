# Smart Cook Book :plate_with_cutlery:
## What is it :thinking:
This is a website application designed for easy recipe management.

After its first run, the application sets up some basic data, like available units of measurement :triangular_ruler::balance_scale: and recipe categories.

With just a few clicks, users can effortlessly create and modify recipes. The application also generates interactive shopping lists :heavy_check_mark::heavy_multiplication_x::shopping_cart: for each recipe (which are populated based on chosen ingredients :onion::cheese::hot_pepper:).
## Tech stack :hammer_and_wrench:
- Backend :gear:
  - Python :snake:
    - FastAPI 
    - SQLAlchemy
- Frontend :crayon:
  - Vue.js (CDN)
  - Tailwind CSS (CDN)
  - Axios (CDN)
## How to run it :man_technologist:
1. Verify your internet connectivity, as the application uses Content Delivery Network (CDN) on the frontend :globe_with_meridians:
2. Navigate to the *backend* directory where all the python files are kept and where your *venv* folder should be, assuming you're working with virtual environments: `cd ./backend`
3. Install all the required python packages before the first run: `pip install -r requirements.txt`
4. Run the backend server: `uvicorn main:app --reload`
5. Open: http://127.0.0.1:8000/smart-cook-book
