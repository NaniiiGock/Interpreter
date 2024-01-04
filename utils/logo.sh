#!/usr/bin/env zsh

# Define the rainbow colors
RAINBOW=(
  $'\033[38;5;196m' # Red
  $'\033[38;5;202m' # Orange
  $'\033[38;5;082m' # Green
  $'\033[38;5;226m' # Bright Yellow
  $'\033[38;5;163m' # Cyan
  $'\033[38;5;093m' # Magenta
  $'\033[38;5;44m' # Blue
  $'\033[38;5;15m' # Bright white
)

# Reset color
RESET=$'\e[0m'

# MacTell ASCII art lines
ART_LINES=(
  "\$\$\      \$\$\               \$\$\$\$\$\$\$\$\      \$\$\\$\$\ "
  "\$\$\$\    \$\$\$ |              \__\$\$  __|     \$\$ \$\$ |"
  "\$\$\$\$\  \$\$\$\$ |\$\$\$\$\$\$\  \$\$\$\$\$\$\$\\$\$ |\$\$\$\$\$\$\ \$\$ \$\$ |"
  "\$\$\\$\$\\$\$ \$\$ |\____\$\$\\$\$  _____\$\$ \$\$  __\$\$\\$\$ \$\$ |"
  "\$\$ \\$\$\$  \$\$ |\$\$\$\$\$\$\$ \$\$ /     \$\$ \$\$\$\$\$\$\$\$ \$\$ \$\$ |"
  "\$\$ |\\$  /\$\$ \$\$  __\$\$ \$\$ |     \$\$ \$\$   ____\$\$ \$\$ |"
  "\$\$ | \_/ \$\$ \\$\$\$\$\$\$\$ \\$\$\$\$\$\$\$\\$\$ \\$\$\$\$\$\$\$\\$\$ \$\$ |"
  "\__|     \__|\_______|\_______\__|\_______\__\__|"
)

# Print each line of the ASCII art in a different color
# shellcheck disable=SC2068
for i in ${!ART_LINES[@]}; do
  color_index=$((i % ${#RAINBOW[@]}))
  printf "%b%s%b\n" "${RAINBOW[$color_index]}" "${ART_LINES[i]}" "$RESET"
done

