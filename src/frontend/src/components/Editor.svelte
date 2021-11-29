<script lang="ts">
    import {runTest} from "../utils/api/api";
    import { createAndDownloadFile } from "../utils/utils";
    import Tabs from "../components/Tabs.svelte";
    import TextEditor from "../components/TextEditor.svelte";
    import CodeMirror from "codemirror";
    import { onMount } from "svelte";
    import Loading from "../components/Loading.svelte";

    export let projectId: any;
    export let getFiles: Function;
    export let saveFiles: Function;
    export let deleteFiles: Function;
    export let showReset: boolean = false;
    export let showDelete: boolean = true;
    export let showAdd: boolean = true;
    export let showRun: boolean = true;
    export let allowRename: boolean = true;
    let editor: CodeMirror.EditorFromTextArea;
    let message: string = "";
    let resultFileContent: string;
    let resultFileName: string;
    let currentTab: number = 0;
    let tabItems = [];
    let loading = false;
    let waveDiv;
    let toplevelEntity = "";
    let selected;
    let testbenchName = "tb.vhdl";

    onMount(async () => {
        editor.on("change", onChangeContent);

        await setTabItems();
    });

    async function setTabItems() {
        tabItems = await getFiles(projectId);
        if (tabItems.length > 0)
            editor.setValue(tabItems[currentTab].content);
    }

    async function onRunFiles(): Promise<void> {
        await onSaveFiles();
        loading = true;
        let response = await runTest(projectId);
        loading = false;

        message = response.status == "OK"
                ? "Código simulado com sucesso.\n"
                : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        resultFileContent = response.result;
        resultFileName = response.filename;
    }

    async function onSaveFiles(): Promise<void> {
        loading = true;
        try {
            await saveFiles(tabItems, projectId);
            message = "Arquivos salvos.\n";
        } catch {
            message = "Não foi possível salvar os arquivos.\n";
        } finally {
            loading = false;
        }
    }

    async function removeFiles() {
        if (tabItems.length > 0) {
            let ids = tabItems.map(x => x.id);
            for (let id of ids) {
                if (id) {
                    await deleteFiles(id);
                }
            }
        }
    }

    function onChangeContent() {
        tabItems[currentTab].content = editor.getValue();
        if (tabItems[currentTab].filename === "wave.json") {
            window.WaveDrom.RenderWaveForm(0, JSON.parse(tabItems[currentTab].content), "WaveJSON_");
        }
    }

    function onChangeTab(event) {
        changeTab(event.detail);
    }

    function changeTab(newTabIndex) {
        currentTab = newTabIndex;
        editor.setValue(tabItems[newTabIndex].content);
    }

    function addTab() {
        let newFilename = "nova_aba";

        tabItems.push({
            filename: newFilename,
            content: "",
        });
        tabItems = tabItems;
        changeTab(tabItems.length-1);
    }

    function renameTab(event) {
        let newName = prompt("Digite o nome do arquivo", tabItems[event.detail].filename);
        if (newName) {
            tabItems[event.detail].filename = newName;
        }
    }

    async function deleteTab() {
        let confirmDeleteTab = confirm(`Deseja apagar a aba ${tabItems[currentTab].filename}?`);
        if (confirmDeleteTab) {
            loading = true;
            if (tabItems.length > 0) {
                await deleteFiles(tabItems[currentTab].id);
            }
            loading = false;
            tabItems.splice(currentTab, 1);
            let newTabIndex = currentTab > tabItems.length-1 ? tabItems.length-1 : currentTab;

            if (newTabIndex < 0) {
                editor.setValue("");
                tabItems = tabItems;
                return;
            }

            currentTab = newTabIndex;
            editor.setValue(tabItems[newTabIndex].content);
            tabItems = tabItems;
        }
    }

    async function onReset() {
        loading = true;
        await removeFiles();
        await setTabItems();
        await saveFiles(tabItems, projectId);
        loading = false;
    }
</script>

<section class="panel">
    <Tabs
        activeTabValue={currentTab}
        items={tabItems}
        on:changeTab={onChangeTab}
        on:addTab={addTab}
        on:renameTab={renameTab}
        on:deleteTab={deleteTab}
        showAdd={showAdd}
        showDelete={showDelete}
        allowRename={allowRename}
    />

    <nav>
        <div class="controls">
            {#if resultFileContent}
                <button on:click={() => createAndDownloadFile(resultFileContent, resultFileName)}>
                    Download VCD
                </button>
                <button on:click={() => window.open("http://raczben.pythonanywhere.com/")}>
                    Abrir visualizador de forma de onda
                </button>
            {/if}
            {#if showReset}
                <button on:click={onReset}>Reset</button>
            {/if}
            <button on:click={onSaveFiles}>Salvar</button>
            {#if showRun}
                <button on:click={onRunFiles}>Rodar</button>
            {/if}
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        <div class="message">
            <div
                id="WaveJSON_0"
                class={tabItems && currentTab && tabItems[currentTab] && tabItems[currentTab].filename.endsWith(".json")
                    ? "visible"
                    : "hidden"}
            ></div>
            {#if loading}
                <Loading />
            {:else}
                {message}
            {/if}
        </div>
    </aside>
</section>

<style>
    .visible {
        visibility: visible;
        margin-bottom: 1rem;
    }

    .hidden {
        visibility: hidden;
        height: 0;
        width: 0;
        margin: 0;
    }

    aside {
        padding: 0;
    }

    .message {
        padding: 1rem;
        box-sizing: border-box;
    }

    .panel {
        height: 100%;
        width: 100%;
        display: grid;
        grid-template: 2.3em auto / 1fr 1fr;
        grid-template-areas:
            "t n"
            "e r";
    }

    nav {
        background: #333;
        grid-area: n;
        display: flex;
        justify-content: flex-end;
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
        color: antiquewhite;
        white-space: pre-line;
    }

    button {
        margin: 0 0.3rem 0 0;
        padding: 0.3rem;
    }
</style>
