package util is

  function clog2 (n : natural) return natural;

end package util;

package body util is

  function clog2 (n: natural) return natural is
    variable i    : natural;
    variable test : natural;
  begin
    test := 1;
    i := 0;
    while (test < n) loop
      i := i + 1;
      test := test * 2;
    end loop;
    return i;
  end function clog2;

end package body util;
