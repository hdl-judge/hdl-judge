<script>
    import Editor from "../components/Editor.svelte";
    import {getSubmissonFiles, removeSubmissionFile, saveSubmissionFiles} from "../utils/api/submissions";

    export let params;
</script>

<Editor
    getFiles={getSubmissonFiles}
    saveFiles={saveSubmissionFiles}
    deleteFiles={removeSubmissionFile}
    showReset={true}
    projectId={params.id}
/>