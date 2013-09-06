if [[ "$TERM" != 'emacs' ]]
then

    typeset -A key
    key=(
        Home     "${terminfo[khome]}"
        End      "${terminfo[kend]}"
        Insert   "${terminfo[kich1]}"
        Delete   "${terminfo[kdch1]}"
        Up       "${terminfo[kcuu1]}"
        Down     "${terminfo[kcud1]}"
        Left     "${terminfo[kcub1]}"
        Right    "${terminfo[kcuf1]}"
        PageUp   "${terminfo[kpp]}"
        PageDown "${terminfo[knp]}"
    )

    function bind2maps () {
        local i sequence widget
        local -a maps

        while [[ "$1" != "--" ]]; do
            maps+=( "$1" )
            shift
        done
        shift

        sequence="${key[$1]}"
        widget="$2"

        [[ -z "$sequence" ]] && return 1

        for i in "${maps[@]}"; do
            bindkey -M "$i" "$sequence" "$widget"
        done
    }

    bind2maps emacs             -- Home   beginning-of-line
    bind2maps       viins vicmd -- Home   vi-beginning-of-line
    bind2maps emacs             -- End    end-of-line
    bind2maps       viins vicmd -- End    vi-end-of-line
    bind2maps emacs viins       -- Insert overwrite-mode
    bind2maps             vicmd -- Insert vi-insert
    bind2maps emacs             -- Delete delete-char
    bind2maps       viins vicmd -- Delete vi-delete-char
    bind2maps emacs viins vicmd -- Up     history-search-backward
    bind2maps emacs viins vicmd -- Down   history-search-forward
    bind2maps emacs             -- Left   backward-char
    bind2maps       viins vicmd -- Left   vi-backward-char
    bind2maps emacs             -- Right  forward-char
    bind2maps       viins vicmd -- Right  vi-forward-char

    # Make sure the terminal is in application mode, when zle is
    # active. Only then are the values from $terminfo valid.
    if (( ${+terminfo[smkx]} )) && (( ${+terminfo[rmkx]} )); then
        function zle-line-init () {
            printf '%s' ${terminfo[smkx]}
        }
        function zle-line-finish () {
            printf '%s' ${terminfo[rmkx]}
        }
        zle -N zle-line-init
        zle -N zle-line-finish
    fi

    unfunction bind2maps

fi # [[ -z "$DEBIAN_PREVENT_KEYBOARD_CHANGES" ]] && [[ "$TERM" != 'emacs' ]]

