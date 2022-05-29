import scratch
from util.debug_utils import o_print, j_print

b = scratch.Business.default()

print("="*10)
print(f"OPrint: of {b}")
print("="*10)
print(scratch.Business.sub_resources)
j_print(scratch.Business.parse(b.raw).raw)


