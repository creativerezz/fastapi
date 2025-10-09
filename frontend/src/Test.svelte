<script>
  let count = 0;
</script>

<div class="p-8 bg-blue-500 text-white">
  <h1 class="text-4xl font-bold">Test Component</h1>
  <p>Count: {count}</p>
  <button class="btn btn-primary mt-4" on:click={() => count++}>Increment</button>
</div>
