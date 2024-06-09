from sqlalchemy.orm import Session

import models, schemas

# Database operations

# Recipes
# Create
def create_recipe(db: Session, recipe: schemas.Recipe):
    # separate regular column attributes from relations attributes
    recipe_ingredients = [models.RecipeIngredient(**x.model_dump()) for x in recipe.recipe_ingredients]
    recipe_steps = [models.RecipeStep(**x.model_dump()) for x in recipe.recipe_steps]
    del recipe.recipe_ingredients
    del recipe.recipe_steps
            
    # create db model object from request body excluding relations attributes
    db_recipe = models.Recipe(**recipe.model_dump())

    # add relations attributes from request body to db model object 
    db_recipe.recipe_ingredients = recipe_ingredients
    db_recipe.recipe_steps = recipe_steps

    # add new record to db
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
# Read
def get_recipes(db: Session, recipe_category: str):
    return db.query(models.Recipe).filter(models.Recipe.recipe_category == recipe_category).all()

def get_recipe(db: Session, recipe_name: str):
    return db.query(models.Recipe).filter(models.Recipe.name == recipe_name).first()

# Update
def update_recipe(db: Session, recipe: schemas.RecipeUpdate, db_recipe: models.Recipe):
    # separate regular column attributes from relations attributes
    recipe_ingredients = None
    if "recipe_ingredients" in recipe.model_fields_set:
        recipe_ingredients = [models.RecipeIngredient(**x.model_dump()) for x in recipe.recipe_ingredients]
        del recipe.recipe_ingredients
    
    recipe_steps = None
    if "recipe_steps" in recipe.model_fields_set:
        recipe_steps = [models.RecipeStep(**x.model_dump()) for x in recipe.recipe_steps]
        del recipe.recipe_steps

    # update db model object fields from request body excluding relations attributes
    for key, value in recipe.model_dump(exclude_unset=True).items():
        setattr(db_recipe, key, value)

    # rebuild db model object relations from request body if set
    if recipe_ingredients is not None:
        for db_recipe_ingredient in db_recipe.recipe_ingredients:
            db.delete(db_recipe_ingredient)
        # set part of primary key for each new recipe ingredient
        for recipe_ingredient in recipe_ingredients:
            recipe_ingredient.recipe = db_recipe.name
        db_recipe.recipe_ingredients = recipe_ingredients

    if recipe_steps is not None:
        for db_recipe_step in db_recipe.recipe_steps:
            db.delete(db_recipe_step)
        # set part of primary key for each new recipe step
        for recipe_step in recipe_steps:
            recipe_step.recipe = db_recipe.name
        db_recipe.recipe_steps = recipe_steps
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
    
# Delete
def delete_recipe(db: Session, db_recipe: models.Recipe):
    db.delete(db_recipe)
    db.commit()

# Recipe categories
# Read
def get_recipe_categories(db: Session):
    return db.query(models.RecipeCategory).all()

# Units
# Read
def get_units(db: Session):
    return db.query(models.Unit).all()

# Food categories
# Read
def get_food_categories(db: Session):
    return db.query(models.FoodCategory).all()

# Joined recipe ingredients with their food categories
# Read
def get_recipe_ingredients(db: Session, recipe_name: str):
    return  (db
            .query(models.RecipeIngredient, models.FoodItem.food_category)
            .filter(models.RecipeIngredient.recipe == recipe_name)
            .join(models.FoodItem, models.FoodItem.name == models.RecipeIngredient.food_item)
            .all())

