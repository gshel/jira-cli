#!/bin/bash
if [ ! -L ".git/hooks/pre-commit" ]; then
    cp "./.git_hooks_pre-commit" ".git/hooks/pre-commit"
    chmod +x .git/hooks/pre-commit
fi