<script>
    import Editor from "../components/Editor.svelte";

    export let params;
    let getInitialFiles = () => [
        { filename: "instrucoes.txt", content: "Implemente um somador com carry in e carry out"},
        { filename: "adder.vhdl", content: `entity adder is
  -- \`i0\`, \`i1\`, and the carry-in \`ci\` are inputs of the adder.
  -- \`s\` is the sum output, \`co\` is the carry-out.
  port (i0, i1 : in bit; ci : in bit; s : out bit; co : out bit);
end adder;

architecture rtl of adder is
begin
  --  This full-adder architecture contains two concurrent assignments.
  --  Compute the sum.
  s <= i0 xor i1 xor ci;
  --  Compute the carry.
  co <= (i0 and i1) or (i0 and ci) or (i1 and ci);
end rtl;` },
        { filename: "adder_tb.vhdl", content: `--  A testbench has no ports.
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

end behav;
` },
        { filename: "wave.json", content: `{
    "clk_period": 10,
    "toplevel": "adder",
    "signal": [
        {"dir": "in", "name": "i0", "type": "bit", "wave": "0...1..."},
        {"dir": "in", "name": "i1", "type": "bit", "wave": "0.1.0.1."},
        {"dir": "in", "name": "ci", "type": "bit", "wave": "01010101"},
        {"dir": "out", "name": "s", "type": "bit", "wave": "01.010.1"},
        {"dir": "out", "name": "co", "type": "bit", "wave": "0..101.."}
    ]
}` },
];

</script>

<Editor
    getFiles={getInitialFiles}
    saveFiles={() => {}}
    deleteFiles={() => {}}
    onlyRunCode={true}
    returnButton={false}
    showSave={false}
/>

<style>
    section {
        padding: 1.3rem;
    }
</style>