<script>
    import {addUser} from "../../utils/api/users";
    import {push} from "svelte-spa-router";
    import Loading from "../../components/Loading.svelte";

    let name = "";
    let email = "";
    let academic_id = "";
    let is_admin = false;
    let loading = false;

    async function handleSubmit() {
        loading = true;
        await addUser(name, email, academic_id, is_admin);
        loading = false;
        await push('/users');
    }
</script>
<section>
    {#if loading}
        <Loading/>
    {:else}
        <form on:submit|preventDefault={handleSubmit}>
            <label for="name">Nome</label>
            <input type="text" id="name" bind:value={name}>
            <label for="email">Email</label>
            <input type="email" id="email" bind:value={email}>
            <label for="academic_id">Id Acadêmico</label>
            <input type="text" id="academic_id" bind:value={academic_id}>
            <label for="is_admin">Admin</label>
            <input type="checkbox" id="is_admin" bind:value={is_admin}><br><br>
            <input type="submit" value="Adicionar usuário">
        </form>
    {/if}
</section>

<style>
    section {
        padding: 1.3rem;
    }
</style>