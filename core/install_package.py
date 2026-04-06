# ------------ EXTERNAL IMPORTS ------------
import subprocess
import sys
import warnings
# ------------ INTERNAL IMPORTS ------------
from ..utils.dprint import dprint, DebugWarning
from .is_installed import is_installed

# ------------ FUNCTION DEFINITION ------------
def install_package(installing_name, force_reinstall=False, upgrade=False,
                    version=None, show_output=True):
    """Installs a package using pip with version control and output management.
    Parameters:
    - installing_name: package name (e.g. "numpy")
    - force_reinstall: if True, reinstalls even if already present
    - upgrade: if True, upgrades the package
    - version: version condition (e.g. ">=1.2.3")
    - show_output: controls both dprint messages and pip output
    Notes:
    - Uses 'pip install' internally
    - Uses 'is_installed' to check existence/version
    - Uses 'dprint' (based on warnings) for controllable messages

    Flow:
    1. Constructs pip command
    2. Checks if package is installed and meets version
    3. Decides whether to install, upgrade, or skip
    4. Executes pip command with appropriate flags
    5. Handles errors and outputs messages accordingly

        Raises:
        - ValueError: if the version specifier is invalid
    
    Future improvements:
    - Improve pip calling (e.g., use pip's internal API if possible)
    - Add more detailed error handling and logging
    """

    # Build the pip command
    cmd = [sys.executable, "-m", "pip", "install"]

    # Build the package specification with version if provided
    package_spec = f"{installing_name}{version}" if version else installing_name

    # if show_output is False, we want to suppress both dprint and pip output
    if not show_output:
        cmd += ["-q"]

    # Warning control: we want to suppress dprint messages if show_output is False
    with warnings.catch_warnings():
        if not show_output:
            warnings.simplefilter("ignore", DebugWarning)

        # Forced Mode: reinstalls regardless of current state
        if force_reinstall:
            dprint(f"Reinstalling '{package_spec}'...")
            try:
                subprocess.check_call(cmd + ["--force-reinstall", package_spec])
                dprint(f"'{package_spec}' reinstalled successfully.")
            except subprocess.CalledProcessError as e:
                warnings.warn(f"Error occurred while reinstalling '{package_spec}': {e}", UserWarning)
            return

        # Version check: if version is specified, check if it meets the condition
        installed = is_installed(installing_name, version)

        # SKIP: Already installed and meets version requirement
        if installed and not upgrade:
            dprint(f"'{package_spec}' is already installed.")
            return

        # UPDATE
        if installed and upgrade:
            dprint(f"Upgrading '{package_spec}'...")
            try:
                subprocess.check_call(cmd + ["--upgrade", package_spec])
                dprint(f"'{package_spec}' upgraded successfully.")
            except subprocess.CalledProcessError as e:
                warnings.warn(f"Error occurred while upgrading '{package_spec}': {e}", UserWarning)
            return

        # INSTALLATION: Not installed or doesn't meet version requirement
        dprint(f"Installing '{package_spec}'...")
        try:
            subprocess.check_call(cmd + [package_spec])
            dprint(f"'{package_spec}' installed successfully.")
        except subprocess.CalledProcessError as e:
            warnings.warn(f"Error occurred while installing '{package_spec}': {e}", UserWarning)
