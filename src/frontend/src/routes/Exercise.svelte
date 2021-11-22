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

    onMount(async () => {
        editor.on("change", onChangeContent);

        if (!$userStore)
            return;

        if ($userStore.is_admin) {
            tabItems = await getFilesFromProject(params.id);
        } else {
            tabItems = await getSubmissonFiles(params.id, $userStore.id);
            if (!tabItems.length > 0)
                tabItems = await getFilesFromProject(params.id);
        }
        if (tabItems.length > 0)
            editor.setValue(tabItems[currentTab].content);
    });

    async function onRunFiles(): Promise<void> {
        await onSaveFiles();
        loading = true;
        let response = await submitTest(tabItems);
        loading = false;

        message = response.status == "OK"
                ? "Código simulado com sucesso.\n"
                : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
    }

    async function onSaveFiles(): Promise<void> {
        loading = true;
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
        let response = $userStore.is_admin
            ? await saveProjectFiles(tabItems, params.id)
            : await saveSubmissionFiles(tabItems, params.id);
        loading = false;
        message = "Arquivos salvos.\n";
    }

    function onChangeContent() {
        tabItems[currentTab].content = editor.getValue();
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
            currentTab = newTabIndex;
            editor.setValue(tabItems[newTabIndex].content);
            tabItems = tabItems;
        }
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
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>
                    Download VCD
                </button>
            {/if}
            <button on:click={onSaveFiles}>Salvar</button>
            <button on:click={onRunFiles}>Rodar</button>
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        {#if loading}
            <Loading />
        {:else}
            {message}
        {/if}
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
