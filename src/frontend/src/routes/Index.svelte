<script lang="ts">
	import TextEditor from "../components/TextEditor.svelte";

	import { submitTest } from "../utils/api";
    import { createAndDownloadFile } from "../utils/utils";
    import { ResponseStatus } from "../utils/response_status";

    let userCode: string = `entity adder is
	port(
		i0, i1 : in bit;
		ci : in bit;
		s : out bit;
		co : out bit
	);
end adder;`;
    let message: string;
    let vcd: string;

	async function onSubmit(): Promise<void> {
        console.log(userCode)
		let response = await submitTest(userCode);

        message = response.status == ResponseStatus.OK
            ? "Código simulado com sucesso.\n"
            : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
	}
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>
    <nav>
    	<div class="instruction">Implemente um somador com a seguinte interface</div>
        <div class="controls">
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>Download VCD</button>
            {/if}
            <button on:click={onSubmit}>Enviar</button>
        </div>
    </nav>
    <section class="editor">
        <TextEditor bind:value={userCode}/>
    </section>
    <aside class="results">
        {#if message}
            {message}
        {/if}
    </aside>
</main>

<style>
	main {
        height: 100%;
        width: 100%;
        display: grid;
        grid-template: 5em 3em auto / 1fr 1fr;
        grid-template-areas:
                "h h"
                "n n"
                "e r";
	}

    header {
        background: #262626;
        grid-area: h;
    }

    nav {
        background: #333;
        grid-area: n;
        display: flex;
        justify-content: space-between;
    }

    .editor {
        grid-area: e;
        overflow-y: auto;
        font-size: 1.3em;
    }

    .results {
        background: #262626;
        grid-area: r;
        border-left: 3px solid #333;
        padding: 1.3em;
        color: antiquewhite;
        white-space: pre-line;
    }

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
		margin: auto 10px;
	}

    .instruction {
        font-size: 1.1em;
        color: antiquewhite;
        display: inline;
        margin: auto 1em;
    }

    button {
        margin: 0.5em 1em;
    }
</style>
