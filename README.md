# ResourceEZ

ResourceEZ (reource easy) was born of my frustration with `attrs` and
`dataclasses` both being a bit too clever for serialising/deserialising
rest resources as a client. Often the implementation of a rest client is
a crystalisation of the author(s) understanding of parts of the interface
that they choose to imlement their use cases.

If the upstream API is complex or deeply nested, this kind of code can be an
absolute nigtmare of nested dict/list access, with code like:

```python
resp = requests.get(url)
resource = resp.json()

# idk why this doesn't work sometimes, gah!
useful_thing = resource["content"]["data"]["body"]["info"][0]["metadata"]["something_useful"]
```

cropping up in your project.

What if you could express your client in terms of _the abstractions than you
care about_?

While `attrs`/`dataclasses` can do this, it's clunky and syntactically noisy.

From the `attrs` [pypi project page](https://pypi.org/project/attrs/):

```python
from attrs import define, Factory

@define
class SomeClass:
    a_number: int = 42
    list_of_numbers: list[int] = Factory(list)

```

which is fine, until you try to express deeply nested object graphs like you might
encounter while trying to consume an upstream API. An example of where this gets
messy is if the `list_of_numbers` sub-resource is a list containing elements that
are another sub-resource object.

This isn't to say there's anything wrong with `attrs`; the nature of a swiss army
knife is that it's not a very good knife, though it's very useful to have around.
By the same token `attrs` and `dataclasses` are very useful, they just aren't designed
specifically around parsing rest resources.

So how could it be improved if rest resources is what we're working with? ResourceEZ
aims to let you express only the parts of a resource you care about, with as little
boilerplate as possible:

```python
from __future__ import annotations # Even compatible with this!

from typing import List
from resourceez import from_annotatations, ApiObject


class SubResource(ApiObject):
    id: int
    name: str


@from_annotatations
class Resource(ApiObject):
    a_number: int
    subresource_list: List[SubResource]


raw = {
    "a_number": 42,
    "subresource_list": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ],
    "something_else": {
        "foo": "bar",
        "I": [
            "don't",
            "care",
            "about",
            "this",
            "stuff",
        ],
    },
}

ez = Resource(**raw)

# We care about these parts of the resource
assert isinstance(ez, Resource)
assert isinstance(ez.subresource_list[0], SubResource)
assert {sub.name for sub in ez.subresource_list} == {"Alice", "Bob"}
assert ez.raw() == raw

# We didn't tell resourceez how to parse this.
assert isinstance(ez.something_else, dict)
```

That's it. You don't even need to express the whole object graph!
Your IDE will have accurate type inference where you care about it, and most
importantly it's only the info that you, as somebody developing a client to
an api, need and almost nothing else.
