import json
from typing import List, Any, Union


def j_print(d: Union[dict, List]) -> None:
    print(json.dumps(d, indent=4))


def o_print(o: object) -> None:
    try:
        j_print(o.__dict__)
    except AttributeError:
        print(AttributeError)


def l_print(l :List[Any]) -> None:
    j_print([repr(el) for el in l])

