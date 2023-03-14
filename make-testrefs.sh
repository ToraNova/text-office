#!/bin/bash

. bin/activate

printf 'are you sure you want to regenerate the testrefs? yes/(no):'
read yesno
if [ "${yesno}" = "yes" ]
then
    arr=(dual toc headfoot figures lists tables sections)

    for s in ${arr[@]}; do
        python ./text-office.py samples/$s.md -o testrefs/$s.docx
    done;

    python ./text-office.py samples/auto_indent.md -o testrefs/auto_indent.docx -dxopt auto_left_indent=0.4in
fi
