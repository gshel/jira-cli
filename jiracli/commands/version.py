import os
import sys
from importlib import metadata as pkgmd

import click

import jiracli


def _package_deps(package, deps=None, ignore=()):
    """Recursive gather package's named transitive dependencies."""
    if deps is None:
        deps = []
    try:
        pdeps = pkgmd.requires(package) or ()
    except pkgmd.PackageNotFoundError:
        return deps
    for r in pdeps:
        # skip optional deps
        if ';' in r and 'extra' in r:
            continue
        for idx, c in enumerate(r):
            if not c.isalnum() and c not in ('-', '_', '.'):
                break
        if idx + 1 == len(r):
            idx += 1
        pkg_name = r[:idx]
        if pkg_name in ignore:
            continue
        if pkg_name not in deps:
            try:
                _package_deps(pkg_name, deps, ignore)
            except pkgmd.PackageNotFoundError:
                continue
            deps.append(pkg_name)
    return deps


def generate_requirements(packages, ignore=(), exclude=(), include_self=False):
    """Generate frozen requirements file for the given set of packages
    if include_self is True we'll also include the packages in the generated
    requirements.
    """
    if pkgmd is None:
        raise ImportError("importlib_metadata missing")
    if isinstance(packages, str):
        packages = [packages]

    deps = []
    for p in packages:
        _package_deps(p, deps, ignore=ignore)
    lines = []
    if include_self:
        deps = list(set(deps).union(packages))
    for d in sorted(deps):
        if d in exclude:
            continue
        try:
            lines.append(
                '%s==%s' % (d, pkgmd.distribution(d).version))
        except pkgmd.PackageNotFoundError:
            continue
    return '\n'.join(lines)


@click.command()
@click.option("--debug", is_flag=True, help="Print info for bug reports.")
def version(debug: bool):
    """Display the current version."""
    if not debug:
        click.echo(jiracli.__version__)
        return
    click.echo(f"\nPlease copy/paste the following info into any bug reports:\n")
    click.echo(f"jira-cli:   v{jiracli.__version__}")
    indent = 12
    pyversion = sys.version.replace('\n', '\n' + ' ' * indent)
    click.echo(f"Python:     {pyversion}")
    # os.uname is only available on recent versions of Unix
    try:
        click.echo(f"Platform:   {os.uname()}")
    except Exception:  # pragma: no cover
        click.echo(f"Platform:   {sys.platform}")
    is_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    click.echo(f"Using venv: {is_venv}")
    in_container = os.path.exists('/.dockerenv')
    click.echo(f"Docker:     {str(bool(in_container))}")
    click.echo("Installed: \n")
    packages = ['jira-cli']
    click.echo(generate_requirements(packages))
