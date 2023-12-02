# Get the current shell from the SHELL environment variable
current_shell=$(basename "$SHELL")

# Function to add alias to shell configuration file
add_alias() {
    local alias_name="$1"
    local alias_command="$2"
    local shell_rc_file="$3"
    
    if ! grep -q "# Guangzhao He Project Configuration" "$shell_rc_file"; then
        echo "# Guangzhao He Project Configuration" >> "$shell_rc_file"
    fi

    if ! grep -q "$alias_name" "$shell_rc_file"; then
        echo "alias $alias_name=\"$alias_command\"" >> "$shell_rc_file"
        echo "Added alias $alias_name to $shell_rc_file"
    else
        echo "Alias $alias_name already exists in $shell_rc_file"
    fi
}

if [ "$current_shell" = "bash" ]; then
    add_alias "hgz" "python3 main.py" "$HOME/.bashrc"
    add_alias "hgzd" "python3 main.py --dist=True" "$HOME/.bashrc"
    add_alias "hgzt" "python3 main.py --test=True" "$HOME/.bashrc"
    add_alias "hgztd" "python3 main.py --dist=True --test=True" "$HOME/.bashrc"
elif [ "$current_shell" = "zsh" ]; then
    add_alias "hgz" "python3 main.py" "$HOME/.zshrc"
    add_alias "hgzd" "python3 main.py --dist=True" "$HOME/.zshrc"
    add_alias "hgzt" "python3 main.py --test=True" "$HOME/.zshrc"
    add_alias "hgztd" "python3 main.py --dist=True --test=True" "$HOME/.zshrc"
else
    echo "Unknown shell: $current_shell"
    exit 1
fi

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${YELLOW}Setup procedure complete. Welcome${YELLOW}."
echo "${NC}Please restart shell to continue..."