# Create initial data for each table
def create_exemplary_data(db: Session):
    db.add_all([
        models.Unit(name='kg', is_metric=True),
        models.Unit(name='g', is_metric=True),
        models.Unit(name='ml', is_metric=True),
        models.Unit(name='lbs', is_metric=False),
        models.Unit(name='pcs', is_metric=False),
        models.Unit(name='oz', is_metric=False),
        models.Unit(name='ft', is_metric=False),
        models.Unit(name='tbsp', is_metric=False),
        models.Unit(name='tsp', is_metric=False),
        models.Unit(name='pinch', is_metric=False)
    ])

    # source of descriptions: https://www.nia.nih.gov/health/healthy-eating-nutrition-and-diet/healthy-eating-you-age-know-your-food-groups
    db.add_all([  
        models.FoodCategory(name='Vegetables', 
                            description='Vegetables come in a wide variety of colors, flavors, and textures. They contain vitamins and minerals, carbohydrates, and are an important source of fiber.'),
        models.FoodCategory(name='Grains', 
                            description='Any food made from wheat, rye, rice, oats, cornmeal, barley, or other cereal grain is a grain product. This includes bread and pasta, breakfast cereal, grits, tortillas, and even popcorn.'),
        models.FoodCategory(name='Fruits', 
                            description='Fruits, like vegetables, contain carbohydrates and provide extra fiber that helps keep your digestive system moving. For even more fiber, eat fruits with the skin on — just make sure you wash all fruits thoroughly before eating.'),
        models.FoodCategory(name='Dairy', 
                            description='Consuming dairy helps older adults maintain strong bones and provides several vital nutrients, including calcium, potassium, and vitamin D. For your heart health, pick from the many low-fat or fat-free choices in the dairy group.'),
        models.FoodCategory(name='Beverages', 
                            description='Although many beverages can be part of a healthy eating pattern, some add calories without adding nutritional value and you should avoid them.'),
        models.FoodCategory(name='Protein Foods', 
                            description="Proteins are often called the body's building blocks. They are used to build and repair tissues, and also help your body fight infection. Your body uses extra protein for energy."),
        models.FoodCategory(name='Added sugars', 
                            description='Limit the consumption of foods high in added sugar, which include sweetened cereals, highly processed snack foods such as cookies and cakes, dairy desserts, and many items marketed as low-fat.'),
        models.FoodCategory(name='Seasonings', 
                            description=None),
    ])

    db.add_all([
        models.FoodItem(name='Potato', food_category='Vegetables'),
        models.FoodItem(name='Carrot', food_category='Vegetables'),
        models.FoodItem(name='Onion', food_category='Vegetables'),
        models.FoodItem(name='Green onion', food_category='Vegetables'),
        models.FoodItem(name='Garlic', food_category='Vegetables'),
        models.FoodItem(name='Cornbread', food_category='Grains'),
        models.FoodItem(name='Graham bread', food_category='Grains'),
        models.FoodItem(name='Fusilli pasta', food_category='Grains'),
        models.FoodItem(name='Rice cereal', food_category='Grains'),
        models.FoodItem(name='Apple', food_category='Fruits'),
        models.FoodItem(name='Pear', food_category='Fruits'),
        models.FoodItem(name='Butter', food_category='Dairy'),
        models.FoodItem(name='Cheddar cheese', food_category='Dairy'),
        models.FoodItem(name='Milk', food_category='Dairy'),
        models.FoodItem(name='Beer', food_category='Beverages'),
        models.FoodItem(name='Cider', food_category='Beverages'),
        models.FoodItem(name='Beef broth', food_category='Beverages'),
        models.FoodItem(name='Ground Beef', food_category='Protein Foods'),
        models.FoodItem(name='Marshmallows', food_category='Added sugars'),
        models.FoodItem(name='Salt', food_category='Seasonings'),
        models.FoodItem(name='Pepper', food_category='Seasonings'),
        models.FoodItem(name='Worcestershire sauce', food_category='Seasonings'),
        models.FoodItem(name='Ketchup', food_category='Seasonings')
    ])

    # source of descriptions: https://en.wikipedia.org/wiki/Main_Page
    db.add_all([
        models.RecipeCategory(name='Breakfast', 
                              description='Breakfast is the first meal of the day usually eaten in the morning. The word in English refers to breaking the fasting period of the previous night.'),
        models.RecipeCategory(name='Lunch', 
                              description='Lunch is a meal eaten around the middle of the day. It is commonly the second meal of the day, after breakfast, and varies in size by culture and region.'),
        models.RecipeCategory(name='Dessert', 
                              description='Dessert is a course that concludes a meal. The course consists of sweet foods, such as cake, biscuit, ice cream and possibly a beverage such as dessert wine and liqueur.'),
    ])

    # source of recipes: https://tasty.co/
    db.add_all([
        models.Recipe(name='One-Pot Cheeseburger Pasta', recipe_category='Lunch', time_minutes=30),
        models.Recipe(name='Microwave Marshmallow Treats', recipe_category='Dessert', time_minutes=5)
    ])

    db.add_all([
        models.RecipeStep(number=1, recipe='One-Pot Cheeseburger Pasta', 
                          description='In a large pot over a medium-high heat, add ground beef, onions, garlic, salt, pepper, worcestershire sauce, and ketchup. Break up the beef to incorporate the seasonings and cook until browned, about 6-7 minutes.'),
        models.RecipeStep(number=2, recipe='One-Pot Cheeseburger Pasta', 
                          description='Pour in the beef broth and one cup of water and bring to a simmer.'),
        models.RecipeStep(number=3, recipe='One-Pot Cheeseburger Pasta', 
                          description='Add the pasta and simmer for 20 minutes or until the pasta is cooked throughout and the broth has cooked down, stirring occasionally.'),
        models.RecipeStep(number=4, recipe='One-Pot Cheeseburger Pasta', 
                          description='Pour in the milk and cheese. Stir until the cheese has melted.'),
        models.RecipeStep(number=5, recipe='One-Pot Cheeseburger Pasta', 
                          description='Serve garnished with some sliced green onions'),
        models.RecipeStep(number=1, recipe='Microwave Marshmallow Treats', 
                          description='Add 1 tbs butter and 8 large marshmallows and heat in the microwave for 30 seconds.'),
        models.RecipeStep(number=2, recipe='Microwave Marshmallow Treats', 
                          description='Mix 1 cup of rice cereal and place to cool.')
    ])

    db.add_all([
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Ground Beef', unit='g', amount=455.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Onion', unit='g', amount=150.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Garlic', unit='tbsp', amount=1.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Salt', unit='tsp', amount=1.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Pepper', unit='tsp', amount=0.5),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Worcestershire sauce', unit='tbsp', amount=2.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Ketchup', unit='tbsp', amount=2.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Beef broth', unit='ml', amount=945.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Fusilli pasta', unit='g', amount=455.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Cheddar cheese', unit='g', amount=300.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Milk', unit='ml', amount=120.0),
        models.RecipeIngredient(recipe='One-Pot Cheeseburger Pasta', food_item='Green onion', unit='pinch', amount=1.0),
        models.RecipeIngredient(recipe='Microwave Marshmallow Treats', food_item='Butter', unit='tbsp', amount=1.0),
        models.RecipeIngredient(recipe='Microwave Marshmallow Treats', food_item='Marshmallows', unit='pcs', amount=8.0),
        models.RecipeIngredient(recipe='Microwave Marshmallow Treats', food_item='Rice cereal', unit='g', amount=25.0)
    ])

    db.commit()