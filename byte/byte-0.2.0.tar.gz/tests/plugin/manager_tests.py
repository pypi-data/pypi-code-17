from __future__ import absolute_import, division, print_function

from byte.core.plugin.manager import PluginManager
import byte.executors.memory


def test_discovery():
    """Test plugins can be discovered."""
    plugins = PluginManager()

    # Ensure the core executors have been registered
    assert ('executor', 'file') in plugins
    assert ('executor', 'memory') in plugins


def test_provided_modules():
    """Test plugins can be resolved from modules."""
    plugins = PluginManager([
        byte.executors.memory
    ])

    # Ensure only one plugin exists
    assert len(plugins) == 1

    # Ensure memory executor has been registered
    assert ('executor', 'memory') in plugins
