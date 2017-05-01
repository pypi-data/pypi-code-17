import spip.install

def test_install_av():
    # AV needs git during setup phase
    system = spip.install.System.get_current()
