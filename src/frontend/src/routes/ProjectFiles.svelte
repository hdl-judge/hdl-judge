<script>
    import Editor from "../components/Editor.svelte";
    import {getFilesFromProject, removeProjectFile, saveProjectFiles} from "../utils/api/api";

    export let params;
</script>

<Editor
    getFiles={getFilesFromProject}
    saveFiles={saveProjectFiles}
    deleteFiles={removeProjectFile}
    showReset={false}
    projectId={params.id}
/>