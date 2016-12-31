#!/bin/bash

TREE_SIZE=8
ALLOWED_CHARS="-A-Za-z0-9_,.="

red="\e[31m"
green="\e[32m"
yellow="\e[33m"
brown="\e[90m"
blue="\e[34m"
reset="\e[0m"
b="\e[1m"
u="\e[4m"

# some ugly strings
dashed_line="$yellow+---------------------------------------------------------------------------------+$reset"
empty_line="$yellow|                                                                                 |$reset"
stars="$yellow|             *                          *                          *             |$reset"
base1="$yellow|$brown             \$                          \$                          \$             $yellow|$reset"
base2="$yellow|$brown           \"\"\"\"\"                      \"\"\"\"\"                      \"\"\"\"\"           $yellow|$reset"
tree_base="$base1\n$base2"
tree_legend="$yellow|        $b${red}Red Tree$reset [1]              $b${green}Green Tree$reset [2]              ${b}No Tree$reset [3]        $yellow|$reset"

r[0]="$brown             |             $reset"
r[1]="$red            ###            $reset"
r[2]="$red           #####           $reset"
r[3]="$red          #######          $reset"
r[4]="$red         #########         $reset"
r[5]="$red        ###########        $reset"
r[6]="$red       #############       $reset"
r[7]="$red      ###############      $reset"
r[8]="$red     #################     $reset"
r[9]="$red    ###################    $reset"
r[10]="$red   #####################   $reset"

g[0]="$brown             |             $reset"
g[1]="$green            ===            $reset"
g[2]="$green           =====           $reset"
g[3]="$green          =======          $reset"
g[4]="$green         =========         $reset"
g[5]="$green        ===========        $reset"
g[6]="$green       =============       $reset"
g[7]="$green      ===============      $reset"
g[8]="$green     =================     $reset"
g[9]="$green    ===================    $reset"
g[10]="$green   =====================   $reset"

declare -A trees
declare -A tree_heights

function splash {
    echo -e $green
    echo -e "$reset"
    cat "santa_splash"
    echo -e "${b}Look at that wonderful christmas tree! "
    echo -e "${b}Help Santa sort out the other christmas trees that somewhat got mixed up!$reset"
    echo ""
}



function get_max_height {
    local max="${tree_heights[0]}"
    if [[ "${tree_heights[1]}" -gt "$max" ]]; then
        max=${tree_heights[1]}
    fi
    if [[ "${tree_heights[2]}" -gt "$max" ]]; then
        max=${tree_heights[2]}
    fi

    echo "$max"
}


function print_trees {
    local height=$(get_max_height)
    ((height++))
    echo -e "$dashed_line"
    echo -e "$empty_line"
    echo -e "$stars"

    local line
    for ((i=$height; i >= 0; i--)); do
        line="$yellow|$reset"
        for ((twr=0; twr < 3; twr++)); do
            local branch=${trees[$twr,$i]}

            if [[ $branch -gt 0 ]]; then
                line="$line${r[$branch]}"
            else
                line="$line${g[${branch#-}]}"
            fi
        done
        line="$line$yellow|$reset"
        echo -e  "$line"
    done

    echo -e "$tree_base"
    echo -e "$empty_line"
    echo -e "$tree_legend"
    echo -e "$dashed_line"

    echo ""
}

function get_heights {
    tree_heights[0]=-1
    tree_heights[1]=-1
    tree_heights[2]=-1
    for ((i=$((2*$TREE_SIZE+1)); i>=0; i--)); do
        if [[ ${trees[0,$i]} -ne "0" && ${tree_heights[0]} -eq "-1" ]]; then
            tree_heights[0]=$i
        fi

        if [[ ${trees[1,$i]} -ne "0" && ${tree_heights[1]} -eq "-1" ]]; then
            tree_heights[1]=$i
        fi

        if [[ ${trees[2,$i]} -ne "0" && ${tree_heights[2]} -eq "-1" ]]; then
            tree_heights[2]=$i
        fi
    done

}

