// HTML
<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1>Recipes</h1>
              <hr><br>
              <alert :message=message v-if="showMessage"></alert>
              <button type="button" class="btn btn-info btn-sm" v-b-modal.list-modal @click="listButton()">See List</button>
              <br><br>
              <button type="button" class="btn btn-info btn-sm" v-b-modal.recipe-modal>Add New Recipe</button>
              <br><br>
              <table class="table table-hover">
                  <thead>
                      <tr>
                          <th scope="col">Name</th>
                          <th scope="col">Category</th>
                          <th scope="col">Meal</th>
                          <th scope="col">Added to list?</th>
                          <th></th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(recipe,index) in recipes" :key="index">
                          <td>{{recipe.title}}</td>
                          <td>{{recipe.category}}</td>
                          <td>{{recipe.meal}}</td>
                          <td>
                              <span v-if="recipe.added">Yes</span>
                              <span v-else>No</span>
                          </td>
                          <td>
                              <div class="btn-group" role="group">
                                <button type="button" class="btn btn-primary btn-sm" v-b-modal.recipe-update-modal @click="editRecipe(recipe)">Edit</button>
                                <button type="button" class="btn btn-info btn-sm"  @click="addToListYes(recipe)" v-show="!recipe.added">Add to List</button>
                                <button type="button" class="btn btn-info btn-sm"  @click="addToListNo(recipe)" v-show="recipe.added">Remove from List</button>
                                <button type="button" class="btn btn-primary btn-sm">Recipe</button>
                                <button type="button" class="btn btn-info btn-sm" @click="onDeleteRecipe(recipe)">Delete</button>
                              </div>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  <b-modal
    id="recipe-modal"
    title="Add a new recipe"
    hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                  label="Title:"
                  label-for="form-title-input">
          <b-form-input id="form-title-input"
                        type="text"
                        v-model="addRecipeForm.title"
                        required
                        placeholder="Enter Title">
          </b-form-input>
    </b-form-group>
    <b-form-group id="form-category-group"
                  label="Category:"
                  label-for="form-category-input">
          <b-form-input id="form-category-input"
                        type="text"
                        v-model="addRecipeForm.category"
                        required
                        placeholder="Enter Category">
          </b-form-input>
    </b-form-group>
        <b-form-group id="form-meal-group"
                  label="Meal:"
                  label-for="form-meal-input">
          <b-form-input id="form-meal-input"
                        type="text"
                        v-model="addRecipeForm.meal"
                        required
                        placeholder="Enter which meal this is typically eaten at">
          </b-form-input>
        </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </b-modal>
  <b-modal ref="editRecipeModal"
           id="recipe-update-modal"
           title="Edit"
           hide-footer>
    <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
    <b-form-group id="form-title-edit-group"
                  label="Title:"
                  label-for="form-title-edit-input">
        <b-form-input id="form-title-edit-input"
                      type="text"
                      v-model="editForm.title"
                      required
                      placeholder="Enter Title">
        </b-form-input>
    </b-form-group>
    <b-form-group id="form-category-edit-group"
                  label="Category:"
                  label-for="form-category-edit-input">
      <b-form-input id="form-category-edit-input"
                    type="text"
                    v-model="editForm.category"
                    required
                    placeholder="Enter Category">
      </b-form-input>
    </b-form-group>
        <b-form-group id="form-meal-edit-group"
                  label="Meal:"
                  label-for="form-meal-edit-input">
      <b-form-input id="form-meal-edit-input"
                    type="text"
                    v-model="editForm.meal"
                    required
                    placeholder="Enter what meal this would typically be eaten at">
      </b-form-input>
    </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
    </b-form>
  </b-modal>
  <b-modal ref="listModal"
           id="list-modal"
           title="LIST"
           hide-footer>
      <b-card id="form-recipes-group"
                    title="Recipes:">
                    <p>{{addedRecipes}}</p>
      </b-card>
      <b-card id="form-ingredients-group"
                    title="Ingredients:">
                    <p>{{ingredients}}</p>
      </b-card>
  </b-modal>
  </div>
</template>

