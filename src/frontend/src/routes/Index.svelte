<script lang="ts">
    import Router from 'svelte-spa-router'
    import { link } from 'svelte-spa-router'
    import active from 'svelte-spa-router/active'
	import Home from './Home.svelte';
	import Projects from './Projects.svelte';
	import Exercise from './Exercise.svelte';

    const routes = {
        '/': Home,
        '/projects/:id': Exercise,
        '/projects': Projects,
        '*': Home,
    }

    export let url = "";
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>

    <nav>
        <a href="/" use:link use:active class="nav-button">Home</a>
        <a href="/projects" use:link use:active class="nav-button">Projetos</a>
        <div class="nav-button">Alunos</div>
        <div class="nav-button">Submissões</div>
    </nav>

    <section class="content">
        <Router {routes}/>
    </section>
</main>

<style>
    main {
        height: 100%;
        width: 100%;
        display: grid;
        grid-template: 5em 3em auto / 1fr;
        grid-template-areas:
                "h"
                "n"
                "c";
    }

    header {
        background: #262626;
        grid-area: h;
    }

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

    :global(.active) {
        background: dimgray;
    }

    .content {
        background: #262626;
        grid-area: c;
        color: white;
        white-space: pre-line;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        margin: auto 10px;
    }
</style>
