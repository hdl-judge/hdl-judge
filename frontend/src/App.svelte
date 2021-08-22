<script lang="ts">
	import { AceEditor } from "svelte-ace";
	import "brace/mode/vhdl";
	import "brace/theme/monokai";

	let text = `entity adder is
	port(
		i0, i1 : in bit;
		ci : in bit;
		s : out bit;
		co : out bit
	);
end adder;`;
</script>

<main>
	<h1>HDL Judge</h1>
	<p>Implement an adder with the following interface</p>
	<div id="editor">
		<AceEditor
			width="100%"
			height="300px"
			lang="vhdl"
			theme="monokai"
			bind:value={text}
		/>
	</div>
	<form action="http://127.0.0.1:8000/test/execute" method="post">
		<input name="code" type="text" value={text} hidden>
		<button>Submit</button>
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
		margin: 0.3em 0;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	#editor {
		width: 500px;
		margin: auto;
		margin-bottom: 10px;
	}
</style>