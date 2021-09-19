<script lang="ts">
	import { onMount, onDestroy } from "svelte";
	import CodeMirror from "codemirror";

	import "codemirror/lib/codemirror.css";
	import "codemirror/theme/lesser-dark.css";
	import "codemirror/mode/vhdl/vhdl";

	import { submitTest } from "./api";
    import { createAndDownloadFile } from "./utils";

	let textarea: HTMLTextAreaElement;
	let editor: CodeMirror.EditorFromTextArea;

	const config: CodeMirror.EditorConfiguration = {
		lineNumbers: true,
		lineWrapping: true,
		theme: "lesser-dark",
		mode: "vhdl",
		indentWithTabs: true,
		smartIndent: false,
	};

	const initialValue: string = `entity adder is
	port(
		i0, i1 : in bit;
		ci : in bit;
		s : out bit;
		co : out bit
	);
end adder;`;

	onMount(() => {
		editor = CodeMirror.fromTextArea(textarea, config);
		editor.setSize("100%", "100%");
		editor.setValue(initialValue);
	});

	onDestroy(() => {
		editor.toTextArea();
	});

	async function onSubmit(): Promise<void> {
        let userCode = editor.getValue();
		let vcd: string = await submitTest(userCode);
        createAndDownloadFile(vcd, "result", "vcd");
	}
</script>

<main>
	<h1>HDL Judge</h1>
	<p>Implement an adder with the following interface</p>
	<div id="editor">
		<textarea name="code" bind:this={textarea}></textarea>
	</div>
	<button on:click={onSubmit}>Submit</button>
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
		text-align: left;
		width: 500px;
		height: 300px;
		margin: auto;
	}

	button {
		margin-top: 15px;
	}
</style>
