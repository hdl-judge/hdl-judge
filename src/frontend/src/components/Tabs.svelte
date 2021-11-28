<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import {pop} from "svelte-spa-router";
    import {Icon} from "svelte-awesome";
    import {arrowLeft} from "svelte-awesome/icons";

    export let items = [];
    export let activeTabValue = 0;
    export let showDelete: boolean = true;
    export let showAdd: boolean = true;

    const dispatch = createEventDispatcher();

    function handleClick(tabValue) {
        return () => {
            dispatch('changeTab', tabValue);
        };
    }

    function handleDoubleClick(tabValue) {
        return () => {
            dispatch('renameTab', tabValue);
        };
    }
</script>

<section class="tabs">
    <span on:click={pop} class="btn btn-icon"><Icon data={arrowLeft} /></span>

    {#if showDelete}
        <div class="nav-button" on:click={() => dispatch('deleteTab')}>
            <img alt="deletar" id="delete" src="icons/x.svg" />
        </div>
    {/if}
    {#each items as item, i}
        <div
            class={activeTabValue === i ? 'nav-button active' : 'nav-button'}
            on:click={handleClick(i)}
            on:dblclick={handleDoubleClick(i)}
        >
            {item.filename}
        </div>
    {/each}
    {#if showAdd}
        <div class="nav-button" on:click={() => dispatch('addTab')}>
            <img alt="adicionar" id="add" src="icons/plus.svg" />
        </div>
    {/if}
</section>

<style>
    .btn {
        margin: 0.3rem;
        padding: 0.5rem;
        border-radius: 6px;
        color: white;
        background: #444;
        text-decoration: none;
    }

    .btn:hover {
        background: dimgray;
        cursor: pointer;
    }

    .btn-icon {
        display: inline-block;
        padding: 0.3rem 0.5rem 0.3rem 0.5rem;
    }

    .tabs {
        background: #333;
        display: flex;
        grid-area: t;
        color: white;
    }

    .nav-button {
        margin: 0 0.3rem 0 0.3rem;
        padding: 0.5rem;
        border-radius: 6px 6px 0 0;
        color: white;
    }

    .nav-button:hover {
        background: dimgray;
        cursor: pointer;
    }

    .active {
        background: #262626;
    }

    #delete {
        filter: invert();
    }

    #add {
        filter: invert();
    }
</style>
