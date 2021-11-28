<script lang="ts">
    import { onMount } from 'svelte';
    import Loading from '../components/Loading.svelte';
    import {link, pop} from 'svelte-spa-router';
    import {getAllProjectSubmissons, sendSubmissionsToMoss} from "../utils/api/submissions";
    import {arrowLeft} from "svelte-awesome/icons";
    import {Icon} from "svelte-awesome";
    import {getMossKey} from "../utils/utils";

    export let params: any = {};
    let students = [];
    let loading = true;
    let mossResultUrl: string;

    onMount(async () => {
        await loadSubmissions();
        let cachedMossResult = localStorage.getItem(getMossKey(params.id));
        if (cachedMossResult)
            mossResultUrl = cachedMossResult;
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

</script>

<section>
    {#if loading}
        <Loading/>
    {:else}
        <span on:click={pop} class="btn btn-icon"><Icon data={arrowLeft} /></span>
        <a href="/project_files/{params.id}" use:link class="btn">Editar arquivos padrão do projeto</a>
        <a href="/testbench/{params.id}" use:link class="btn">Editar testbench</a>
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
                </tr>
                {#each students as student (student.id)}
                    <tr>
                        <td>{student.name}</td>
                        <td class="center">{student.count}</td>
                        <td class="center"><a href="/" use:link>Baixar</a></td>
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
</style>
