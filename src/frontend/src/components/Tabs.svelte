<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let items = [];
    export let activeTabValue = 0;

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
    <div class="nav-button" on:click={() => dispatch('deleteTab')}>
        <img alt="deletar" id="delete" src="icons/x.svg" />
    </div>
    {#each items as item, i}
        <div
            class={activeTabValue === i ? 'nav-button active' : 'nav-button'}
            on:click={handleClick(i)}
            on:dblclick={handleDoubleClick(i)}
        >
            {item}
        </div>
    {/each}
    <div class="nav-button" on:click={() => dispatch('addTab')}>
        <img alt="adicionar" id="add" src="icons/plus.svg" />
    </div>
</section>

<style>
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
