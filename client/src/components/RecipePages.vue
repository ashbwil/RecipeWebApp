<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1>Recipes</h1>
              <hr><br>
              <alert :message=message v-if="showMessage"></alert>
              <button type="button" class="btn btn-success btn-sm">See List</button>
              <br><br>
              <button type="button" class="btn btn-success btn-sm" v-b-modal.recipe-modal>Add New Recipe</button>
              <br><br>
              <table class="table table-hover">
                  <thead>
                      <tr>
                          <th scope="col">Name</th>
                          <th scope="col">Category</th>
                          <th scope="col">Added?</th>
                          <th></th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(recipe,index) in recipes" :key="index">
                          <td>{{recipe.title}}</td>
                          <td>{{recipe.category}}</td>
                          <td>
                              <span v-if="recipe.added">Yes</span>
                              <span v-else>No</span>
                          </td>
                          <td>
                              <div class="btn-group" role="group">
                                <button type="button" class="btn btn-warning btn-sm" v-b-modal.recipe-update-modal @click="editRecipe(recipe)">Edit</button>
                                <button type="button" class="btn btn-success btn-sm">Add to List</button>
                                <button type="button" class="btn btn-warning btn-sm">Recipe</button>
                                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteRecipe(recipe)">Delete</button>
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
    <b-form-group id="form-added-group">
      <b-form-checkbox-group v-model="addRecipeForm.added" id="form-checks">
        <b-form-checkbox value="true"> Added?</b-form-checkbox>
      </b-form-checkbox-group>
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
    <b-form-group id="form-added-edit-group">
      <b-form-checkbox-group v-model="editForm.added" id="form-checks">
        <b-form-checkbox value="true"> Added?</b-form-checkbox>
      </b-form-checkbox-group>
    </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
    </b-form>
  </b-modal>
  </div>
  </template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      recipes: [],
      addRecipeForm:{
        title: '',
        category:'',
        added: [],
      },
      editForm:{
      id: '',
      title: '',
      category:'',
      added: [],
    },
      message: '',
      showMessage: false,
    };
  },
  components:{
    alert:Alert,
  },

  methods: {
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
          this.message = response.data.message;
          this.showMessage = true;
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
      this.addRecipeForm.added = [];
      this.editForm.id ='';
      this.editForm.title = '';
      this.editForm.Category='';
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
        added, //property shorthand
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