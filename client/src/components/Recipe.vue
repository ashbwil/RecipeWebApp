<template>
  <div class="container">
    <button type="button" class="btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Recipes',
  data() {
    return {
      msg: '',
    };
  },
  methods:{
    getMessage(){
      const path = 'http://localhost:5000/recipes';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    },
    created(){
      this.getMessage();
  },
};
</script>