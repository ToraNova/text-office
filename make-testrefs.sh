#!/bin/bash

. bin/activate

printf 'are you sure you want to regenerate the testrefs? yes/(no):'
read yesno
if [ "${yesno}" = "yes" ]
then
    arr=(dual toc headfoot figures lists tables)

    for s in ${arr[@]}; do
        python ./docxtool.py samples/$s.md -o testrefs/$s.docx
    done;
fi
