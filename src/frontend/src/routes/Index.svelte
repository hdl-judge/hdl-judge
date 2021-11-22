<script lang="ts">
    import Router from 'svelte-spa-router'
	import Home from './Home.svelte';
	import Projects from './Projects.svelte';
	import Exercise from './Exercise.svelte';
	import Navbar from '../components/Navbar.svelte';
    import Login from "./Login.svelte";
    import { onMount } from "svelte";
    import { getUserData } from "../utils/api/api";
    import { userStore } from "../utils/store";
    import Users from "./users/Users.svelte";
    import UserForm from "./users/UserForm.svelte";

    const routes = {
        '/': Home,
        '/projects': Projects,
        '/projects/:id': Exercise,
        '/login': Login,
        '/users': Users,
        '/users/new': UserForm,
        '*': Home,
    }

    onMount(async () => {
        let accessToken = localStorage.getItem("access_token");
        if (accessToken) {
            let user = await getUserData();
            if (user && user.name) {
                $userStore = user
            }
        }
    })
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>

    <Navbar />

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
