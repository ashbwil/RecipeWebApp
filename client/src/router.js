import Vue from 'vue';
import Router from 'vue-router';
import Recipe from './components/Recipe.vue';
import RecipePages from './components/RecipePages.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/Recipes',
      name: 'Recipe Pages',
      component: RecipePages,
    },
    {
      path: '/',
      name: 'Recipes',
      component: Recipe,

    },

  ],
});
