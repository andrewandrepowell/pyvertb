library ieee;
  use ieee.std_logic_1164.all;

entity fifo_top is
end entity fifo_top;

architecture behav of fifo_top is

  signal clk       : std_ulogic;
  signal rst       : std_ulogic;
  signal data_in   : std_ulogic_vector(31 downto 0);
  signal valid_in  : std_ulogic;
  signal ready_out : std_ulogic;
  signal data_out  : std_ulogic_vector(31 downto 0);
  signal valid_out : std_ulogic;
  signal ready_in  : std_ulogic;

  component fifo is
    generic (
      min_depth : natural
    );
    port (
      clk       : in    std_ulogic;
      rst       : in    std_ulogic;
      data_in   : in    std_ulogic_vector;
      valid_in  : in    std_ulogic;
      ready_out : out   std_ulogic;
      data_out  : out   std_ulogic_vector;
      valid_out : out   std_ulogic;
      ready_in  : in    std_ulogic
    );
  end component fifo;

begin

  fifo_inst : component fifo
    generic map (
      min_depth => 8
    )
    port map (
      clk       => clk,
      rst       => rst,
      data_in   => data_in,
      valid_in  => valid_in,
      ready_out => ready_out,
      data_out  => data_out,
      valid_out => valid_out,
      ready_in  => ready_in
    );

end architecture behav;
