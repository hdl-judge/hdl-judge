<script lang="ts">
    import {link, push} from 'svelte-spa-router'
    import active from 'svelte-spa-router/active'
    import { userStore } from '../utils/store'

    function logout() {
        localStorage.removeItem("access_token");
        $userStore = null;
        push("/");
    }
</script>

<nav>
    <a href="/" use:link use:active={{ className: 'active-navbar' }} class="nav-button">Home</a>

    {#if $userStore}
        <a href="/projects" use:link use:active={{ className: 'active-navbar' }} class="nav-button">Projetos</a>
    {/if}

    {#if $userStore && $userStore.is_admin}
        <a href="/users" use:link use:active={{ className: 'active-navbar' }} class="nav-button">Usuários</a>
    {/if}

    {#if $userStore}
        <div class="last-child">{$userStore.name}</div>
        <div class="nav-button" on:click={logout}>Logout</div>
    {:else}
        <a href="/login" use:link use:active={{ className: 'active-navbar' }} class="nav-button last-child">Login</a>
    {/if}
</nav>

<style>
    nav {
        background: #333;
        grid-area: n;
        display: flex;
        color: white;
    }

    .nav-button {
        margin: 0.3rem;
        padding: 0.5rem;
        border-radius: 6px;
        color: white;
        text-decoration: none;
    }

    .nav-button:hover {
        background: dimgray;
        cursor: pointer;
    }

    .last-child {
        margin: 0.3rem 0.3rem 0.3rem auto;
        padding: 0.5rem;
        border-radius: 6px;
        color: white;
    }

    :global(.active-navbar) {
        background: dimgray;
    }
</style>