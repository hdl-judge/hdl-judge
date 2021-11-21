<script>
    import {getUserData, login} from "../utils/api";
    import Loading from "../components/Loading.svelte";
    import { push } from "svelte-spa-router";
    import { userStore } from "../utils/store";

    let email = "";
    let password = "";
    let loading = false;

    async function onSubmit() {
        if (!email) {
            alert("É necessário preencher o email");
            return;
        }
        if (!password) {
            alert("É necessário preencher a senha");
            return;
        }
        loading = true;
        let response = await login(email, password);
        localStorage.setItem("access_token", response.access_token);
        $userStore = await getUserData();
        loading = false;
        await push("/");
    }
</script>

<section>
    {#if loading}
        <Loading />
    {:else}
        <form>
            <fieldset>
                <legend>Login</legend>
                <label for="email-form">Email</label>
                <input type="email" id="email-form" name="email-form" bind:value={email}><br>
                <label for="password-form">Senha</label>
                <input type="password" id="password-form" name="password-form" bind:value={password}><br>
                <input type="submit" value="Entrar" on:click|preventDefault={onSubmit}><br>
            </fieldset>
        </form>
    {/if}
</section>

<style>
    section {
        padding: 1.3rem;
        display: flex;
        justify-content: center;
    }
</style>