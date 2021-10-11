<script lang="ts">
    import {submitTest, File} from "../utils/api";
    import {createAndDownloadFile} from "../utils/utils";
    import {ResponseStatus} from "../utils/response_status";
    import Tabs from "../components/Tabs.svelte";
    import TextEditor from "../components/TextEditor.svelte";
    import CodeMirror from "codemirror";
    import {onMount} from "svelte";

    let editor: CodeMirror.EditorFromTextArea;
    let message: string = "";
    let vcd: string;
    let tabItems: File[] = [
        {filename: "intrucoes.txt", content: "Implemente um somador com a interface apresentada"},
        {filename: "adder.vhdl", content: `entity adder is
	port(
		i0, i1 : in bit;
		ci : in bit;
		s : out bit;
		co : out bit
	);
end adder;`},
        {filename: "adder_tb.vhdl", content: `--  A testbench has no ports.
entity adder_tb is
end adder_tb;

architecture behav of adder_tb is
  --  Declaration of the component that will be instantiated.
  component adder
    port (i0, i1 : in bit; ci : in bit; s : out bit; co : out bit);
  end component;

  --  Specifies which entity is bound with the component.
  for adder_0: adder use entity work.adder;
  signal i0, i1, ci, s, co : bit;
begin
  --  Component instantiation.
  adder_0: adder port map (i0 => i0, i1 => i1, ci => ci, s => s, co => co);

  --  This process does the real job.
  process
    type pattern_type is record
      --  The inputs of the adder.
      i0, i1, ci : bit;
      --  The expected outputs of the adder.
      s, co : bit;
    end record;
    --  The patterns to apply.
    type pattern_array is array (natural range <>) of pattern_type;
    constant patterns : pattern_array :=
      (('0', '0', '0', '0', '0'),
       ('0', '0', '1', '1', '0'),
       ('0', '1', '0', '1', '0'),
       ('0', '1', '1', '0', '1'),
       ('1', '0', '0', '1', '0'),
       ('1', '0', '1', '0', '1'),
       ('1', '1', '0', '0', '1'),
       ('1', '1', '1', '1', '1'));
  begin
    --  Check each pattern.
    for i in patterns'range loop
      --  Set the inputs.
      i0 <= patterns(i).i0;
      i1 <= patterns(i).i1;
      ci <= patterns(i).ci;
      --  Wait for the results.
      wait for 1 ns;
      --  Check the outputs.
      assert s = patterns(i).s
        report "bad sum value" severity error;
      assert co = patterns(i).co
        report "bad carry out value" severity error;
    end loop;
    assert false report "end of test" severity note;
    --  Wait forever; this will finish the simulation.
    wait;
  end process;

end behav;`}
    ];
    let currentTab: number = 0;

    async function onSubmit(): Promise<void> {
        tabItems[currentTab].content = editor.getValue();

        let response = await submitTest(tabItems);

        message = response.status == ResponseStatus.OK
                ? "Código simulado com sucesso.\n"
                : "Erro ao compilar ou simular o código:\n";
        message += response.message;
        vcd = response.result;
    }

    function onChangeTab(event) {
        tabItems[currentTab].content = editor.getValue();
        editor.setValue(tabItems[event.detail].content);
        currentTab = event.detail;
    }

    onMount(() => {
        editor.setValue(tabItems[currentTab].content);
    });
</script>

<main>
    <header>
        <h1>HDL Judge</h1>
    </header>

    <section class="tabs">
        <Tabs activeTabValue={currentTab} items={tabItems} on:changeTab={onChangeTab}/>
    </section>

    <nav>
        <div class="controls">
            {#if vcd}
                <button on:click={() => createAndDownloadFile(vcd, "result", "vcd")}>Download VCD</button>
            {/if}
            <button on:click={onSubmit}>Enviar</button>
        </div>
    </nav>

    <section class="editor">
        <TextEditor bind:editor={editor}/>
    </section>

    <aside class="results">
        {message}
    </aside>
</main>

<style>
    main {
        height: 100%;
        width: 100%;
        display: grid;
        grid-template: 5em 3em auto / 1fr 1fr;
        grid-template-areas:
                "h h"
                "t n"
                "e r";
    }

    header {
        background: #262626;
        grid-area: h;
    }

    nav {
        background: #333;
        grid-area: n;
        display: flex;
        justify-content: flex-end;
    }

    .tabs {
        background: #333;
        grid-area: t;
    }

    .editor {
        grid-area: e;
        overflow-y: auto;
        font-size: 1.3em;
    }

    .results {
        background: #262626;
        grid-area: r;
        border-left: 3px solid #333;
        padding: 1.3em;
        color: antiquewhite;
        white-space: pre-line;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
        margin: auto 10px;
    }

    button {
        margin: 0.5em 1em;
    }
</style>
