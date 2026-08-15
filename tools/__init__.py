import importlib
import pkgutil

def register_all(mcp):
    """Auto-discover and register every tool module in tools/, including subdirs"""
    package = __name__
    for _, module_name, is_pkg in pkgutil.walk_packages(__path__, prefix=package + "."):
        if is_pkg:
            continue  # skip package __init__ files themselves, only import leaf modules
        module = importlib.import_module(module_name)
        if hasattr(module, "register"):
            module.register(mcp)
            print(f"Registered tool module: {module_name}")