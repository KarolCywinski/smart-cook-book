from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional

from database import Base

class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    recipe: Mapped[str] = mapped_column(ForeignKey('recipes.name', ondelete="cascade", onupdate="cascade"), 
                                        primary_key=True)
    food_item: Mapped[str] = mapped_column(ForeignKey('food_items.name'), primary_key=True)
    unit: Mapped[str] = mapped_column(ForeignKey('units.name'))
    amount: Mapped[float]

class Unit(Base):
    __tablename__ = 'units'

    name: Mapped[str] = mapped_column(primary_key=True)
    is_metric: Mapped[bool]
    recipe_ingredients: Mapped[list[RecipeIngredient]] = relationship()

class FoodItem(Base):
    __tablename__ = 'food_items'

    name: Mapped[str] = mapped_column(primary_key=True)
    food_category: Mapped[str] = mapped_column(ForeignKey('food_categories.name'))
    recipe_ingredients: Mapped[list[RecipeIngredient]] = relationship()

class FoodCategory(Base):
    __tablename__ = 'food_categories'

    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    food_items: Mapped[list[FoodItem]] = relationship()

class RecipeStep(Base):
    __tablename__ = 'recipe_steps'

    number: Mapped[int] = mapped_column(primary_key=True)
    recipe: Mapped[str] = mapped_column(ForeignKey('recipes.name', ondelete="cascade", onupdate="cascade"), 
                                        primary_key=True)
    description: Mapped[str]

class Recipe(Base):
    __tablename__ = 'recipes'

    name: Mapped[str] = mapped_column(primary_key=True)
    recipe_category: Mapped[str] = mapped_column(ForeignKey('recipe_categories.name'))
    time_minutes: Mapped[int]
    recipe_steps: Mapped[list[RecipeStep]] = relationship(passive_deletes=True, passive_updates=True)
    recipe_ingredients: Mapped[list[RecipeIngredient]] = relationship(passive_deletes=True, passive_updates=True)

class RecipeCategory(Base):
    __tablename__ = 'recipe_categories'

    name: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]]
    recipes: Mapped[list[Recipe]] = relationship()