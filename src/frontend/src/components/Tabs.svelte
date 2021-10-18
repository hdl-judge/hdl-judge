<script lang="ts">
    import {createEventDispatcher} from "svelte";

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

<ul>
    <li>
        <img id="delete" on:click={() => dispatch('deleteTab')}  src="icons/x.svg" />
    </li>
    {#if Array.isArray(items)}
        {#each items as item, i}
            <li class={activeTabValue === i ? 'active' : ''}>
                <span class="tab" on:click={handleClick(i)} on:dblclick={handleDoubleClick(i)}>
                    {item.filename}
                </span>
            </li>
        {/each}
    {/if}
    <li>
        <img id="add" on:click={() => dispatch('addTab')} src="icons/plus.svg" />
    </li>
</ul>

<style>
    ul {
        display: flex;
        flex-wrap: nowrap;
        padding-left: 1px;
        margin: 11px 0 0 0;
        list-style: none;
        color: #dee2e6;
    }

    .tab {
        border: 1px solid transparent;
        border-top-left-radius: 0.25rem;
        border-top-right-radius: 0.25rem;
        border-bottom: none;
        display: block;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }

    .tab:hover {
        border-color: #8a8a8a;
    }

    #delete {
        padding: 0.5rem;
        cursor: pointer;
        filter: invert();
    }

    li.active > .tab {
        color: #dee2e6;
        background-color: #262626;
        border-color: #383d3f;
    }

    #add {
        padding: 0.5rem 0.2rem;
        cursor: pointer;
        filter: invert();
    }
</style>
