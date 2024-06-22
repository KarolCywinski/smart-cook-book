# Smart Cook Book :plate_with_cutlery:
![smart-cook-book](https://github.com/KarolCywinski/smart-cook-book/assets/167247117/627418ed-cffd-4206-8116-d4cfc389d6e1)
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
### Using Python virtual environment :snake: :desert_island:
1. Install Python and verify your internet connectivity, as the application uses Content Delivery Network (CDN) on the frontend :earth_asia:
2. Navigate to the *backend* directory where all the python files are kept: `cd ./backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment from the console or if you are using VS Code, select the proper Python interpreter from the created *venv* directory :rocket:
5. Install all the required python packages before the first run: `pip install -r requirements.txt`
6. Run the backend server: `uvicorn main:app --reload`
7. Open: http://127.0.0.1:8000/smart-cook-book
### Using Docker :whale2: :ocean:
1. Install Docker and verify your internet connectivity, as the application uses Content Delivery Network (CDN) on the frontend :earth_americas:
2. Build the image and run the container defined in the *docker-compose.yml* file: `docker-compose up`
3. Open: http://127.0.0.1:8000/smart-cook-book
