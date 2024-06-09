from fastapi import FastAPI, Path, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

import models, schemas, database, crud


# Define main application life cycle

app = FastAPI()
app.mount("/smart-cook-book", StaticFiles(directory="../frontend", html = True), name="frontend")

# Make sure each API request gets new session and destroys it later
def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()

# Create tables (if needed) after application startup
@app.on_event("startup")
def initialize_db():
    models.Base.metadata.create_all(database.engine)

# Create initial data (if needed)
@database.event.listens_for(models.Base.metadata, 'after_create')
def receive_after_create(target, connection, tables, **kw):
    # Initialize only after database tables are created
    if tables:
        with database.Session() as db:
            crud.create_exemplary_data(db)
    
# Define requests

# Recipes
# GET
@app.get("/recipes/{recipe_category_name}", response_model=list[schemas.Recipe])
def get_recipes(recipe_category_name: str = Path(description='Recipe category name'), db: Session = Depends(get_db)):
    try:
        return crud.get_recipes(db, recipe_category_name)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Internal Server Error (unable to read recipes)")
    
# POST
@app.post("/recipes", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.Recipe, db: Session = Depends(get_db)):
    try:
        db_recipe = crud.get_recipe(db, recipe.name)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error (unable to verify recipe name uniqueness)")
    else:
        if db_recipe is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Recipe with that name already exists")
        try:
            return crud.create_recipe(db, recipe)
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Internal Server Error (unable to create recipe)")
        
# PATCH
@app.patch("/recipes/{recipe_name}", response_model=schemas.Recipe)
def update_recipe(recipe: schemas.RecipeUpdate, 
                  recipe_name: str = Path(description="Name of recipe to update"), db: Session = Depends(get_db)):
    try:
        # find recipe to update
        db_recipe = crud.get_recipe(db, recipe_name)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error (unable to find recipe to update)")
    else:
        if db_recipe is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Recipe with that name not found")
        try:
            # check if recipe with that name already exists
            db_recipe_with_new_name = None
            if "name" in recipe.model_fields_set:
                db_recipe_with_new_name = crud.get_recipe(db, recipe.name)
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Internal Server Error (unable to check if recipe name is unique)")
        else:
            if db_recipe_with_new_name is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Recipe with that name already exists")
            try:
                return crud.update_recipe(db, recipe, db_recipe)
            except:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Internal Server Error (unable to update recipe)")
   
        
# DELETE
@app.delete("/recipes/{recipe_name}")
def delete_recipe(recipe_name: str = Path(description="Name of recipe to delete"), db: Session = Depends(get_db)):
    try:
        db_recipe = crud.get_recipe(db, recipe_name)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal Server Error (unable to find recipe to delete)")
    else:
        if db_recipe is not None:
            try:
                crud.delete_recipe(db, db_recipe)
            except:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Internal Server Error (unable to delete recipe)")
        else:   
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Recipe with that name not found")
        
# Recipe categories
# GET
@app.get("/recipe-categories", response_model=list[schemas.RecipeCategory])
def get_recipe_categories(db: Session = Depends(get_db)):
    try:
        return crud.get_recipe_categories(db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Internal Server Error (unable to read recipe categories)")
    
# Units
# GET
@app.get("/units", response_model=list[schemas.Unit])
def get_units(db: Session = Depends(get_db)):
    try:
        return crud.get_units(db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Internal Server Error (unable to read units)")
    
# Food categories
# GET
@app.get("/food-categories", response_model=list[schemas.FoodCategory])
def get_food_categories(db: Session = Depends(get_db)):
    try:
        return crud.get_food_categories(db)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Internal Server Error (unable to read food categories)")
    

# Recipe ingredients with their food categories
# GET
@app.get("/recipe-ingredients/{recipe_name}")
def get_recipe_ingredients(recipe_name: str = Path(description='Recipe name'), db: Session = Depends(get_db)):
    try:
        # build a list of db tuples
        results = crud.get_recipe_ingredients(db, recipe_name)

        # create a dictionary that stores a list of ingredients for each food category
        food_categories_dict = {}
        for result in results:
            db_recipe_ingredient, food_category_name = result
            # if food category key not present in dictionary - create a new list to store ingredients
            if food_category_name not in food_categories_dict:
                food_categories_dict[food_category_name] = []
            # add ingredient to list  
            food_categories_dict[food_category_name].append(db_recipe_ingredient)

        # build a response object list from the dictionary
        return [schemas.RecipeIngredientWithFoodCategory(food_category=food_category_name, recipe_ingredients=db_recipe_ingredients) 
                    for food_category_name, db_recipe_ingredients 
                    in food_categories_dict.items()]
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Internal Server Error (unable to read recipe ingredients with food categories)")