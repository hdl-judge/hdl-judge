<script lang="ts">
    import { executeTest } from './api'
    
	let files: FileList;

	async function upload() {
		let result = await executeTest(files[0]);
        console.log(result);
	}
</script>

<main>
	<h1>HDL Judge</h1>
	<p>Choose a .vhd file to be tested</p>
	<input id="fileUpload" type="file" bind:files>
	{#if files}
		<button on:click={upload}>Submit</button>
	{:else}
		<button disabled>Submit</button>
	{/if}
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