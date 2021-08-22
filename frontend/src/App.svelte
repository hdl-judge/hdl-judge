<script lang="ts">
	let files: FileList;
</script>

<main>
	<h1>HDL Judge</h1>
	<p>Choose a .vhd file to be tested</p>
	<form action="http://127.0.0.1:8000/test/execute" enctype="multipart/form-data" method="post">
		<input name="file" type="file" bind:files>
		{#if files}
			<button>Submit</button>
		{:else}
			<button disabled>Submit</button>
		{/if}
	</form>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>