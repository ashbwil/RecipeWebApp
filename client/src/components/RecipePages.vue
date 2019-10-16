<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1>Recipes</h1>
              <hr><br><br>
              <button type="button" class="btn btn-success btn-sm">See List</button>
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
                                <button type="button" class="btn-warning btn-sm">Recipe</button>
                                <button type="button" class="btn btn-danger btn-sm">Add to List</button>
                              </div>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </div>
  </template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      recipes: [],
    };
  },
  methods: {
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
  },
  created() {
    this.getRecipes();
  },
};
</script>