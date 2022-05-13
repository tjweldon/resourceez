from __future__ import annotations

from typing import List, Optional

from unittest import TestCase

rest_utils import ApiObject, Primitive


class FlatResource(ApiObject):
    primitive_property: Primitive
    nullable_property: Optional[Primitive]

    @classmethod
    def create(cls, primitive) -> dict:
        return {
            "primitive_property": primitive,
            "nullable_property": None,
        }

    @classmethod
    def create_collection(cls) -> List[dict]:
        return [FlatResource.create(primitive) for primitive in ("foo", 1, 0.1, True)]


class NestedResource(ApiObject):
    sub_resources = {
        "nested": FlatResource.parse,
    }

    nested: FlatResource

    @classmethod
    def create(cls, primitive="foo") -> dict:
        return {"nested": FlatResource.create(primitive)}


class NestedResourceCollection(ApiObject):
    sub_resources = {
        "nested_collection": FlatResource.parse_collection,
    }

    nested_collection: List[FlatResource]

    @classmethod
    def create(cls) -> dict:
        return {"nested_collection": FlatResource.create_collection()}


class TestApiObject(TestCase):
    def test_parsed_resource_fields_are_available_via_object_access(self):
        for raw_resource in FlatResource.create_collection():
            parsed = FlatResource.parse(raw_resource)

            primitive_type = type(raw_resource["primitive_property"])
            with self.subTest(
                msg="resource is correctly parsed when the primitive property is "
                + repr(primitive_type)
            ):
                self.assertEqual(
                    raw_resource["primitive_property"], parsed.primitive_property
                )

    def test_subresource_is_constructed_with_subresource_constructor(self):
        raw = NestedResource.create()

        parsed = NestedResource.parse(raw)

        self.assertIsInstance(parsed.nested, FlatResource)

    def test_subresource_collection_is_constructed_with_subresource_constructor(self):
        raw = NestedResourceCollection.create()

        parsed = NestedResourceCollection.parse(raw)

        self.assertIsInstance(parsed.nested_collection, list)
        distinct_types = {type(element) for element in parsed.nested_collection}
        self.assertSetEqual({FlatResource}, distinct_types)

    def test_raw_returns_json_serializable_dict_equivalent_to_parsed_input(self):
        raw = NestedResourceCollection.create()
        parsed = NestedResourceCollection.parse(raw)

        self.assertDictEqual(raw, parsed.raw)
