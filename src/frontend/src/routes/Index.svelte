<script lang="ts">
    import {submitTest, File} from "../utils/api";
    import {createAndDownloadFile} from "../utils/utils";
    import {ResponseStatus} from "../utils/response_status";
    import Tabs from "../components/Tabs.svelte";
    import TextEditor from "../components/TextEditor.svelte";
    import CodeMirror from "codemirror";
    import {onMount} from "svelte";

    let editor: CodeMirror.EditorFromTextArea;
    let message: string = "";
    let vcd: string;
    let tabItems: File[] = [
        {filename: "intrucoes.txt", content: "Implemente um somador com a interface apresentada"},
        {filename: "adder.vhdl", content: `entity adder is
	port(
		i0, i1 : in bit;
		ci : in bit;
		s : out bit;
		co : out bit
	);
end adder;`},
        {filename: "wave.json", content: `{
    "signal": [
        {"dir": "in",  "name": "i0", "type": "bit", "wave": "00001111"},
        {"dir": "in",  "name": "i1", "type": "bit", "wave": "00110011"},
        {"dir": "in",  "name": "ci", "type": "bit", "wave": "01010101"},
        {"dir": "out", "name": "s",  "type": "bit", "wave": "01101001"},
        {"dir": "out", "name": "co", "type": "bit", "wave": "00010111"}
    ]
}`}
    ];
    let currentTab: number = 0;

    async function onSubmit(): Promise<void> {
        tabItems[currentTab].content = editor.getValue();

        let response = await submitTest(tabItems);

        message = response.status == ResponseStatus.OK
                ? "Código simulado com sucesso.\n"
                : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
    }

    onMount(() => {
        editor.setValue(tabItems[currentTab].content);
    });

    function onChangeTab(event) {
        changeTab(event.detail);
    }

    function changeTab(newTabIndex) {
        tabItems[currentTab].content = editor.getValue();
        editor.setValue(tabItems[newTabIndex].content);
        currentTab = newTabIndex;
    }

    function addTab() {
        tabItems.push({filename: "nova_aba", content: ""});
        changeTab(tabItems.length-1);
    }

    function renameTab(event) {
        let newName = prompt("Digite o nome do arquivo", tabItems[event.detail].filename);
        if (newName)
            tabItems[event.detail].filename = newName
    }

    function deleteTab() {
        let confirmDeleteTab = confirm(`Deseja apagar a aba ${tabItems[currentTab].filename}?`);
        if (confirmDeleteTab) {
            tabItems.splice(currentTab, 1);
            let newTabIndex = currentTab > tabItems.length-1 ? tabItems.length-1 : currentTab;
            editor.setValue(tabItems[newTabIndex].content);
            currentTab = newTabIndex;
            tabItems = tabItems;
        }
    }
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>

    <section class="tabs">
        <Tabs
            activeTabValue={currentTab}
            items={tabItems}
            on:changeTab={onChangeTab}
            on:addTab={addTab}
            on:renameTab={renameTab}
            on:deleteTab={deleteTab}
        />
    </section>

    <nav>
        <div class="controls">
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>Download VCD</button>
            {/if}
            <button on:click={onSubmit}>Enviar</button>
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        {message}
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
                "t n"
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
        justify-content: flex-end;
    }

    .tabs {
        background: #333;
        grid-area: t;
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

    button {
        margin: 0.5em 1em;
    }
</style>
