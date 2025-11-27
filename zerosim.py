import cirq
import numpy as np
import re

class AlwaysZeroSimulator(cirq.Simulator):
    def run(self, program, *args, **kwargs):

        res = super().run(program, *args, **kwargs)


        zeroed = {}
        pattern = re.compile(r"^ZeroKey\d+$")
        for k, v in res.measurements.items():
            if pattern.match(k):
                zeroed[k] = np.zeros_like(v)
            else:
                zeroed[k] = v

          
        return cirq.ResultDict(params=res.params,
                               measurements=zeroed)