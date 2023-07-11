import typing


# @lc-entity
# @lc-identifier :Component
class Component:
    # @lc-property
    # @lc-name label
    # @lc-type str
    label: str

    # @lc-property
    # @lc-name position
    position: typing.Tuple(int, int)
