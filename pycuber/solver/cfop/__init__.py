import sys, time, pycuber
if sys.version_info > (3,4):
    import io as generalized_io
else:
    import cStringIO as generalized_io

from .cross import CrossSolver
from .f2l import F2LSolver
from .oll import OLLSolver
from .pll import PLLSolver


class CFOPSolver(object):
    def __init__(self, cube=None):
        self.cube = cube

    def feed(self, cube):
        self.cube = cube

    def solve(self, suppress_progress_messages=False):
        if suppress_progress_messages:
            save_stdout = sys.stdout
            sys.stdout = generalized_io.StringIO()
        if not self.cube.is_valid():
            raise ValueError("Invalid Cube.")
        result = pycuber.Formula()
        sys.stdout.write("Solver starts....")
        sys.stdout.write("\rSolving Cross ......")
        solver = CrossSolver(self.cube)
        cross = solver.solve()
        result += cross
        sys.stdout.write("\rCross: {0}\n".format(cross))

        solver = F2LSolver(self.cube)
        f2lall = solver.solve()
        for i, f2l in enumerate(f2lall):
            sys.stdout.write("\rSolving F2L#{0} ......".format(i))
            result += f2l[1]
            sys.stdout.write("\rF2L{0}: {1}\n".format(*f2l))
        
        solver = OLLSolver(self.cube)
        sys.stdout.write("\rSolving OLL ......")
        oll = solver.solve()
        result += oll
        sys.stdout.write("\rOLL:  {0}\n".format(oll))
        solver = PLLSolver(self.cube)
        sys.stdout.write("\rSolving PLL ......")
        pll = solver.solve()
        result += pll
        sys.stdout.write("\rPLL:  {0}\n".format(pll))
        sys.stdout.write("\nFULL: {0}\n".format(result.optimise()))
        if suppress_progress_messages:
            sys.stdout = save_stdout
        return result

