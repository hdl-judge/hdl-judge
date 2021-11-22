<script lang="ts">
    import {getAllUsers, removeUser} from '../../utils/api/users';
    import { onMount } from 'svelte';
    import Loading from '../../components/Loading.svelte';
    import {link, push} from 'svelte-spa-router'

    let users = [];
    let loading = true;

    async function loadUsers() {
        loading = true;
        users = await getAllUsers();
        loading = false;
    }

    onMount(loadUsers);

    async function onClickAddExercise() {
        await push('/users/new');
    }

    async function onRemoveUser(id) {
        loading = true;
        await removeUser(id);
        await loadUsers();
        loading = false;
    }
</script>

<section>
    {#if loading}
        <Loading/>
    {:else}
        <table>
            <tr>
                <th>Id</th>
                <th>Nome</th>
                <th>Email</th>
                <th>Id Acadêmico</th>
                <th>Admin</th>
                <th class="clickable center" on:click={onClickAddExercise}><img alt="adicionar" class="icon" src="icons/plus.svg" /></th>
            </tr>
            {#each users as user (user.id)}
                <tr>
                    <td><a href="/projects/{user.id}" use:link class="nav-button">{user.id}</a></td>
                    <td>{user.name}</td>
                    <td>{user.email_address}</td>
                    <td>{user.academic_id}</td>
                    <td class="center">
                        {#if user.is_admin}
                            <img alt="é admin" class="icon" src="icons/check.svg" />
                        {:else}
                            <img alt="não é admin" class="icon" src="icons/x.svg"/>
                        {/if}
                    </td>
                    <td class="clickable center" on:click={() => onRemoveUser(user.id)}><img alt="remover" class="icon" src="icons/x.svg" /></td>
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

    .center {
        text-align: center;
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
