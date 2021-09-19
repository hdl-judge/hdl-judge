<script lang="ts">
	import { onMount, onDestroy } from "svelte";
	import CodeMirror from "codemirror";

	import "codemirror/lib/codemirror.css";
	import "codemirror/theme/lesser-dark.css";
	import "codemirror/mode/vhdl/vhdl";

    export let value: string = "";

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

	onMount(() => {
		editor = CodeMirror.fromTextArea(textarea, config);
		editor.setSize("100%", "100%");
		editor.setValue(value);
        editor.on('change', () => value = editor.getValue());
	});

	onDestroy(() => {
		editor.toTextArea();
	});
</script>

<textarea name="code" bind:this={textarea}></textarea>