#!/usr/bin/env zsh

# Define the rainbow colors
RAINBOW=(
  $'\e[31m' # Red
  $'\e[33m' # Yellow
  $'\e[32m' # Green
  $'\e[36m' # Cyan
  $'\e[34m' # Blue
  $'\e[35m' # Magenta
  $'\e[33;1m' # Bright Yellow
  $'\e[37;1m' # Bright white
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

