<script>
</script>

<img alt="carregando" class="icon" src="icons/loader.svg" />

<style>
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .icon {
        filter: invert();
        animation: spin 4s linear infinite;
    }
</style>