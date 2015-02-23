#!/bin/bash

showDate()
{
        echo "-------------------------------------------"
        echo `date +"%A %d, %B in %Y (%r)"`
        echo "-------------------------------------------"
}

showSettings()
{
        echo "Current Settings: "
        echo -e "\tReplaying directory: $1"
}

confirmParameters()
{
        local answer
        echo -n "Proceed? (y/n) "
        read answer
        if [ "$answer" == "y" ] || [ "$answer" == "Y" ] || [ "$answer" == "yes" ]; then
                echo "OK!"
                return
        else
                printUsage
                exit
        fi
}

printUsage()
{
        echo "Usage: $0 [target directory]"
		echo "This script is to extract \'import dlls\'"
}

doExtract()
{
	local target="/media/Koo/MS_Malware_Classification_Challenge/train/$1"
	local result="/media/Koo/MS_Malware_Classification_Challenge/train/import_functions_$1.txt"
	allFiles=`ls $target`
	
	if [ ! -e "$result" ]
	then
		touch $result
	else
		rm -rf $result
		touch $result
	fi
	
	cnt=1
	for file in $allFiles
	do
		if [[ $target/$file == *.asm ]]; then
			echo -e "\t" [$cnt] $target/$file
			cat $target/$file | egrep '^.idata' | egrep '(extrn|Imports)' | \
			awk -F" " '{if ( $7 == "") { \
							split($0, dlls, ";"); \
							split(dlls[2], dll, " "); \
							print "\n" dll[3] } \
						else { print $7 }}' >> $result
			cnt=$[$cnt+1]
		fi
	done
}

if [ $# -eq 0 ]
	then
		showDate
		confirmParameters
		for i in "1" "2" "3" "4" "5" "6" "7" "8" "9"
		do
			echo "Processing Directory.. $i"
			doExtract $i
		done
		echo "All Saved the result to /media/Koo/MS_Malware_Classification_Challenge/train/"
else
	printUsage
fi
