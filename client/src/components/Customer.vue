<template>
  <div>
    <h1>{{ customer.name }}</h1>
    <p>UserID</p>
    <p>{{ customer.userid }}</p>
    <p>Email</p>
    <p>{{ customer.email }}</p>
    <p>Timezone</p>
    <p>{{ customer.timezone }}</p>
  </div>
</template>

<script>
export default {
  props: ['customer'],
};
</script>
