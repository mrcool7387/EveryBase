import inspect
from collections.abc import Callable


def internal(func: Callable) -> Callable:
    func.is_internal = True  # pyright: ignore[reportFunctionMemberAccess]
    return func


def validate_plugin_class(cls) -> tuple[bool, list[Exception]]:
    required_methods: dict[str, list[str]] = {}
    allowed_vars: list[str] = []
    forbidden_underscores: list[str] = []
    class_errors: list[Exception] = []

    # 1. Validate Methods
    found_methods = {
        name: func
        for name, func in inspect.getmembers(cls, predicate=inspect.isfunction)
        if not (name.startswith("__") and name.endswith("__"))
    }

    for method_name, expected_params in required_methods.items():
        if method_name not in found_methods:
            class_errors.append(
                TypeError(
                    f"Required method '{method_name}' is missing in '{cls.__name__}'."
                )
            )
            continue

        sig = inspect.signature(found_methods[method_name])
        params = sig.parameters

        for p_name in expected_params:
            if p_name == "args":
                if not any(p.kind == p.VAR_POSITIONAL for p in params.values()):
                    class_errors.append(
                        TypeError(f"Method '{method_name}' must support *args.")
                    )
            elif p_name == "kwargs":
                if not any(p.kind == p.VAR_KEYWORD for p in params.values()):
                    class_errors.append(
                        TypeError(f"Method '{method_name}' must support **kwargs.")
                    )
            elif p_name not in params:
                class_errors.append(
                    TypeError(
                        f"Argument '{p_name}' is missing in method '{method_name}'."
                    )
                )

    for method_name, func in found_methods.items():
        if method_name in required_methods:
            continue

        has_underscore = method_name.startswith("_")
        has_internal_attr = getattr(func, "is_internal", False)

        if not (has_underscore and has_internal_attr):
            class_errors.append(
                AttributeError(
                    f"Function '{method_name}' forbidden. Extras must have '_' AND @internal."
                )
            )

    instance = None
    try:
        instance = cls()
    except Exception as e:
        class_errors.append(
            RuntimeError(f"Could not instantiate '{cls.__name__}' for validation: {e}")
        )

    if instance:
        all_attributes = {
            name: value
            for name, value in inspect.getmembers(instance)
            if not (inspect.isfunction(value) or inspect.ismethod(value))
            and not (name.startswith("__") and name.endswith("__"))
        }

        for attr_name in all_attributes:
            if attr_name in forbidden_underscores:
                class_errors.append(
                    AttributeError(
                        f"The underscore variable '{attr_name}' is explicitly forbidden."
                    )
                )

            if attr_name in allowed_vars or attr_name.startswith("_"):
                continue

            class_errors.append(
                AttributeError(
                    f"Unauthorized attribute '{attr_name}' found. "
                    f"Instance variables (self.{attr_name}) must start with '_' or be whitelisted."
                )
            )

    if class_errors:
        # print(f"Validation Failed for '{cls.__name__}':")
        # for error in class_errors:
        # print(f"  - {type(error).__name__}: {error}")

        return False, class_errors
    else:
        # print(f"Class '{cls.__name__}' successfully validated.")
        return True, []
