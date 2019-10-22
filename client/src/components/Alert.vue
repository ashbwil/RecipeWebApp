<template>
    <div>
        <b-alert variant="info" show>{{ message}} </b-alert>
        <br>
    </div>
</template>

<script>
export default {
    props: ['message'],
};
</script>