const app = Vue.createApp({
    data() {
        return {
            // shopping list
            shoppingListCategories: [],
            // drop-down lists
            // units
            units: [],
            selectedUnit: null,
            // recipe categories
            recipeCategories: [],
            selectedRecipeCategory: null,
            // food categories
            foodCategories: [],
            selectedFoodCategory: null,
            // food items
            foodItems: [],
            selectedFoodItem: null,
            // recipes
            recipes: [],
            selectedRecipe: null,
            // operational states
            // mode types
            editMode: false,
            createMode: false,
            // input
            newRecipeName: null,
            newRecipeTime: null,
            amount: null,
            recipeStepDescription: null,
            // recipe copy before modifications
            selectedRecipeOriginal: null,
            // styling
            // buttons
            btnRounded: 'font-bold py-3 px-4 border-2 border-black rounded shadow',
            btnBlue: 'bg-blue-500 hover:bg-blue-400',
            btnRose: 'bg-rose-500 hover:bg-rose-400',
            btnGreen: 'bg-green-500 hover:bg-green-400',
            btnDisabled: 'disabled:opacity-50 disabled:cursor-not-allowed disabled:border-none',
            // forms
            dropDown: "py-3 px-4 rounded border border-black text-black w-full my-2",
            checkBox: "accent-cyan-500 w-6 h-6 rounded-lg mx-2",
            // other
            captionText: "font-bold text-xl"
        }
    },
    computed: {
        // check if selected recipe was changed
        isRecipeEdited() {
            if(JSON.stringify(this.selectedRecipe) == JSON.stringify(this.selectedRecipeOriginal) 
                && this.selectedRecipeOriginal.time_minutes === this.newRecipeTime
                && this.selectedRecipeOriginal.name === this.newRecipeName) {
                return false;
            }
            else {
                return true;
            }
        },
        // check if new recipe is ready to be saved
        isRecipeToAddReady() {				
            if(this.selectedRecipe.recipe_ingredients.length > 0
                || this.selectedRecipe.recipe_steps.length > 0
                || this.newRecipeName != null
                || this.newRecipeTime != null) {
                return true;
            }
            return false;
        },
        // check if all parameters are ready to create new ingredient
        isIngredientToAddReady() {
            if(this.selectedFoodItem != null 
                && this.selectedUnit != null 
                && this.amount) {
                return true;
            }
            return false;
        },
        // styling
        // lists
        orderedList() {
            if((!this.editMode) && (!this.createMode)) {
                return "list-decimal list-inside";
            }
            else {
                return "list-decimal list-inside";
            }
        },
        unorderedList() {
            if((!this.editMode) && (!this.createMode)) {
                return "list-disc list-inside";
            }
            else {
                return "list-disc list-inside";
            }
        }
    },
    watch: {
        // fetch recipes if recipe category reselected
        selectedRecipeCategory(val) {
            if(val != null) {
                this.getRecipes();
            }
            else {
                this.recipes = [];
            }
        },
        // stop edit mode after choosing different recipe from drop-down
        selectedRecipe(val) {
            if(val != null && val.hasOwnProperty('recipe_ingredients') && !(this.createMode)) {
                this.getRecipeIngredients();
            }
            this.stopEditMode();
        },
        // deselect current recipe after fetching new recipe list
        recipes(val) {
            this.selectedRecipe = null;	
        },
        // list of food items depends on selected category
        selectedFoodCategory(val) {
            if(val != null && val.hasOwnProperty('food_items')) {
                this.foodItems = val.food_items;
            }
            else {
                this.foodItems = [];
            }
        }
    },
    methods: {
        // api calls
        // fetch recipes list
        getRecipes() {
            axios
                .get(`http://127.0.0.1:8000/recipes/${this.selectedRecipeCategory.name}`)
                .then(response => {
                    this.recipes = response.data;
                })
                .catch(error => {
                    if(error.response) {
                        alert(error.response.data.detail);
                    }
                    else {
                        alert(error.message);
                    }
                });
        },
        getRecipeIngredients() {
            axios
                .get(`http://127.0.0.1:8000/recipe-ingredients/${this.selectedRecipe.name}`)
                .then(response => {
                    this.shoppingListCategories = response.data;
                })
                .catch(error => {
                    if(error.response) {
                        alert(error.response.data.detail);
                    }
                    else {
                        alert(error.message);
                    }
                });
        },
        // delete recipe
        deleteRecipe() {
            if(confirm('Do you really want to delete this recipe?')) {
                axios
                    .delete(`http://127.0.0.1:8000/recipes/${this.selectedRecipe.name}`)
                    .then(response => {
                        this.recipes = this.recipes.filter(recipe => recipe !== this.selectedRecipe);
                        // todo box saying that recipe was deleted
                    })
                    .catch(error => {
                        if(error.response) {
                            alert(error.response.data.detail);
                        }
                        else {
                            alert(error.message);
                        }
                    });
            }
        },
        // edit mode functions
        // save changes
        editRecipe() {
            // validation
            // failed
            if(!this.newRecipeName) {
                alert('You need to provide a name for the edited recipe!');
            }
            else if(!this.newRecipeTime) {
                alert('You need to provide preparation time for the edited recipe!');					
            }
            else if(this.selectedRecipe.recipe_ingredients.length === 0) {
                alert('You need to provide at least one ingredient for the edited recipe!');						
            }
            else if(this.selectedRecipe.recipe_steps.length === 0) {
                alert('You need to provide at least one preparation step for the edited recipe!');						
            }
            // succeeded
            else {
                // patch request object
                var patchRequestRecipy = {};
                var propertyNamesToExclude = ['name', 'time_minutes', 'recipe_category'];
                var propertyNames = Object.keys(this.selectedRecipeOriginal);
                // add only modified properties to patch request object
                for(propertyName of propertyNames) {
                    if(!propertyNamesToExclude.includes(propertyName)) {
                        if(
                            (Array.isArray(this.selectedRecipeOriginal[propertyName]) && JSON.stringify(this.selectedRecipeOriginal[propertyName]) !== JSON.stringify(this.selectedRecipe[propertyName]))
                            || (!(Array.isArray(this.selectedRecipeOriginal[propertyName]) && this.selectedRecipeOriginal[propertyName] !== this.selectedRecipe[propertyName]))) {
                            patchRequestRecipy[propertyName] = this.selectedRecipe[propertyName];
                        }				
                    }
                }
                if(this.selectedRecipeOriginal.name !== this.newRecipeName) {
                    patchRequestRecipy.name = this.newRecipeName;
                }
                if(this.selectedRecipeOriginal.time_minutes !== this.newRecipeTime) {
                    patchRequestRecipy.time_minutes = this.newRecipeTime;
                }
                // http patch request
                axios
                    .patch(`http://127.0.0.1:8000/recipes/${this.selectedRecipe.name}`, patchRequestRecipy)
                    .then(response => {
                        var editedRecipeIndex = this.recipes.indexOf(this.selectedRecipe);
                        this.recipes[editedRecipeIndex] = response.data;
                        this.selectedRecipe = this.recipes[editedRecipeIndex];
                    })
                    .catch(error => {
                        if(error.response) {
                            alert(error.response.data.detail);
                        }
                        else {
                            alert(error.message);
                        }
                    });
            }
        },		
        // start edit mode and prepare default values
        startEditMode() {
            // copy original recipe to check later if anything was changed
            this.selectedRecipeOriginal = JSON.parse(JSON.stringify(this.selectedRecipe));
            // prepare default values for some fields
            this.newRecipeName = this.selectedRecipeOriginal.name;
            this.newRecipeTime = this.selectedRecipeOriginal.time_minutes
            // empty fields
            this.recipeStepDescription = null;
            this.amount = null;
            this.selectedFoodCategory = null;
            this.selectedFoodItem = null;
            this.selectedUnit = null;
            // start edit mode
            this.editMode = true;
        },
        // go back to original values and stop editing
        cancelEditMode() {
            Object.assign(this.selectedRecipe, this.selectedRecipeOriginal);
            this.stopEditMode();
        },
        // stop edit mode and hide shopping list
        stopEditMode() {
            this.editMode = false;
        },
        // create mode functions	
        // save new recipe
        createRecipe() {
            // validation
            // failed
            if(!this.newRecipeName) {
                alert('New recipe needs a name!');
            }
            else if(!this.newRecipeTime) {
                alert('You need to provide preparation time for the new recipe!');					
            }
            else if(this.selectedRecipe.recipe_ingredients.length === 0) {
                alert('You need to provide at least one ingredient for the new recipe!');						
            }
            else if(this.selectedRecipe.recipe_steps.length === 0) {
                alert('You need to provide at least one preparation step for the new recipe!');						
            }
            // succeeded
            else {
                // add properties to post request object
                this.selectedRecipe.name = this.newRecipeName;
                this.selectedRecipe.time_minutes = this.newRecipeTime;		
                
                // http post request
                axios
                    .post('http://127.0.0.1:8000/recipes', this.selectedRecipe)
                    .then(response => {
                        this.createMode = false;
                        this.getRecipes();
                    })
                    .catch(error => {
                        if(error.response) {
                            alert(error.response.data.detail);
                        }
                        else {
                            alert(error.message);
                        }
                    });
            }
        },	
        // start create mode and prepare default values
        startCreateMode() {
            // cancel edit mode
            if(this.editMode) {
                this.cancelEditMode();
            }
            // start create mode
            this.createMode = true;
            // create new recipe object with empty default values
            this.selectedRecipe = {
                recipe_category: this.selectedRecipeCategory.name,
                name: null,
                time_minutes: null,
                recipe_steps: [],
                recipe_ingredients: []
            };
            // empty fields
            this.newRecipeName = null;
            this.newRecipeTime = null;
            this.recipeStepDescription = null;
            this.amount = null;
            this.selectedFoodCategory = null;
            this.selectedFoodItem = null;
            this.selectedUnit = null;
        },
        // cancel create mode
        cancelCreateMode() {
            this.selectedRecipe = null;
            this.createMode = false;
        },
        // edit/create operations on lists
        // remove recipe ingredient
        deleteRecipeIngredient(foodItemName) {
            this.selectedRecipe.recipe_ingredients = 
                this.selectedRecipe
                    .recipe_ingredients
                    .filter(ingredient => ingredient.food_item != foodItemName);
        },
        // add new recipe ingredient
        addRecipeIngredient() {
            // validation - food item repetition
            let existingIngredient = this
                                        .selectedRecipe
                                        .recipe_ingredients
                                        .find(x => x.food_item == this.selectedFoodItem.name);
            // failed
            if(!(existingIngredient === undefined)) {
                alert("This food item is already on the ingredient list");
            }
            // succeeded
            else {
                // add to list
                this.selectedRecipe.recipe_ingredients.push({
                    food_item: this.selectedFoodItem.name,
                    unit: this.selectedUnit.name,
                    amount: this.amount
                });
                // empty fields before adding next ingredient
                this.amount = null;
                this.selectedFoodItem = null;
                this.selectedFoodCategory = null;
                this.selectedUnit = null;
            }
        },
        // remove recipe step
        deleteRecipeStep(number) {
            this.selectedRecipe.recipe_steps = 
                this.selectedRecipe
                    .recipe_steps
                    .filter(step => step.number != number);
            this.recalculateStepNumbers();		
        },
        // add new recipe step
        addRecipeStep() {
            this.selectedRecipe.recipe_steps.push({
                description: this.recipeStepDescription
            });
            this.recalculateStepNumbers();

            // empty field for next step
            this.recipeStepDescription = null;
        },
        // maintain recipe steps order
        recalculateStepNumbers() {
            this.selectedRecipe.recipe_steps
                .forEach((element, index) => element.number = index);
        },
        // forms validation
        // time must be integer
        blockNonIntegerKeys(evt) {
            let nonIntegerPattern = /[^0-9]/g;
            if(evt.key.match(nonIntegerPattern) != null) {
                evt.preventDefault();
            }
        },
        // amount must be numeric
        blockNonNumericKeys(evt) {
            let nonNumericPattern = /[^0-9,]/g;
            if(evt.key.match(nonNumericPattern) != null) {
                evt.preventDefault();
            }
        }
    },
    mounted() {
        // api calls to fetch available options for drop-down lists
        // units
        axios
            .get('http://127.0.0.1:8000/units')
            .then(response => {
                this.units = response.data;
            })
            .catch(error => {
                if(error.response) {
                    alert(error.response.data.detail);
                }
                else {
                    alert(error.message);
                }
            });
        // recipe categories
        axios
            .get('http://127.0.0.1:8000/recipe-categories')
            .then(response => {
                this.recipeCategories = response.data;
            })
            .catch(error => {
                if(error.response) {
                    alert(error.response.data.detail);
                }
                else {
                    alert(error.message);
                }
            });
        // food categories
        axios
            .get('http://127.0.0.1:8000/food-categories')
            .then(response => {
                this.foodCategories = response.data;
            })
            .catch(error => {
                if(error.response) {
                    alert(error.response.data.detail);
                }
                else {
                    alert(error.message);
                }
            });
    }
});
app.mount('#app');