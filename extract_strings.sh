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
	local target="/media/Koo/MS_Malware_Classification_Challenge/trainBin/$1"
	local stringTarget="/media/Koo/MS_Malware_Classification_Challenge/trainBin/strings"
	allFiles=`ls $target`
	
	cnt=1
	for file in $allFiles
	do
		local result="$stringTarget/$1_strs_$file.txt"
		if [[ $target/$file == *_raw ]]; then
			echo -e "\t" [$cnt] $target/$file
			strings -10 $target/$file >> $result
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
		echo "All Saved the result to $stringTarget"
else
	printUsage
fi
