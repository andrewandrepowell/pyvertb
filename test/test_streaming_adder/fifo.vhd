library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity fifo is
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
end entity fifo;

architecture rtl of fifo is

  constant ptr_size : natural := work.util.clog2(min_depth);
  constant depth    : natural := 2 ** ptr_size;
  signal   rd_ptr   : unsigned(ptr_size downto 0);
  signal   wr_ptr   : unsigned(ptr_size downto 0);

  type ram_type is array(0 to depth - 1) of std_ulogic_vector(data_in'length - 1 downto 0);

  signal ram : ram_type;

begin

  fifo_proc : process (clk) is

    variable next_wr_ptr : wr_ptr'subtype;
    variable next_rd_ptr : rd_ptr'subtype;

  begin

    if (clk'event and clk = '1') then
      if (rst /= '0') then
        rd_ptr    <= (others => '0');
        wr_ptr    <= (others => '0');
        ready_out <= '0';
        valid_out <= '0';
      else
        next_wr_ptr := wr_ptr;
        next_rd_ptr := rd_ptr;
        if ((valid_in='1') and (ready_out='1')) then
          ram(to_integer(wr_ptr(wr_ptr'left - 1 downto 0))) <= data_in;
          next_wr_ptr := wr_ptr + 1;
        end if;
        if ((valid_out='1') and (ready_in='1')) then
          next_rd_ptr := rd_ptr + 1;
        end if;
        ready_out <= '0' when
                     (next_wr_ptr(next_wr_ptr'left) /= next_rd_ptr(next_rd_ptr'left)) and
                     (next_wr_ptr(next_wr_ptr'left - 1 downto 0) = next_rd_ptr(next_rd_ptr'left - 1 downto 0)) else
                     '1';
        valid_out <= '0' when
                     (next_wr_ptr(next_wr_ptr'left) = next_rd_ptr(next_rd_ptr'left)) and
                     (next_wr_ptr(next_wr_ptr'left - 1 downto 0) = next_rd_ptr(next_rd_ptr'left - 1 downto 0)) else
                     '1';
        wr_ptr   <= next_wr_ptr;
        rd_ptr   <= next_rd_ptr;
        data_out <= ram(to_integer(next_rd_ptr(next_rd_ptr'left - 1 downto 0)));
      end if;
    end if;

  end process fifo_proc;

end architecture rtl;
