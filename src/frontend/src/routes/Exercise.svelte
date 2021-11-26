<script lang="ts">
    import {submitTest, getFilesFromProject, saveProjectFiles, removeProjectFile} from "../utils/api/api";
    import { createAndDownloadFile, getStorageKey } from "../utils/utils";
    import Tabs from "../components/Tabs.svelte";
    import TextEditor from "../components/TextEditor.svelte";
    import CodeMirror from "codemirror";
    import { onMount } from "svelte";
    import {userStore} from "../utils/store";
    import Loading from "../components/Loading.svelte";
    import {getSubmissonFiles, removeSubmissionFile, saveSubmissionFiles} from "../utils/api/submissions";

    export let params: any = {};
    let editor: CodeMirror.EditorFromTextArea;
    let message: string = "";
    let vcd: string;
    let currentTab: number = 0;
    let tabItems = [];
    let loading = false;
    let waveDiv;
    let toplevelEntity = "";
    let selected;
    let testbenchName = "tb.vhdl";

    onMount(async () => {
        editor.on("change", onChangeContent);

        if (!$userStore)
            return;

        await setTabItems();
    });

    async function setTabItems() {
        if ($userStore.is_admin) {
            tabItems = await getFilesFromProject(params.id);
        } else {
            tabItems = await getSubmissonFiles(params.id);
        }
        if (tabItems.length > 0)
            editor.setValue(tabItems[currentTab].content);
    }

    async function onRunFiles(): Promise<void> {
        await onSaveFiles();
        loading = true;
        let response = await submitTest(tabItems, toplevelEntity);
        loading = false;

        message = response.status == "OK"
                ? "Código simulado com sucesso.\n"
                : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
    }

    async function onSaveFiles(): Promise<void> {
        loading = true;
        try {
            await saveFiles();
            message = "Arquivos salvos.\n";
        } catch {
            message = "Não foi possível salvar os arquivos.\n";
        } finally {
            loading = false;
        }
    }

    async function saveFiles() {
        return $userStore.is_admin
            ? await saveProjectFiles(tabItems, params.id)
            : await saveSubmissionFiles(tabItems, params.id);
    }

    async function removeFiles() {
        if (tabItems.length > 0) {
            let ids = tabItems.map(x => x.id);
            for (let id of ids) {
                if (id) {
                    $userStore.is_admin
                        ? await removeProjectFile(id)
                        : await removeSubmissionFile(id);
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
                $userStore.is_admin
                    ? await removeProjectFile(tabItems[currentTab].id)
                    : await removeSubmissionFile(tabItems[currentTab].id);
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
        await saveFiles();
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
    />

    <nav>
        <div class="controls">
            <select bind:value={selected}>
                <option value="wave.json">Gerar onda (wave.json)</option>
                <option value={testbenchName}>Testbench ({testbenchName})</option>
            </select>
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>
                    Download VCD
                </button>
                <button on:click={() => window.open("http://raczben.pythonanywhere.com/")}>Abrir visualizador de forma de onda</button>
            {/if}
            {#if !$userStore.is_admin}
                <button on:click={onReset}>Reset</button>
            {/if}
            <button on:click={onSaveFiles}>Salvar</button>
            <button on:click={onRunFiles}>Rodar</button>
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        <div class="message">
            <div
                id="WaveJSON_0"
                class={tabItems && currentTab && tabItems[currentTab] && tabItems[currentTab].filename === "wave.json"
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
    select {
        margin: 0 0.3rem 0 0;
        padding: 0.3rem;
    }

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
