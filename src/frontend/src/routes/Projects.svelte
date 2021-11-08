<script lang="ts">
    import { getAllExercises, createExercise, removeExercise } from '../utils/api';
    import { onMount } from 'svelte';
    import Loading from '../components/Loading.svelte';
    import { link } from 'svelte-spa-router'

    let exercises = [];
    let loading = true;

    async function loadExercises() {
        loading = true;
        exercises = await getAllExercises();
        loading = false;
    }

    onMount(loadExercises);

    async function onClickAddExercise() {
        let name = prompt("Digite o nome do exercício");
        loading = true;
        await createExercise(name);
        await loadExercises();
        loading = false;
    }

    async function onClickRemoveExercise(id) {
        loading = true;
        await removeExercise(id);
        await loadExercises();
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
                <th class="clickable" on:click={onClickAddExercise}><img alt="adicionar" class="icon" src="icons/plus.svg" /></th>
            </tr>
            {#each exercises as exercise (exercise.id)}
                <tr>
                    <td><a href="/projects/{exercise.id}" use:link class="nav-button">{exercise.name}</a></td>
                    <td class="clickable" on:click={() => onClickRemoveExercise(exercise.id)}><img alt="remover" class="icon" src="icons/x.svg" /></td>
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
