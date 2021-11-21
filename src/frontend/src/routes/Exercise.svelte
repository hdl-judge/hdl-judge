<script lang="ts">
    import { submitTest, getFilesFromProject, saveProjectFiles } from "../utils/api";
    import { createAndDownloadFile, getStorageKey } from "../utils/utils";
    import Tabs from "../components/Tabs.svelte";
    import TextEditor from "../components/TextEditor.svelte";
    import CodeMirror from "codemirror";
    import { onMount } from "svelte";

    export let params: any = {};
    const storageKey: string = getStorageKey(params.id);
    let editor: CodeMirror.EditorFromTextArea;
    let message: string = "";
    let vcd: string;
    let currentTab: number = 0;
    let tabs: string[] = [];

    async function onSubmit(): Promise<void> {
        let storedTabItems = JSON.parse(localStorage.getItem(storageKey));

        let response = await submitTest(storedTabItems);

        // message = response.status == ResponseStatus.OK
        //         ? "Código simulado com sucesso.\n"
        //         : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
    }

    async function onSaveFiles(): Promise<void> {
        let storageKey = `project-${params.id}`;
        let storedTabItems = JSON.parse(localStorage.getItem(storageKey));

        await saveProjectFiles(storedTabItems, params.id);

        message = "Arquivos salvos.\n";
    }

    onMount(async () => {
        let stored = localStorage.getItem(storageKey);
        if (!stored) {
            let tabItems = await getFilesFromProject(params.id);
            stored = JSON.stringify(tabItems);
            localStorage.setItem(storageKey, stored);
        }
        let storedTabItems = JSON.parse(stored);
        tabs = storedTabItems.map(x => x.filename);
        editor.setValue(storedTabItems[currentTab].content);
        editor.on("change", onChangeContent);
    });

    function onChangeContent() {
        let storedTabItems = JSON.parse(localStorage.getItem(storageKey));

        storedTabItems[currentTab].content = editor.getValue();
        localStorage.setItem(storageKey, JSON.stringify(storedTabItems));
    }

    function onChangeTab(event) {
        changeTab(event.detail);
    }

    function changeTab(newTabIndex) {
        let storedTabItems = JSON.parse(localStorage.getItem(storageKey));
        currentTab = newTabIndex;
        editor.setValue(storedTabItems[newTabIndex].content);
    }

    function addTab() {
        let newFilename = "nova_aba";

        let storedTabItems = JSON.parse(localStorage.getItem(storageKey));
        storedTabItems.push({
            filename: newFilename,
            content: "",
        });
        localStorage.setItem(storageKey, JSON.stringify(storedTabItems));

        tabs.push(newFilename);
        changeTab(tabs.length-1);
    }

    function renameTab(event) {
        let newName = prompt("Digite o nome do arquivo", tabs[event.detail]);
        if (newName) {
            let storedTabItems = JSON.parse(localStorage.getItem(storageKey));
            storedTabItems[event.detail].filename = newName;
            localStorage.setItem(storageKey, JSON.stringify(storedTabItems));

            tabs[event.detail] = newName;
        }
    }

    function deleteTab() {
        let confirmDeleteTab = confirm(`Deseja apagar a aba ${tabs[currentTab]}?`);
        if (confirmDeleteTab) {
            let storedTabItems = JSON.parse(localStorage.getItem(storageKey));
            storedTabItems.splice(currentTab, 1);
            localStorage.setItem(storageKey, JSON.stringify(storedTabItems));

            tabs.splice(currentTab, 1);
            let newTabIndex = currentTab > tabs.length-1 ? tabs.length-1 : currentTab;
            currentTab = newTabIndex;
            editor.setValue(storedTabItems[newTabIndex].content);
            tabs = tabs;
        }
    }
</script>

<section class="panel">
    <Tabs
        activeTabValue={currentTab}
        items={tabs}
        on:changeTab={onChangeTab}
        on:addTab={addTab}
        on:renameTab={renameTab}
        on:deleteTab={deleteTab}
    />

    <nav>
        <div class="controls">
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>
                    Download VCD
                </button>
            {/if}
            <button on:click={onSaveFiles}>Salvar</button>
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        {message}
    </aside>
</section>

<style>
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
        padding: 1.3em;
        color: antiquewhite;
        white-space: pre-line;
    }

    button {
        margin: 0 0.3rem 0 0;
        padding: 0.3rem;
    }
</style>
