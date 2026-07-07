import importlib
import pkgutil

def register_all(mcp):
    """Auto-discover and register every tool module in this package."""
    package = __name__
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        if hasattr(module, "register"):
            module.register(mcp)
            print(f"Registered tool module: {module_name}")