<script>
    import Editor from "../components/Editor.svelte";
    import {getTestbenchFiles, removeTestbenchFile, saveTestbenchFiles} from "../utils/api/testbench_files";

    export let params;
</script>

<Editor
    getFiles={getTestbenchFiles}
    saveFiles={saveTestbenchFiles}
    deleteFiles={removeTestbenchFile}
    showReset={false}
    showAdd={false}
    showDelete={false}
    showRun={false}
    allowRename={false}
    projectId={params.id}
/>