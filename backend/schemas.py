from pydantic import BaseModel, ConfigDict
from typing import Optional

class Unit(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    is_metric: bool

class FoodItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

class FoodCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str]
    food_items: list[FoodItem] = []

class RecipeIngredient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    food_item: str
    unit: str
    amount: float

class RecipeIngredientWithFoodCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    food_category: str
    recipe_ingredients: list[RecipeIngredient]

class RecipeStep(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    description: str

class Recipe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    recipe_category: str
    time_minutes: int
    recipe_steps: list[RecipeStep] = []
    recipe_ingredients: list[RecipeIngredient] = []

class RecipeUpdate(Recipe):
    name: Optional[str] = None
    recipe_category: Optional[str] = None
    time_minutes: Optional[int] = None

class RecipeCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: Optional[str]


