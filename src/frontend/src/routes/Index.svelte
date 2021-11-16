<script lang="ts">
    import Router from 'svelte-spa-router'
	import Home from './Home.svelte';
	import Projects from './Projects.svelte';
	import Exercise from './Exercise.svelte';
	import Navbar from '../components/Navbar.svelte';

    const routes = {
        '/': Home,
        '/projects': Projects,
        '/projects/:id': Exercise,
        '*': Home,
    }

    export let url = "";
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>

    <Navbar items={[
        { name: "Home", link: "/" },
        { name: "Projetos", link: "/projects" },
        { name: "Alunos", link: "/students" },
        { name: "Submissões", link: "/submissions" },
    ]} />

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
