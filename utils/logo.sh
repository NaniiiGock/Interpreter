#!/bin/bash

RB_RED=$(printf '\033[38;5;196m')
RB_ORANGE=$(printf '\033[38;5;202m')
RB_YELLOW=$(printf '\033[38;5;226m')
RB_GREEN=$(printf '\033[38;5;082m')
RB_BLUE=$(printf '\033[38;5;021m')
RB_INDIGO=$(printf '\033[38;5;093m')
RB_VIOLET=$(printf '\033[38;5;163m')
RB_RESET=$(printf '\033[0m')

EXTENDED_RAINBOW=(
       $RB_RED
       $RB_ORANGE
       $RB_YELLOW
       $RB_GREEN
       $RB_BLUE
       $RB_INDIGO
       $RB_VIOLET
       $RB_RED
       $RB_ORANGE
       $RB_YELLOW
       $RB_GREEN
    )


rotate_colors() {
    local first_color=$1
    EXTENDED_RAINBOW=("${EXTENDED_RAINBOW[@]:1}" "$first_color")
}

for _ in {1..5}; do
    printf '%sI%s n%s t%s e%s r%s p%s r%s e%s t%s e%s r%s\n' "${EXTENDED_RAINBOW[@]}" "$RB_RESET"
    rotate_colors "${EXTENDED_RAINBOW[0]}"
done