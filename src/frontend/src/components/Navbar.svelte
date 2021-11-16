<script lang="ts">
    import { link } from 'svelte-spa-router'
    import active from 'svelte-spa-router/active'

    export let items = [];
</script>

<nav>
    {#each items as item (item.name)}
        <a href={item.link} use:link use:active={{ className: 'active-navbar' }} class="nav-button">{item.name}</a>
    {/each}
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
    }

    .nav-button:hover {
        background: dimgray;
        cursor: pointer;
    }

    :global(.active-navbar) {
        background: dimgray;
    }
</style>