function make_move {
    local from=$(($1-1))
    local to=$(($2-1))
    local from_height=${tree_heights[$from]}
    local to_height=${tree_heights[$to]}

    if [[ ${trees[$from,$from_height]} -eq "0" ]]; then
        echo "nothing there"
        return
    fi

    to_size=${trees[$to,$to_height]#-}
    if [[  "$to_size" -ne "0" && "${trees[$from,$from_height]#-}" > "$to_size" ]]; then
        echo "can't place large branches above little branches"
        return
    fi


    trees[$to,$(($to_height+1))]=${trees[$from,$from_height]}
    trees[$from,$from_height]=0

    ((tree_heights[$to]++))
    ((tree_heights[$from]--))
}

function get_input {
    local input
    read input
    local filtered=$(echo -n "$input" | sed "s/[^$ALLOWED_CHARS]//g")
    if [[ "$filtered" =~ $1 ]]; then
        echo "$input"
    fi
}

function check_success {
    for ((i=$(($TREE_SIZE-1)); i>=0; i--)); do
        if [[ "${trees[0,$i]}" -ne "$(($TREE_SIZE-$i))" \
            || "${trees[1,$i]}" -ne "-$(($TREE_SIZE-$i))" ]]; then 
            return
        fi
    done

    print_trees
    echo ""
    echo -e "$b$red\t\tCongrats you did it!!$reset"
    echo ""
    echo -e "Do you want a present from Santa? [${b}y$reset]es / [${b}n$reset]o"
    echo -n "> "
    local answer=$(get_input ^\(y\|n\)$)
    if [[ ${answer} = "y" ]]; then
        local santa="santa"
        echo -e "Ok then! Do you wish to get some [${b}c$reset]andy or some [${b}a$reset]pples?"
        echo -n "> "
        local present=$(get_input ^\(c\|i\)$)
        if [[ ${present:0:1} = "c" ]]; then
            echo "Ahhh candy is great!"
            santa="$santa --choice candy"
        else
            echo "Mhhm healthy apples, good choice!"
            santa="$santa --choice apples"
        fi

        echo -e "But as you know only the nice people deserve a present from Santa!\n"
        echo -e "Do you think you have been [${b}n$reset]aughty or n[${b}i$reset]ce?"
        echo -n "> "
        local naughtiness=$(get_input ^\(n\|i\)$)
        santa="$santa --naughtiness $naughtiness"

        echo -e "Ok I have prepared your request and will send it off to Santa!\n"
        echo "Let's see what he has to say:"
        eval "$santa" <&-
    else
        echo "Well ok then.. bye!"
        exit
    fi
    echo
    exit
}

function save_progress {
    echo -n "" > "progress"
    for ((i=0; i<3; i++)); do
        for ((j=0; j<2*$TREE_SIZE+1; j++)); do
            echo -n "${trees[$i,$j]} " >> "progress"
        done
    done
}

function load_progress {
    echo "Great to see you back! Which ID has Santa given you?"
    echo -n "> "
    uuid=$(get_input ^[[:alnum:]]+$)
    local sandbox="sandboxes/$uuid"
    if [ -f "$sandbox/progress" ]; then
        loaded=($(cat "$sandbox/progress"))
        for ((i=0; i<2*$TREE_SIZE+1; i++)); do
            trees[0,$i]=${loaded[$i]}
            trees[1,$i]=${loaded[$(($i+2*$TREE_SIZE+1))]}
            trees[2,$i]=${loaded[$(($i+4*$TREE_SIZE+2))]}
        done

        cd "sandboxes/$uuid"
        start_working
    else
        echo "$sandbox/progress doesn't exist....."
    fi
}

function new_workplace {
    echo -e "\n\n"
    echo -e "Return to help Santa at any time with this ID: $b$uuid$reset\n"
    local x=1
    for ((i=0; i<$TREE_SIZE; i++)); do
        x=$(($x*-1))
        trees[0,$i]=$(($x * ($TREE_SIZE-$i)))
        trees[1,$i]=$(($x * ($i-$TREE_SIZE)))
        trees[2,$i]=0
    done
    for ((i=$TREE_SIZE; i<2*$TREE_SIZE+1; i++)); do
        trees[0,$i]=0
        trees[1,$i]=0
        trees[2,$i]=0
    done
    start_working
}

function visit_santa {
    echo "Hohoho!"
    echo "Which part of the North Pole would you like to see?"
    echo -e "- [${b}1]$reset The elfs"
    echo -e "- [${b}2]$reset Santa himself"
    echo -e "- [${b}3$reset] Some candy please!"
    echo -n "> "
    local choice=$(get_input ^[[:digit:]]$)

    if [[ $choice = "" ]]; then
        echo "invalid choice, come back later"
        return
    fi
    cat santa_$choice
}

function start_working {
    get_heights
    while true; do
        echo  ""
        print_trees
        echo -e "Santa wants an all$green green$reset and an all$red red$reset tree!"
        echo -en "Rearrange branches (e.g. ${b}12$reset, ${b}32$reset, etc. or you can also rearrange multiple branches at once like ${b}1232$reset): "
        local move=$(get_input ^[[:digit:]]+$)
        echo ""
        local length=${#move}
        if [[ $(($length % 2)) -ne 0 ]]; then
            echo "Doesn't look like valid moves..."
        fi

        for ((i=0; i < $length; i += 2)); do
            local from=${move:$i:1}
            local to=${move:$i+1:1}
            if [[ "$from" -lt "1" || \
                    "$from" -gt "3" || \
                    "$from" -eq "$to" || \
                    "$to" -lt "1" || \
                    "$to" -gt "3" ]]; then
                echo "Santa says you can't do that!"
                break
            else
                make_move $from $to
            fi
        done
        check_success
        save_progress
    done

}

function sandbox_it {
    uuid=$(head /dev/urandom | sha1sum | cut -f1 -d" ")
    mkdir "sandboxes/$uuid"
    cd "sandboxes/$uuid"
}

function main_menu {
    while true; do
        echo -e "- [${b}S$reset]tart helping Santa"
        echo -e "- [${b}C$reset]ontinue helping Santa"
        echo -e "- [${b}V$reset]isit the North Pole"
        echo -e "- [${b}Q$reset]uit"
        echo -n "> "
        local choice=$(get_input ^[[:upper:]]$)

        case $choice in
            S)
                sandbox_it
                new_workplace
            ;;
            C)
                load_progress
            ;;
            V)
                visit_santa
            ;;
            Q)
                echo "Bye!"
                exit
            ;;
            *)
                echo "Santa didn't understand.... :("
            ;;
        esac
    done
}

splash
main_menu

