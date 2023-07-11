# @lc-entity
# @lc-identifier :Component
# @lc-name PartialComponent
class PartialComponent:
    # @lc-property
    # @lc-name label
    label: str


# @lc-entity
# @lc-identifier :Person
class Person:
    # @lc-property
    # @lc-name name
    name: str
    # @lc-property
    # @lc-name component
    # @lc-type :Component
    component: PartialComponent
