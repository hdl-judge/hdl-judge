<script lang="ts">
    import { getAllProjects, createProject, removeProject } from '../utils/api/api';
    import { onMount } from 'svelte';
    import Loading from '../components/Loading.svelte';
    import { link } from 'svelte-spa-router'
    import {userStore} from "../utils/store";

    let projects = [];
    let loading = true;

    async function loadProjects() {
        loading = true;
        projects = await getAllProjects();
        loading = false;
    }

    onMount(loadProjects);

    async function onClickAddProject() {
        let name = prompt("Digite o nome do exercício");
        loading = true;
        await createProject(name);
        await loadProjects();
        loading = false;
    }

    async function onClickRemoveProject(id) {
        loading = true;
        await removeProject(id);
        await loadProjects();
        loading = false;
    }
</script>

<section>
    {#if loading}
        <Loading/>
    {:else}
        <table>
            <tr>
                <th>Nome do projeto</th>
                {#if $userStore && $userStore.is_admin}
                    <th class="clickable" on:click={onClickAddProject}><img alt="adicionar" class="icon" src="icons/plus.svg" /></th>
                {/if}
            </tr>
            {#each projects as project (project.id)}
                <tr>
                    {#if $userStore && $userStore.is_admin}
                        <td><a href="/submissions/{project.id}" use:link class="nav-button">{project.name}</a></td>
                    {:else}
                        <td><a href="/projects/{project.id}" use:link class="nav-button">{project.name}</a></td>
                    {/if}
                    {#if $userStore && $userStore.is_admin}
                        <td class="clickable" on:click={() => onClickRemoveProject(project.id)}><img alt="remover" class="icon" src="icons/x.svg" /></td>
                    {/if}
                </tr>
            {/each}
        </table>
    {/if}
</section>

<style>
    section {
        padding: 1.3rem;
    }

    th, td {
        border: 1px solid silver;
        padding: 0.3rem;
    }

    table {
        border-collapse: collapse
    }

    .icon {
        filter: invert();
    }

    .clickable:hover {
        background: silver;
        cursor: pointer;
    }

    a {
        color: white;
    }
</style>
