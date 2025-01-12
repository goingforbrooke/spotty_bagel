"""Miscellaneous utilities."""
from logging import error, debug
from pathlib import Path
from platform import system
from subprocess import run as run_cli


"""Check if an application is installed on the host system."""
def application_is_installed(application_name, throw_error) -> bool:
    # Applications that can by found by `which` or `where`.
    which_where_applications = ['which', 'where', 'open', 'osascript']
    # Applications that require us to check installation directories for.
    manual_find_applications = ['spotify', 'vlc']

    host_platform = system()

    # Perform a which/where application check.
    if application_name.lower() in which_where_applications:
        # Choose the platform-specific command to check for programs with.
        if host_platform == 'Windows':
            which_or_where = 'where'
        # Assume that non-Windows platforms (MacOS or Linux, probably) are unix systems 🦕.
        elif host_platform == 'Darwin':
            # I prefer `where`  in the terminal on my (MacOS) machine, but it's not installed by default.
            which_or_where = 'which'
        else:
            error_message = f'Unrecognized host platform: {host_platform}.'
            error(error_message)
            raise RuntimeError(error_message)

        # Disabled b/c max recursion depth exceeded.
        ## Ensure that `which` or `where` is installed.
        #if not application_is_installed(which_or_where, throw_error=True):
        #    error_message = f"The CLI application {which_or_where} isn't installed. We need it to check if other applications are installed."
        #    error(error_message)
        #    # Always throw errors if `which`/`where` isn't installed.
        #    raise RuntimeError(error_message)

        # Check for the given application with `which`/`where`.
        cli_args = [which_or_where, application_name]
        # Error out if `which`/`where` couldn't find the application.
        run_cli(cli_args, check=True)

    # Perform a manual application check.
    elif application_name.lower() in manual_find_applications:
        if host_platform == 'Windows':
            error_message = f"Manual application discovery isn't supported for Windows."
            error(error_message)
            # todo: Add manual application discovery for Windows.
            raise NotImplemented(error_message)
        elif host_platform == 'Darwin':
            expected_path = Path(f'/Applications/{application_name.capitalize()}.app')
            if expected_path.exists():
                debug(f'Found application {application_name} at {expected_path}')
            else:
                error_message = f'Failed to find application {application_name} at {expected_path}'
                error(error_message)
                if throw_error:
                    raise RuntimeError(error_message)
        else:
            error_message = f'Unrecognized host platform: {host_platform}.'
            error(error_message)
            raise RuntimeError(error_message)

    else:
        error_message = f'Unrecognized application "{application_name}"'
        error(error_message)
        raise RuntimeError(error_message)

    debug(f"Found that application {application_name} is installed.")
    return True