// Javascript
<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      addedRecipes:[],
      ingredients:[],
      recipes: [],
      addRecipeForm:{
        title: '',
        category:'',
        meal: '',
        added: false,
      },
      editForm:{
        id: '',
        title: '',
        category:'',
        meal: '',
        added: false,
      },
      message: '',
      showMessage: false,
    };
  },
  components:{
    alert:Alert,
  },

  methods: {
    listButton(){
      this.getAddedRecipes(),
      this.getIngredients()
    },
    removeFromList(recipeID){
      const path = `http://localhost:5000/removefromlist/${recipeID}`
      axios.post(path)
    },
    updateList(recipeID){
      const path = `http://localhost:5000/addtolist/${recipeID}`
      axios.post(path)
    },
    getAddedRecipes() {
    const path = 'http://localhost:5000/recipelist';
    axios.get(path)
      .then((res) => {
        this.addedRecipes = res.data.added_recipes;
        console.log(this.addedRecipes)
      })
      .catch((error) => {
        console.error(error);
      });
    },
    getIngredients() {
      const path = 'http://localhost:5000/ingredients';
      axios.get(path)
        .then((res) => {
          this.ingredients = res.data.ingredient_list;
          console.log(this.ingredients)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addToListYes(recipe){
      recipe.added = true;
      this.updateList(recipe.id)
    },
    addToListNo(recipe){
      recipe.added = false;
      console.log('removing', recipe.id, 'from list')
      this.removeFromList(recipe.id) 
    },
    removeRecipe(recipeID){
      const path = `http://localhost:5000/recipes/${recipeID}`;
      axios.delete(path)
        .then(()=>{
          this.getRecipes();
          this.message = 'Recipe Removed From Database';
          this.showMessage = true;
        })
        .catch((error) =>{
          console.error(error);
          this.getRecipes();
        });
    },
    onDeleteRecipe(recipe){
      this.removeRecipe(recipe.id);
    },
    updateRecipe(payload, recipeID){
      const path = `http://localhost:5000/recipes/${recipeID}`;
      axios.put(path, payload)
        .then((response)=>{
          this.getRecipes();
          this.showMessage = false;
        })
        .catch((error) => {
          console.error(error)
          this.getRecipes();
        });
    },

    onResetUpdate(evt){
      evt.preventDefault();
      this.$refs.editRecipeModal.hide();
      this.initForm();
      this.getRecipes();
    },

    editRecipe(recipe){
      this.editForm = recipe;
    },

    onSubmitUpdate(evt){
      evt.preventDefault();
      this.$refs.editRecipeModal.hide();
      let added = false;
      if (this.editForm.added[0]) added = true;
      const payload = {
        title: this.editForm.title,
        category: this.editForm.category,
        meal: this.editForm.meal,
        added,
      };
      this.updateRecipe(payload, this.editForm.id);
    },

    getRecipes() {
      const path = 'http://localhost:5000/recipes';
      axios.get(path)
        .then((res) => {
          this.recipes = res.data.recipes;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    addRecipe(payload){
      const path = 'http://localhost:5000/recipes';
      axios.post(path, payload)
        .then(() => {
          this.getRecipes();
          this.message = 'Recipe Added';
          this.showMessage = true;
        })
        .catch((error)=>{
          console.log(error);
          this.getRecipes();
        });
    },

    initForm(){
      this.addRecipeForm.title = '';
      this.addRecipeForm.category = '';
      this.addRecipeForm.meal ='';
      this.editForm.id ='';
      this.editForm.title = '';
      this.editForm.category='';
      this.editForm.meal='';
      this.editForm.added = [];
    },

    onSubmit(evt){
      evt.preventDefault();
      this.$bvModal.hide('recipe-modal');
      // this.$refs.addRecipeModal.hide();
      let added = false;
      if(this.addRecipeForm.added[0]) added = true;
      const payload = {
        title: this.addRecipeForm.title,
        category: this.addRecipeForm.category,
        meal: this.addRecipeForm.meal
      };
          this.addRecipe(payload);
          this.initForm();
    },

    onReset(evt) {
      evt.preventDefault();
      this.$bvModal.hide('recipe-modal');
      // this.$refs.addRecipeModal.hide();
      this.initForm();
    },
  },

  created() {
    this.getRecipes();
  },
};
</script>

// CSS
<style scoped>
.btn-info{
  background-color: rgb(236, 14, 162);
  border-color: rgb(236, 14, 162);
}
.btn-primary{
  background-color:rgb(230, 134, 198);
  border-color: rgb(230, 134, 198);

}
.btn-danger{
  background-color: blueviolet;
  border-color: blueviolet;
}

</style>