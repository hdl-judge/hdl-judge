<script lang="ts">
    import { onMount } from 'svelte';
    import Loading from '../components/Loading.svelte';
    import {link, pop} from 'svelte-spa-router';
    import {
        getAllProjectSubmissons,
        getUserSubmissionFiles,
        runAutocorrection,
        sendSubmissionsToMoss
    } from "../utils/api/submissions";
    import {arrowLeft} from "svelte-awesome/icons";
    import {Icon} from "svelte-awesome";
    import {createAndDownloadFile, getMossKey} from "../utils/utils";

    export let params: any = {};
    const resultKey = `result_${params.id}`;
    let students = [];
    let loading = true;
    let mossResultUrl: string
    let testbenchResult;

    onMount(async () => {
        await loadSubmissions();
        let cachedMossResult = localStorage.getItem(getMossKey(params.id));
        if (cachedMossResult)
            mossResultUrl = cachedMossResult;

        let storedResult = localStorage.getItem(resultKey);
        if (storedResult) {
            try {
                testbenchResult = await JSON.parse(storedResult);
            } catch {}
        }
    });

    async function loadSubmissions() {
        loading = true;
        students = await getAllProjectSubmissons(params.id);
        loading = false;
    }

    async function submitToMoss() {
        loading = true;
        let result = await sendSubmissionsToMoss(params.id);
        mossResultUrl = result[0];
        loading = false;
    }

    async function downloadFiles(projectId, userId) {
        let zip = await getUserSubmissionFiles(projectId, userId);
        createAndDownloadFile(zip, `submission_project_${projectId}_user_${userId}.zip`);
    }

    async function onRunAutocorrection() {
        let result = await runAutocorrection(params.id);
        localStorage.setItem(resultKey, JSON.stringify(result));
        testbenchResult = result;
    }

</script>

<section>
    {#if loading}
        <Loading/>
    {:else}
        <span on:click={pop} class="btn btn-icon"><Icon data={arrowLeft} /></span>
        <a href="/project_files/{params.id}" use:link class="btn">Editar arquivos padrão do projeto</a>
        <a href="/testbench/{params.id}" use:link class="btn">Editar testbench</a>
        <span on:click={onRunAutocorrection} class="btn">Rodar testbench</span>
        {#if mossResultUrl}
            <a href={mossResultUrl} class="btn" target="_blank" rel="noopener noreferrer">Ver resultados do Moss</a>
        {/if}
        <span class="btn" on:click={submitToMoss}>
            Enviar arquivos para detecção de plágio (Moss)
        </span>
        <br>
        {#if students.length > 0}
            <table>
                <tr>
                    <th>Nome do aluno</th>
                    <th>Quantidade de arquivos</th>
                    <th>Baixar arquivos</th>
                    {#if testbenchResult}
                        <th>Resultado da correção</th>
                    {/if}
                </tr>
                {#each students as student (student.id)}
                    <tr>
                        <td>{student.name}</td>
                        <td class="center">{student.count}</td>
                        <td class="center"><span on:click={() => downloadFiles(params.id, student.id)} class="download">Baixar</span></td>
                        {#if testbenchResult}
                            {#if testbenchResult[student.id]}
                                <td>{testbenchResult[student.id]}</td>
                            {:else}
                                <td></td>
                            {/if}
                        {/if}
                    </tr>
                {/each}
            </table>
        {/if}
    {/if}
</section>

<style>
    .btn {
        margin: 0.3rem;
        padding: 0.5rem;
        border-radius: 6px;
        color: white;
        background: #333;
        text-decoration: none;
    }

    .btn:hover {
        background: dimgray;
        cursor: pointer;
    }

    .btn-icon {
        display: inline-block;
        padding: 0.6rem 0.7rem 0.4rem 0.7rem;
    }

    section {
        padding: 1.3rem;
    }

    th, td {
        border: 1px solid silver;
        padding: 0.3rem;
    }

    .center {
        text-align: center;
    }

    table {
        border-collapse: collapse;
        margin-top: 1.4rem;
    }

    a {
        color: white;
        text-decoration: underline;
    }

    a:hover {
        text-decoration: none;
    }

    .download {
        color: white;
        text-decoration: underline;
    }

    .download:hover {
        text-decoration: none;
        cursor: pointer;
    }
</style>
