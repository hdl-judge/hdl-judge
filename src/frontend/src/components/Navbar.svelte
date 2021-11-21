<script lang="ts">
    import { link } from 'svelte-spa-router'
    import active from 'svelte-spa-router/active'

    export let isLoggedIn = false;
    export let isAdmin = false;
    export let username = "";

    let items = [
        { name: "Home", link: "/", showOnlyWhenLoggedIn: false, showOnlyForAdmin: false },
        { name: "Projetos", link: "/projects", showOnlyWhenLoggedIn: true, showOnlyForAdmin: false },
        { name: "Alunos", link: "/students", showOnlyWhenLoggedIn: true, showOnlyForAdmin: true },
        { name: "Submissões", link: "/submissions", showOnlyWhenLoggedIn: true, showOnlyForAdmin: true },
    ];
</script>

<nav>
    {#each items as item (item.name)}
        {#if item.showOnlyWhenLoggedIn}
            {#if isLoggedIn}
                {#if item.showOnlyForAdmin}
                    {#if isAdmin}
                        <a href={item.link}
                            use:link
                            use:active={{ className: 'active-navbar' }}
                            class="nav-button"
                        >
                            {item.name}
                        </a>
                    {/if}
                {:else}
                    <a href={item.link}
                       use:link
                       use:active={{ className: 'active-navbar' }}
                       class="nav-button"
                    >
                        {item.name}
                    </a>
                {/if}
            {/if}
        {:else}
            <a href={item.link}
               use:link
               use:active={{ className: 'active-navbar' }}
               class="nav-button"
            >
                {item.name}
            </a>
        {/if}
    {/each}
    {#if isLoggedIn && username}
        <div class="last-child">
            {username}
        </div>
    {:else}
        <a href="/login" use:link use:active={{ className: 'active-navbar' }}
           class="nav-button last-child">Login</a>
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